import os
import sys
from datetime import datetime, timedelta

if os.name != "nt":
    bundled_site_packages = os.path.join(os.path.dirname(__file__), ".venv", "Lib", "site-packages")
    if os.path.isdir(bundled_site_packages) and bundled_site_packages not in sys.path:
        sys.path.append(bundled_site_packages)

from openpyxl import Workbook, load_workbook
from api.catalog import build_movie_metadata, catalog_movie_rows
from model import (
    Admin,
    Booking,
    DuplicateUsername,
    InvalidCredentials,
    InvalidInput,
    InvalidSeatSelection,
    InsufficientSeats,
    Movie,
    Screen,
    Show,
    Theater,
    User,
)
class ExcelManager:
    SHEET_HEADERS = {
        "Movies": ["id", "name", "language", "release_date", "status"],
        "Theaters": ["id", "name", "city"],
        "Screens": ["id", "theater_id", "screen_name", "total_seats", "seat_rows", "seats_per_row"],
        "Shows": ["id", "screen_id", "movie_id", "show_date", "show_time", "end_time", "ticket_price"],
        "Users": ["id", "username", "email", "password", "registration_date"],
        "Bookings": ["id", "user_id", "show_id", "booked_seat_numbers", "booking_date", "amount_paid", "status", "hold_expires_at"],
        "Admins": ["id", "username", "password"],
    }

    def __init__(self, path: str = "data.xlsx"):
        self.path = path
        if os.path.exists(self.path):
            self.wb = load_workbook(self.path)
        else:
            self.wb = Workbook()
        self._ensure_sheets()
        self.save()

    def _ensure_sheets(self):
        for sheet_name in self.SHEET_HEADERS:
            if sheet_name not in self.wb.sheetnames:
                self.wb.create_sheet(sheet_name)
            ws = self.wb[sheet_name]
            if ws.max_row == 1 and ws.max_column == 1 and ws.cell(row=1, column=1).value is None:
                ws.delete_rows(1)
                ws.append(self.SHEET_HEADERS[sheet_name])
            else:
                existing_headers = [ws.cell(row=1, column=col).value for col in range(1, ws.max_column + 1)]
                if existing_headers != self.SHEET_HEADERS[sheet_name]:
                    rows = list(ws.iter_rows(min_row=2, values_only=True))
                    remapped_rows = []
                    for row in rows:
                        row_map = {
                            existing_headers[col_index]: row[col_index]
                            for col_index in range(min(len(existing_headers), len(row)))
                        }
                        remapped_rows.append([row_map.get(header) for header in self.SHEET_HEADERS[sheet_name]])
                    ws.delete_rows(1, ws.max_row)
                    ws.append(self.SHEET_HEADERS[sheet_name])
                    for row_values in remapped_rows:
                        ws.append(row_values)
        if "Sheet" in self.wb.sheetnames and len(self.wb.sheetnames) > len(self.SHEET_HEADERS):
            std = self.wb["Sheet"]
            self.wb.remove(std)

    def read_sheet(self, sheet_name: str):
        ws = self.wb[sheet_name]
        rows = []
        headers = [cell.value for cell in ws[1]]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if all(cell is None for cell in row):
                continue
            rows.append({headers[col_index]: row[col_index] for col_index in range(len(headers))})
        return rows

    def write_sheet(self, sheet_name: str, rows: list):
        ws = self.wb[sheet_name]
        ws.delete_rows(1, ws.max_row)
        ws.append(self.SHEET_HEADERS[sheet_name])
        for row in rows:
            ws.append(row)

    def save(self):
        self.wb.save(self.path)


