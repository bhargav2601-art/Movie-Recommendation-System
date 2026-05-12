from datetime import datetime
from typing import List, Optional


class InvalidCredentials(Exception):
    """Raised when admin or user credentials are invalid during login."""
    def __init__(self, message: str = "Invalid credentials provided"):
        self.message = message
        super().__init__(self.message)


class DuplicateUsername(Exception):
    """Raised when attempting to register with an already existing username."""
    def __init__(self, message: str = "Username already exists"):
        self.message = message
        super().__init__(self.message)


class InvalidSeatSelection(Exception):
    """Raised when selected seat is invalid, already booked, or unavailable."""
    def __init__(self, message: str = "Invalid seat selection"):
        self.message = message
        super().__init__(self.message)


class InsufficientSeats(Exception):
    """Raised when user tries to book more seats than allowed (max 4)."""
    def __init__(self, message: str = "Insufficient or too many seats"):
        self.message = message
        super().__init__(self.message)


class InvalidInput(Exception):
    """Raised when user input is empty, invalid, or malformed."""
    def __init__(self, message: str = "Invalid input provided"):
        self.message = message
        super().__init__(self.message)


class Movie:
    def __init__(self, id: int, name: str, language: str, release_date: str, status: str = "active"):
        self.id = int(id)
        self.name = name
        self.language = self.normalize_language(language)
        self.release_date = release_date
        self.status = status

    @staticmethod
    def normalize_language(language: str) -> str:
        if language is None:
            return ""
        normalized = [part.strip().lower() for part in str(language).split(",") if part.strip()]
        # preserve insertion order while removing duplicates
        unique_languages = list(dict.fromkeys(normalized))
        return ", ".join(unique_languages)

    @staticmethod
    def from_row(row: dict):
        return Movie(
            id=int(row["id"]),
            name=row["name"],
            language=row["language"],
            release_date=row["release_date"],
            status=row.get("status", "active") or "active",
        )

    def to_row(self) -> List[str]:
        return [self.id, self.name, self.language, self.release_date, self.status]


class Theater:
    def __init__(self, id: int, name: str, city: str):
        self.id = int(id)
        self.name = name
        self.city = city

    @staticmethod
    def from_row(row: dict):
        return Theater(id=int(row["id"]), name=row["name"], city=row["city"])

    def to_row(self) -> List[str]:
        return [self.id, self.name, self.city]


class Screen:
    def __init__(
        self,
        id: int,
        theater_id: int,
        screen_name: str,
        total_seats: int = 100,
        seat_rows: int = 10,
        seats_per_row: int = 10,
    ):
        self.id = int(id)
        self.theater_id = int(theater_id)
        self.screen_name = screen_name
        self.total_seats = int(total_seats)
        self.seat_rows = int(seat_rows)
        self.seats_per_row = int(seats_per_row)

    @staticmethod
    def from_row(row: dict):
        return Screen(
            id=int(row["id"]),
            theater_id=int(row["theater_id"]),
            screen_name=row["screen_name"],
            total_seats=int(row.get("total_seats", 100) or 100),
            seat_rows=int(row.get("seat_rows", 10) or 10),
            seats_per_row=int(row.get("seats_per_row", 10) or 10),
        )

    def to_row(self) -> List[str]:
        return [
            self.id,
            self.theater_id,
            self.screen_name,
            self.total_seats,
            self.seat_rows,
            self.seats_per_row,
        ]

    def get_seat_ids(self) -> List[str]:
        seats = []
        for row_index in range(self.seat_rows):
            row_letter = chr(65 + row_index)
            for col in range(1, self.seats_per_row + 1):
                seats.append(f"{row_letter}{col}")
                if len(seats) >= self.total_seats:
                    return seats
        return seats


class Show:
    def __init__(
        self,
        id: int,
        screen_id: int,
        movie_id: int,
        show_date: str,
        show_time: str,
        end_time: str,
        ticket_price: float,
    ):
        self.id = int(id)
        self.screen_id = int(screen_id)
        self.movie_id = int(movie_id)
        self.show_date = show_date
        self.show_time = show_time
        self.end_time = end_time
        self.ticket_price = float(ticket_price)

    @staticmethod
    def from_row(row: dict):
        return Show(
            id=int(row["id"]),
            screen_id=int(row["screen_id"]),
            movie_id=int(row["movie_id"]),
            show_date=row.get("show_date", "") or datetime.now().strftime("%Y-%m-%d"),
            show_time=row["show_time"],
            end_time=row.get("end_time", "") or row.get("show_end_time", "") or row["show_time"],
            ticket_price=float(row.get("ticket_price", 0) or 0),
        )

    def to_row(self) -> List[str]:
        return [
            self.id,
            self.screen_id,
            self.movie_id,
            self.show_date,
            self.show_time,
            self.end_time,
            self.ticket_price,
        ]


class User:
    def __init__(
        self,
        id: int,
        username: str,
        email: str,
        password: str,
        registration_date: Optional[str] = None,
    ):
        self.id = int(id)
        self.username = username
        self.email = email
        self.password = password
        self.registration_date = registration_date or datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def from_row(row: dict):
        return User(
            id=int(row["id"]),
            username=row["username"],
            email=row["email"],
            password=row.get("password", row.get("password_hash", "")),
            registration_date=row.get("registration_date", "") or datetime.now().strftime("%Y-%m-%d"),
        )

    def to_row(self) -> List[str]:
        return [self.id, self.username, self.email, self.password, self.registration_date]


class Admin:
    def __init__(self, id: int, username: str, password: str):
        self.id = int(id)
        self.username = username
        self.password = password

    @staticmethod
    def from_row(row: dict):
        return Admin(
            id=int(row["id"]),
            username=row["username"],
            password=row.get("password", row.get("password_hash", "")),
        )

    def to_row(self) -> List[str]:
        return [self.id, self.username, self.password]


class Booking:
    def __init__(
        self,
        id: int,
        user_id: int,
        show_id: int,
        booked_seat_numbers: Optional[List[str]] = None,
        booking_date: Optional[str] = None,
        amount_paid: float = 0.0,
        status: str = "active",
        hold_expires_at: Optional[str] = None,
    ):
        self.id = int(id)
        self.user_id = int(user_id)
        self.show_id = int(show_id)
        self.booked_seat_numbers = booked_seat_numbers or []
        self.booking_date = booking_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.amount_paid = float(amount_paid)
        self.status = self.normalize_status(status)
        self.hold_expires_at = hold_expires_at

    @staticmethod
    def normalize_status(status: str | None) -> str:
        normalized = (status or "active").strip().lower()
        legacy_map = {
            "confirmed": "active",
            "held": "active",
        }
        return legacy_map.get(normalized, normalized)

    @staticmethod
    def from_row(row: dict):
        booked = row.get("booked_seat_numbers", "") or ""
        booked_list = [seat.strip().upper() for seat in booked.split(",") if seat.strip()]
        return Booking(
            id=int(row["id"]),
            user_id=int(row["user_id"]),
            show_id=int(row["show_id"]),
            booked_seat_numbers=booked_list,
            booking_date=row.get("booking_date", "") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            amount_paid=float(row.get("amount_paid", 0) or 0),
            status=row.get("status", "active") or "active",
            hold_expires_at=row.get("hold_expires_at", "") or None,
        )

    def to_row(self) -> List[str]:
        return [
            self.id,
            self.user_id,
            self.show_id,
            ",".join(self.booked_seat_numbers),
            self.booking_date,
            self.amount_paid,
            self.status,
            self.hold_expires_at or "",
        ]