class TicketService:
    def __init__(self, data_path: str = "data.xlsx"):
        self.manager = ExcelManager(data_path)
        self.movies = []
        self.theaters = []
        self.screens = []
        self.shows = []
        self.users = []
        self.bookings = []
        self.admins = []
        self.load_data()
        self._bootstrap_defaults()
        self.cleanup_expired_bookings()

    def load_data(self):
        self.movies = [Movie.from_row(row) for row in self.manager.read_sheet("Movies")]
        self.theaters = [Theater.from_row(row) for row in self.manager.read_sheet("Theaters")]
        self.screens = [Screen.from_row(row) for row in self.manager.read_sheet("Screens")]
        self.shows = [Show.from_row(row) for row in self.manager.read_sheet("Shows")]
        self.users = [User.from_row(row) for row in self.manager.read_sheet("Users")]
        self.bookings = [Booking.from_row(row) for row in self.manager.read_sheet("Bookings")]
        self.admins = [Admin.from_row(row) for row in self.manager.read_sheet("Admins")]
        self._normalize_movie_titles()
        self._normalize_theater_cities()
        self._normalize_show_schedule()
        self._normalize_booking_statuses()

    def _normalize_movie_titles(self):
        changed = False
        for movie in self.movies:
            normalized_name = movie.name.strip().upper()
            if movie.name != normalized_name:
                movie.name = normalized_name
                changed = True
        if changed:
            self.save_all()

    def _normalize_theater_cities(self):
        changed = False
        for theater in self.theaters:
            normalized_city = theater.city.strip().title()
            if theater.city != normalized_city:
                theater.city = normalized_city
                changed = True
        if changed:
            self.save_all()

    def _normalize_show_schedule(self):
        changed = False
        for index, show in enumerate(sorted(self.shows, key=lambda item: item.id)):
            if not show.show_date:
                show.show_date = self._default_show_date(show.show_time, day_offset=index % 5)
                changed = True
            if not show.end_time or show.end_time == show.show_time:
                show.end_time = self._derive_end_time(show.movie_id, show.show_time)
                changed = True
        if changed:
            self.save_all()

    def _normalize_booking_statuses(self):
        changed = False
        for booking in self.bookings:
            normalized_status = Booking.normalize_status(booking.status)
            if booking.status != normalized_status:
                booking.status = normalized_status
                changed = True
        if changed:
            self.save_all()

    def _current_time(self):
        return datetime.now()

    def _today_string(self):
        return self._current_time().strftime("%Y-%m-%d")

    def _parse_show_start(self, show: Show):
        return datetime.strptime(f"{show.show_date} {show.show_time}", "%Y-%m-%d %H:%M")

    def _parse_show_end(self, show: Show):
        return datetime.strptime(f"{show.show_date} {show.end_time}", "%Y-%m-%d %H:%M")

    def _runtime_minutes_for_movie(self, movie_id: int):
        movie = self._find_movie(movie_id)
        if movie is None:
            return 180
        try:
            return int(build_movie_metadata(movie.name).get("runtimeMinutes", 180))
        except Exception:
            return 180

    def _derive_end_time(self, movie_id: int, show_time: str):
        start = datetime.strptime(show_time, "%H:%M")
        runtime = self._runtime_minutes_for_movie(movie_id)
        end = start + timedelta(minutes=runtime + 30)
        return end.strftime("%H:%M")

    def _default_show_date(self, show_time: str, day_offset: int = 0):
        now = self._current_time()
        proposed = now.replace(
            hour=int(show_time.split(":")[0]),
            minute=int(show_time.split(":")[1]),
            second=0,
            microsecond=0,
        ) + timedelta(days=day_offset)
        if proposed <= now:
            proposed += timedelta(days=1)
        return proposed.strftime("%Y-%m-%d")

    def _is_booking_active_for_show(self, booking: Booking, show: Show):
        if booking.status != "active":
            return False
        if booking.hold_expires_at:
            try:
                if self._current_time() > datetime.strptime(booking.hold_expires_at, "%Y-%m-%d %H:%M:%S"):
                    return False
            except ValueError:
                return False
        return self._parse_show_end(show) > self._current_time()

    def cleanup_expired_bookings(self):
        changed = False
        now = self._current_time()
        for booking in self.bookings:
            show = self._find_show(booking.show_id)
            if show is None:
                continue
            if booking.status == "cancelled":
                continue
            if booking.hold_expires_at and booking.status == "active":
                try:
                    if now > datetime.strptime(booking.hold_expires_at, "%Y-%m-%d %H:%M:%S"):
                        booking.status = "expired"
                        changed = True
                        continue
                except ValueError:
                    booking.status = "expired"
                    changed = True
                    continue
            if booking.status == "active" and now > self._parse_show_end(show):
                booking.status = "completed"
                changed = True
        if changed:
            self.save_all()
        return changed

    def _refresh_booking_states(self):
        return self.cleanup_expired_bookings()

    def get_booked_seats_for_show(self, show_id: int):
        self.cleanup_expired_bookings()
        show = self.get_show(show_id)
        seats = []
        for booking in self.bookings:
            if booking.show_id != show_id:
                continue
            if not self._is_booking_active_for_show(booking, show):
                continue
            seats.extend(booking.booked_seat_numbers)
        return sorted(set(seats))

    def _bootstrap_defaults(self):
        changed = False
        if not self.admins:
            self.register_admin("admin", "admin123")
            changed = True
        if not self.theaters:
            self._create_default_theaters_and_screens()
            changed = True
        if not self.movies:
            self._create_default_movies()
            changed = True
        if self._sync_catalog_movies():
            changed = True
        if not self.shows:
            self._create_default_shows()
            changed = True
        if self._ensure_premium_network():
            changed = True
        if self._ensure_catalog_rotation():
            changed = True
        if changed:
            self.save_all()

    def _create_default_theaters_and_screens(self):
        self.theaters.append(Theater(1, "PVR Grand Galleria", "Mumbai"))
        self.theaters.append(Theater(2, "INOX Starplex", "Delhi"))
        self.screens.append(Screen(1, 1, "Audi 1 IMAX", total_seats=220, seat_rows=11, seats_per_row=20))
        self.screens.append(Screen(2, 1, "Audi 2 Recliner", total_seats=120, seat_rows=10, seats_per_row=12))
        self.screens.append(Screen(3, 2, "Audi 1 Dolby Atmos", total_seats=180, seat_rows=10, seats_per_row=18))
        self.screens.append(Screen(4, 2, "Audi 2 Laser", total_seats=160, seat_rows=10, seats_per_row=16))

    def _create_default_movies(self):
        self.movies.append(Movie(1, "PATHAAN", "Hindi", "2024-01-05"))
        self.movies.append(Movie(2, "BAAHUBALI", "Telugu", "2023-11-20"))

    def _sync_catalog_movies(self):
        changed = False
        if self._dedupe_movies_by_title():
            changed = True
        existing = {movie.name.strip().upper(): movie for movie in self.movies}
        for item in catalog_movie_rows():
            title = item["title"].strip().upper()
            movie = existing.get(title)
            if movie is None:
                self.movies.append(Movie(self._next_id(self.movies), title, item["language"], item["releaseDate"]))
                changed = True
                continue
            if movie.language != item["language"] or movie.release_date != item["releaseDate"]:
                movie.language = item["language"]
                movie.release_date = item["releaseDate"]
                changed = True
        return changed

    def _dedupe_movies_by_title(self):
        changed = False
        grouped = {}
        for movie in self.movies:
            grouped.setdefault(movie.name.strip().upper(), []).append(movie)

        for _, movies in grouped.items():
            if len(movies) < 2:
                continue
            show_counts = {
                movie.id: sum(1 for show in self.shows if show.movie_id == movie.id)
                for movie in movies
            }
            keeper = max(movies, key=lambda movie: (show_counts[movie.id], -movie.id))
            duplicates = [movie for movie in movies if movie.id != keeper.id]

            for duplicate in duplicates:
                for show in self.shows:
                    if show.movie_id == duplicate.id:
                        show.movie_id = keeper.id
                self.movies.remove(duplicate)
                changed = True

        return changed

    def _create_default_shows(self):
        if len(self.movies) >= 2 and len(self.screens) >= 2:
            default_specs = [
                (self.screens[0].id, self.movies[0].id, "18:00", 250.0, 0),
                (self.screens[1].id, self.movies[1].id, "20:30", 300.0, 0),
                (self.screens[2].id, self.movies[0].id, "17:00", 260.0, 1),
            ]
            for screen_id, movie_id, show_time, price, day_offset in default_specs:
                self.shows.append(
                    Show(
                        self._next_id(self.shows),
                        screen_id,
                        movie_id,
                        self._default_show_date(show_time, day_offset=day_offset),
                        show_time,
                        self._derive_end_time(movie_id, show_time),
                        price,
                    )
                )

    def _ensure_premium_network(self):
        changed = False
        theater_blueprints = [
            ("PVR Orion", "Bangalore", [("Audi 1 IMAX", 280, 14, 20), ("Audi 2 Dolby Atmos", 180, 10, 18), ("Audi 3 Recliner", 96, 8, 12)]),
            ("INOX Phoenix Marketcity", "Bangalore", [("Audi 4DX", 120, 10, 12), ("Audi 2 Laser", 170, 10, 17)]),
            ("Cinepolis Nexus Shantiniketan", "Bangalore", [("Audi 1 Laser", 160, 10, 16), ("Audi 2 Atmos", 140, 10, 14)]),
            ("PVR Lower Parel", "Mumbai", [("Audi 1 IMAX", 260, 13, 20), ("Audi 2 Recliner", 108, 9, 12)]),
            ("INOX R-City", "Mumbai", [("Audi 1 Dolby Atmos", 190, 10, 19), ("Audi 2 Laser", 150, 10, 15)]),
            ("Miraj Wadala", "Mumbai", [("Audi 1 4DX", 116, 10, 12), ("Audi 2 Premium", 135, 9, 15)]),
            ("PVR Saket Select", "Delhi", [("Audi 1 IMAX", 250, 13, 19), ("Audi 2 Laser", 150, 10, 15)]),
            ("INOX Rajouri", "Delhi", [("Audi 1 Dolby Atmos", 180, 10, 18), ("Audi 2 Recliner", 96, 8, 12)]),
            ("Cinepolis DLF Avenue", "Delhi", [("Audi 1 Laser", 170, 10, 17), ("Audi 2 Premium", 130, 10, 13)]),
            ("Asian Cinemas AMB", "Hyderabad", [("Audi 1 IMAX", 280, 14, 20), ("Audi 2 Atmos", 180, 10, 18), ("Audi 3 Recliner", 110, 10, 11)]),
            ("PVR Irrum Manzil", "Hyderabad", [("Audi 1 Laser", 160, 10, 16), ("Audi 2 4DX", 120, 10, 12)]),
            ("Carnival Forum Vijaya", "Chennai", [("Audi 1 Laser", 170, 10, 17), ("Audi 2 Atmos", 150, 10, 15)]),
            ("PVR Palazzo", "Chennai", [("Audi 1 IMAX", 240, 12, 20), ("Audi 2 Recliner", 90, 9, 10)]),
            ("INOX Marina Mall", "Chennai", [("Audi 1 Premium", 155, 10, 16), ("Audi 2 Laser", 145, 10, 15)]),
            ("Cinepolis Seasons Mall", "Pune", [("Audi 1 Laser", 160, 10, 16), ("Audi 2 Dolby Atmos", 165, 11, 15)]),
            ("PVR Pavilion", "Pune", [("Audi 1 IMAX", 240, 12, 20), ("Audi 2 Recliner", 100, 10, 10)]),
            ("Miraj Hinjawadi", "Pune", [("Audi 1 Premium", 150, 10, 15), ("Audi 2 4DX", 110, 10, 11)]),
        ]

        existing_theaters = {(theater.name.lower(), theater.city.lower()): theater for theater in self.theaters}
        for theater_name, city, screens in theater_blueprints:
            key = (theater_name.lower(), city.lower())
            theater = existing_theaters.get(key)
            if theater is None:
                theater = Theater(self._next_id(self.theaters), theater_name, city)
                self.theaters.append(theater)
                existing_theaters[key] = theater
                changed = True
            for screen_name, total_seats, seat_rows, seats_per_row in screens:
                if any(screen.theater_id == theater.id and screen.screen_name.lower() == screen_name.lower() for screen in self.screens):
                    continue
                self.screens.append(
                    Screen(
                        self._next_id(self.screens),
                        theater.id,
                        screen_name,
                        total_seats=total_seats,
                        seat_rows=seat_rows,
                        seats_per_row=seats_per_row,
                    )
                )
                changed = True

        active_movies = self.get_active_movies()
        if not active_movies:
            return changed

        existing_pairs = {(show.screen_id, show.show_date, show.show_time) for show in self.shows}
        show_slots = ["09:10", "12:35", "16:00", "19:25", "22:45"]
        for screen in self.screens:
            base_price = 220
            screen_label = screen.screen_name.lower()
            if "imax" in screen_label:
                base_price = 420
            elif "4dx" in screen_label:
                base_price = 470
            elif "recliner" in screen_label:
                base_price = 360
            elif "atmos" in screen_label or "laser" in screen_label:
                base_price = 300

            for index, show_time in enumerate(show_slots[:4]):
                show_date = self._default_show_date(show_time, day_offset=index % 3)
                if (screen.id, show_date, show_time) in existing_pairs:
                    continue
                movie = active_movies[(screen.id + index) % len(active_movies)]
                self.shows.append(
                    Show(
                        self._next_id(self.shows),
                        screen.id,
                        movie.id,
                        show_date,
                        show_time,
                        self._derive_end_time(movie.id, show_time),
                        base_price + (index * 25),
                    )
                )
                existing_pairs.add((screen.id, show_date, show_time))
                changed = True

        return changed

    def _ensure_catalog_rotation(self):
        changed = False
        if not self.screens:
            return changed

        candidate_times = [
            "08:15",
            "09:10",
            "10:05",
            "11:30",
            "12:35",
            "14:00",
            "15:20",
            "16:45",
            "18:10",
            "19:35",
            "21:00",
            "22:25",
        ]
        existing_pairs = {(show.screen_id, show.show_date, show.show_time) for show in self.shows}
        screen_cursor = 0
        for movie in self.get_active_movies():
            if any(show.movie_id == movie.id for show in self.shows):
                continue
            for offset in range(len(self.screens) * len(candidate_times)):
                screen = self.screens[(screen_cursor + offset) % len(self.screens)]
                show_time = candidate_times[(movie.id + offset) % len(candidate_times)]
                show_date = self._default_show_date(show_time, day_offset=(movie.id + offset) % 4)
                if (screen.id, show_date, show_time) in existing_pairs:
                    continue
                base_price = 240
                label = screen.screen_name.lower()
                if "imax" in label:
                    base_price = 430
                elif "4dx" in label:
                    base_price = 480
                elif "recliner" in label:
                    base_price = 360
                elif "atmos" in label or "laser" in label:
                    base_price = 310
                self.shows.append(
                    Show(
                        self._next_id(self.shows),
                        screen.id,
                        movie.id,
                        show_date,
                        show_time,
                        self._derive_end_time(movie.id, show_time),
                        base_price + ((movie.id + offset) % 4) * 20,
                    )
                )
                existing_pairs.add((screen.id, show_date, show_time))
                screen_cursor = (screen_cursor + 1) % len(self.screens)
                changed = True
                break
        return changed

    def save_all(self):
        self.manager.write_sheet("Movies", [movie.to_row() for movie in self.movies])
        self.manager.write_sheet("Theaters", [theater.to_row() for theater in self.theaters])
        self.manager.write_sheet("Screens", [screen.to_row() for screen in self.screens])
        self.manager.write_sheet("Shows", [show.to_row() for show in self.shows])
        self.manager.write_sheet("Users", [user.to_row() for user in self.users])
        self.manager.write_sheet("Bookings", [booking.to_row() for booking in self.bookings])
        self.manager.write_sheet("Admins", [admin.to_row() for admin in self.admins])
        self.manager.save()

    def _next_id(self, items: list) -> int:
        return max((item.id for item in items), default=0) + 1

    def _validate_text(self, value: str, field_name: str):
        if value is None or not str(value).strip():
            raise InvalidInput(f"{field_name} cannot be empty.")

    def _find_movie(self, movie_id: int):
        return next((movie for movie in self.movies if movie.id == movie_id), None)

    def _find_theater(self, theater_id: int):
        return next((theater for theater in self.theaters if theater.id == theater_id), None)

    def _find_screen(self, screen_id: int):
        return next((screen for screen in self.screens if screen.id == screen_id), None)

    def _find_show(self, show_id: int):
        return next((show for show in self.shows if show.id == show_id), None)

    def _find_user(self, username: str):
        return next((user for user in self.users if user.username.lower() == username.lower()), None)

    def _find_user_by_id(self, user_id: int):
        return next((user for user in self.users if user.id == user_id), None)

    def _find_admin(self, username: str):
        return next((admin for admin in self.admins if admin.username.lower() == username.lower()), None)

    def get_all_screens(self):
        return list(self.screens)

    def get_theater(self, theater_id: int):
        theater = self._find_theater(theater_id)
        if theater is None:
            raise InvalidInput("Theater not found.")
        return theater

    def get_screen(self, screen_id: int):
        screen = self._find_screen(screen_id)
        if screen is None:
            raise InvalidInput("Screen not found.")
        return screen

    def get_movie(self, movie_id: int):
        movie = self._find_movie(movie_id)
        if movie is None:
            raise InvalidInput("Movie not found.")
        return movie

    def get_show(self, show_id: int):
        show = self._find_show(show_id)
        if show is None:
            raise InvalidInput("Show not found.")
        return show

    def register_admin(self, username: str, password: str):
        self._validate_text(username, "Admin username")
        self._validate_text(password, "Admin password")
        if self._find_admin(username):
            raise DuplicateUsername("Admin username already exists.")
        admin = Admin(self._next_id(self.admins), username, password)
        self.admins.append(admin)
        self.save_all()
        return admin

    def login_admin(self, username: str, password: str):
        self._validate_text(username, "Admin username")
        self._validate_text(password, "Admin password")
        admin = self._find_admin(username)
        if not admin or admin.password != password:
            raise InvalidCredentials("Invalid admin username or password.")
        return admin

    def register_user(self, username: str, email: str, password: str):
        self._validate_text(username, "Username")
        self._validate_text(email, "Email")
        self._validate_text(password, "Password")
        if self._find_user(username):
            raise DuplicateUsername("Username already exists.")
        user = User(self._next_id(self.users), username, email, password)
        self.users.append(user)
        self.save_all()
        return user

    def login_user(self, username: str, password: str):
        self._validate_text(username, "Username")
        self._validate_text(password, "Password")
        user = self._find_user(username)
        if not user or user.password != password:
            raise InvalidCredentials("Invalid username or password.")
        return user

    def add_movie(self, name: str, language: str, release_date: str):
        self._validate_text(name, "Movie name")
        self._validate_text(language, "Language")
        self._validate_text(release_date, "Release date")
        self.movies.append(Movie(self._next_id(self.movies), name.strip().upper(), language, release_date))
        self.save_all()

    def remove_movie(self, movie_id: int):
        movie = self._find_movie(movie_id)
        if movie is None:
            raise InvalidInput("Movie not found.")
        movie.status = "inactive"
        self.save_all()

    def get_active_movies(self):
        return [movie for movie in self.movies if movie.status.lower() == "active"]

    def filter_movies_by_language(self, language: str):
        self._validate_text(language, "Language")
        return [movie for movie in self.get_active_movies() if movie.language.lower() == language.lower()]

    def assign_movie_to_screen(self, movie_id: int, screen_id: int, show_time: str, ticket_price: float, show_date: str | None = None):
        movie = self._find_movie(movie_id)
        screen = self._find_screen(screen_id)
        if movie is None or movie.status.lower() != "active":
            raise InvalidInput("Selected movie is not available.")
        if screen is None:
            raise InvalidInput("Selected screen is not available.")
        self._validate_text(show_time, "Show time")
        if ticket_price <= 0:
            raise InvalidInput("Ticket price must be greater than zero.")
        resolved_show_date = show_date or self._default_show_date(show_time)
        if any(
            existing.screen_id == screen.id
            and existing.show_date == resolved_show_date
            and existing.show_time == show_time
            for existing in self.shows
        ):
            raise InvalidInput("A show is already scheduled for this screen at the selected date and time.")
        show = Show(
            self._next_id(self.shows),
            screen.id,
            movie.id,
            resolved_show_date,
            show_time,
            self._derive_end_time(movie.id, show_time),
            ticket_price,
        )
        self.shows.append(show)
        self.save_all()

    def add_theater(self, name: str, city: str):
        self._validate_text(name, "Theater name")
        self._validate_text(city, "City")
        if any(theater.name.lower() == name.lower() and theater.city.lower() == city.lower() for theater in self.theaters):
            raise InvalidInput("A theater with this name already exists in the selected city.")
        theater = Theater(self._next_id(self.theaters), name, city)
        self.theaters.append(theater)
        self.save_all()
        return theater

    def add_screen(
        self,
        theater_id: int,
        screen_name: str,
        total_seats: int = 100,
        seat_rows: int = 10,
        seats_per_row: int = 10,
    ):
        theater = self._find_theater(theater_id)
        if theater is None:
            raise InvalidInput("Theater not found.")
        self._validate_text(screen_name, "Screen name")
        if total_seats <= 0 or seat_rows <= 0 or seats_per_row <= 0:
            raise InvalidInput("Seat counts and layout values must be positive numbers.")
        if seat_rows * seats_per_row < total_seats:
            raise InvalidInput("Total seats cannot exceed rows multiplied by seats per row.")
        if any(screen.screen_name.lower() == screen_name.lower() and screen.theater_id == theater_id for screen in self.screens):
            raise InvalidInput("A screen with this name already exists in the selected theater.")
        screen = Screen(
            self._next_id(self.screens),
            theater_id,
            screen_name,
            total_seats=total_seats,
            seat_rows=seat_rows,
            seats_per_row=seats_per_row,
        )
        self.screens.append(screen)
        self.save_all()
        return screen

    def view_movie_in_theaters(self):
        schedule = []
        for show in self.shows:
            try:
                movie = self._find_movie(show.movie_id)
                screen = self._find_screen(show.screen_id)
                theater = self._find_theater(screen.theater_id)
            except Exception:
                continue
            if movie is None or screen is None or theater is None:
                continue
            schedule.append(
                {
                    "show_id": show.id,
                    "movie_name": movie.name,
                    "theater_name": theater.name,
                    "screen_name": screen.screen_name,
                    "city": theater.city,
                    "show_time": show.show_time,
                    "ticket_price": show.ticket_price,
                }
            )
        return schedule

    def get_revenue_total(self) -> float:
        self.cleanup_expired_bookings()
        return sum(booking.amount_paid for booking in self.bookings if booking.status in {"active", "completed"})

    def get_revenue_by_movie(self, movie_id: int) -> float:
        self.cleanup_expired_bookings()
        show_ids = [show.id for show in self.shows if show.movie_id == movie_id]
        return sum(
            booking.amount_paid
            for booking in self.bookings
            if booking.show_id in show_ids and booking.status in {"active", "completed"}
        )

    def get_movie_cities(self, movie_id: int):
        cities = {
            self._find_theater(self._find_screen(show.screen_id).theater_id).city
            for show in self.shows
            if show.movie_id == movie_id
            and self._find_screen(show.screen_id) is not None
            and self._find_theater(self._find_screen(show.screen_id).theater_id) is not None
        }
        return sorted(cities)

    def get_user_statistics(self):
        self.cleanup_expired_bookings()
        total_users = len(self.users)
        total_tickets = sum(
            len(booking.booked_seat_numbers)
            for booking in self.bookings
            if booking.status in {"active", "completed"}
        )
        return {
            "total_users": total_users,
            "total_bookings": len([booking for booking in self.bookings if booking.status in {"active", "completed"}]),
            "total_tickets": total_tickets,
        }

    def get_cities_with_theaters(self):
        return sorted({theater.city for theater in self.theaters})

    def _parse_language_values(self, language: str):
        return [lang.strip().lower() for lang in str(language).split(",") if lang.strip()]

    def get_available_languages(self):
        languages = {
            lang
            for movie in self.get_active_movies()
            for lang in self._parse_language_values(movie.language)
        }
        return sorted(languages)

    def filter_movies_by_language(self, language: str):
        self._validate_text(language, "Language")
        normalized_language = language.strip().lower()
        return [
            movie
            for movie in self.get_active_movies()
            if normalized_language in self._parse_language_values(movie.language)
        ]

    def get_theaters_in_city(self, city: str):
        self._validate_text(city, "City")
        return [theater for theater in self.theaters if theater.city.lower() == city.lower()]

    def get_screens_in_theater(self, theater_id: int):
        return [screen for screen in self.screens if screen.theater_id == theater_id]

    def get_shows_for_screen(self, screen_id: int):
        return [show for show in self.shows if show.screen_id == screen_id]

    def get_available_shows(self):
        self.cleanup_expired_bookings()
        return [show for show in self.shows if self._parse_show_end(show) > self._current_time()]

    def get_seat_layout(self, show_id: int):
        show = self.get_show(show_id)
        screen = self.get_screen(show.screen_id)
        return screen.get_seat_ids(), self.get_booked_seats_for_show(show_id)

    def validate_seat_selection(self, show_id: int, seat_numbers: list):
        if not seat_numbers:
            raise InvalidInput("No seats selected.")
        if len(seat_numbers) > 4:
            raise InsufficientSeats("You can book a maximum of 4 seats.")
        show = self.get_show(show_id)
        if self._parse_show_end(show) <= self._current_time():
            raise InvalidSeatSelection("This show has already ended. Please select a later show.")
        screen = self.get_screen(show.screen_id)
        valid_seats = screen.get_seat_ids()
        booked_seats = set(self.get_booked_seats_for_show(show_id))
        selected = []
        for seat in seat_numbers:
            seat = seat.strip().upper()
            if not seat:
                raise InvalidSeatSelection("Seat identifiers cannot be empty.")
            if seat in selected:
                raise InvalidSeatSelection(f"Duplicate seat selection: {seat}")
            if seat not in valid_seats:
                raise InvalidSeatSelection(f"Seat {seat} is not valid for this screen.")
            if seat in booked_seats:
                raise InvalidSeatSelection(f"Seat {seat} is already booked.")
            selected.append(seat)
        return selected

    def book_seats(self, user_id: int, show_id: int, seat_numbers: list):
        user = self._find_user_by_id(user_id)
        show = self.get_show(show_id)
        if user is None:
            raise InvalidInput("User not found.")
        seat_numbers = [seat.strip().upper() for seat in seat_numbers]
        selected = self.validate_seat_selection(show_id, seat_numbers)
        amount_paid = len(selected) * show.ticket_price
        booking = Booking(
            self._next_id(self.bookings),
            user_id,
            show_id,
            booked_seat_numbers=selected,
            amount_paid=amount_paid,
            status="active",
        )
        self.bookings.append(booking)
        self.save_all()
        return booking

    def get_user_bookings(self, user_id: int):
        self.cleanup_expired_bookings()
        return [booking for booking in self.bookings if booking.user_id == user_id and booking.status == "active"]

    def get_user_booking_history(self, user_id: int):
        self.cleanup_expired_bookings()
        return [booking for booking in self.bookings if booking.user_id == user_id]
