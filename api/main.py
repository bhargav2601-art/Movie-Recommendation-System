from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from collections import Counter
from functools import wraps
from typing import Callable, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from api.catalog import build_movie_metadata, build_theater_profile, infer_screen_formats, price_modifiers
from api.schemas import (
    AuthRequest,
    AuthResponse,
    BookingRequest,
    MovieCreateRequest,
    ScreenCreateRequest,
    ShowCreateRequest,
    SignupRequest,
    TheaterCreateRequest,
    UserPayload,
)
from model import DuplicateUsername, InvalidCredentials, InvalidInput, InvalidSeatSelection, InsufficientSeats
from service import TicketService

service = TicketService(data_path=os.getenv("MOVIE_APP_DATA", "data.xlsx"))
app = FastAPI(title="CineVerse API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = os.getenv("MOVIE_APP_SECRET", "ciniverse-demo-secret")


def dedupe_movies_by_title(movies: list[dict]) -> list[dict]:
    deduped: dict[str, dict] = {}
    for movie in movies:
        existing = deduped.get(movie["title"])
        if existing is None or (movie["showCount"], movie["rating"], movie["imdbScore"]) > (
            existing["showCount"],
            existing["rating"],
            existing["imdbScore"],
        ):
            deduped[movie["title"]] = movie
    return list(deduped.values())


def create_token(payload: dict) -> str:
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    signature = hmac.new(SECRET.encode(), encoded_payload.encode(), hashlib.sha256).hexdigest()
    return f"{encoded_payload}.{signature}"


def decode_token(token: str) -> dict:
    try:
        encoded_payload, signature = token.split(".", 1)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid authorization token.") from exc
    expected = hmac.new(SECRET.encode(), encoded_payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=401, detail="Invalid authorization token.")
    try:
        return json.loads(base64.urlsafe_b64decode(encoded_payload.encode()).decode())
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="Malformed authorization token.") from exc


def parse_auth_header(authorization: Optional[str]) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is required.")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Use Bearer token authentication.")
    return decode_token(token)


def get_current_user(authorization: Optional[str] = Header(default=None)) -> dict:
    return parse_auth_header(authorization)


def require_role(role: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            if current_user.get("role") != role:
                raise HTTPException(status_code=403, detail="You do not have access to this resource.")
            return func(*args, current_user=current_user, **kwargs)

        return wrapper

    return decorator


def serialize_movie(movie):
    metadata = build_movie_metadata(movie.name)
    cities = service.get_movie_cities(movie.id)
    shows = [show for show in service.get_available_shows() if show.movie_id == movie.id]
    upcoming = metadata.get("comingSoon", False)
    return {
        "id": movie.id,
        "title": metadata["title"],
        "language": [item.strip().title() for item in movie.language.split(",") if item.strip()],
        "releaseDate": movie.release_date,
        "status": movie.status,
        "cities": cities,
        "genre": metadata["genre"],
        "duration": metadata["duration"],
        "rating": metadata["rating"],
        "certificate": metadata["certificate"],
        "storyline": metadata["storyline"],
        "cast": metadata["cast"],
        "poster": metadata["poster"],
        "backdrop": metadata["backdrop"],
        "logo": metadata["logo"],
        "gallery": metadata["gallery"],
        "castImages": metadata["castImages"],
        "trailerUrl": metadata["trailer_url"],
        "trailerWatchUrl": metadata["trailer_watch_url"],
        "trailer": metadata["trailer_watch_url"],
        "trailerThumbnail": metadata["trailer_thumbnail"],
        "trailerVariants": metadata["trailer_variants"],
        "trailerAvailable": metadata["trailer_available"],
        "trailerCta": metadata["trailer_cta"],
        "isPlaceholder": metadata["is_placeholder"],
        "mood": metadata["mood"],
        "runtimeMinutes": metadata["runtimeMinutes"],
        "imdbScore": metadata["imdbScore"],
        "rottenTomatoes": metadata["rottenTomatoes"],
        "subtitles": metadata["subtitles"],
        "languages": metadata["languages"],
        "trendingBadge": metadata["trendingBadge"],
        "heroTag": metadata["heroTag"],
        "whyRecommended": metadata["whyRecommended"],
        "comingSoon": upcoming,
        "categories": metadata["categories"],
        "palette": metadata["palette"],
        "shows": [
            {
                "id": show.id,
                "showTime": show.show_time,
                "ticketPrice": show.ticket_price,
                "theaterName": service.get_theater(service.get_screen(show.screen_id).theater_id).name,
            }
            for show in shows[:4]
        ],
        "showCount": len(shows),
    }


def serialize_show(show):
    movie = service.get_movie(show.movie_id)
    screen = service.get_screen(show.screen_id)
    theater = service.get_theater(screen.theater_id)
    formats = infer_screen_formats(screen.screen_name)
    modifiers = price_modifiers(screen.screen_name)
    booked_seats = service.get_booked_seats_for_show(show.id)
    start_at = service._parse_show_start(show)
    end_at = service._parse_show_end(show)
    return {
        "id": show.id,
        "movieId": movie.id,
        "movieTitle": movie.name.upper(),
        "showDate": show.show_date,
        "showTime": show.show_time,
        "endTime": show.end_time,
        "startAt": start_at.strftime("%Y-%m-%d %H:%M:%S"),
        "endAt": end_at.strftime("%Y-%m-%d %H:%M:%S"),
        "ticketPrice": show.ticket_price,
        "pricing": {
            "base": show.ticket_price,
            "weekend": round(show.ticket_price * modifiers["weekend"], 2),
            "premiumSeat": round(show.ticket_price * modifiers["premiumSeat"], 2),
            "largeFormat": round(show.ticket_price * modifiers["imax"], 2),
        },
        "bookedSeats": booked_seats,
        "availableSeats": max(0, screen.total_seats - len(booked_seats)),
        "occupancyPercent": round((len(booked_seats) / max(1, screen.total_seats)) * 100, 1),
        "status": "completed" if end_at <= service._current_time() else "scheduled",
        "screen": {
            "id": screen.id,
            "name": screen.screen_name,
            "totalSeats": screen.total_seats,
            "seatRows": screen.seat_rows,
            "seatsPerRow": screen.seats_per_row,
            "formats": formats,
        },
        "theater": {
            "id": theater.id,
            "name": theater.name,
            "city": theater.city,
        },
    }


def serialize_booking(booking):
    show = service.get_show(booking.show_id)
    screen = service.get_screen(show.screen_id)
    theater = service.get_theater(screen.theater_id)
    movie = service.get_movie(show.movie_id)
    return {
        "id": booking.id,
        "bookingDate": booking.booking_date,
        "amountPaid": booking.amount_paid,
        "seatNumbers": booking.booked_seat_numbers,
        "status": booking.status,
        "showId": show.id,
        "showDate": show.show_date,
        "startTime": show.show_time,
        "endTime": show.end_time,
        "show": serialize_show(show),
        "movie": serialize_movie(movie),
        "ticket": {
            "theater": theater.name,
            "city": theater.city,
            "screen": screen.screen_name,
            "showTime": show.show_time,
        },
    }


@app.get("/api/health")
def health_check():
    service.cleanup_expired_bookings()
    return {"status": "ok"}


@app.post("/api/auth/signup", response_model=AuthResponse)
def signup(payload: SignupRequest):
    try:
        user = service.register_user(payload.username, payload.email, payload.password)
    except DuplicateUsername as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except InvalidInput as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    token = create_token({"id": user.id, "username": user.username, "role": "user", "email": user.email})
    return {"token": token, "user": UserPayload(id=user.id, username=user.username, email=user.email, role="user")}


@app.post("/api/auth/login", response_model=AuthResponse)
def login(payload: AuthRequest):
    return login_user(payload)


@app.post("/api/auth/login/user", response_model=AuthResponse)
def login_user(payload: AuthRequest):
    try:
        user = service.login_user(payload.username, payload.password)
        token = create_token({"id": user.id, "username": user.username, "role": "user", "email": user.email})
        return {"token": token, "user": UserPayload(id=user.id, username=user.username, email=user.email, role="user")}
    except InvalidCredentials as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except InvalidInput as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/auth/login/admin", response_model=AuthResponse)
def login_admin(payload: AuthRequest):
    try:
        admin = service.login_admin(payload.username, payload.password)
        token = create_token({"id": admin.id, "username": admin.username, "role": "admin"})
        return {"token": token, "user": UserPayload(id=admin.id, username=admin.username, role="admin")}
    except InvalidCredentials as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except InvalidInput as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/auth/logout")
def logout():
    return {"message": "Logged out successfully."}


@app.get("/api/movies")
def get_movies(
    search: str = "",
    genre: str = "",
    language: str = "",
    city: str = "",
    sort: str = "trending",
):
    movies = [serialize_movie(movie) for movie in service.get_active_movies()]
    if search:
        normalized = search.strip().lower()
        movies = [movie for movie in movies if normalized in movie["title"].lower()]
    if genre:
        normalized = genre.strip().lower()
        movies = [movie for movie in movies if any(normalized == item.lower() for item in movie["genre"])]
    if language:
        normalized = language.strip().lower()
        movies = [movie for movie in movies if any(normalized == item.lower() for item in movie["language"])]
    if city:
        normalized = city.strip().lower()
        movies = [movie for movie in movies if any(normalized == item.lower() for item in movie["cities"])]
    movies = dedupe_movies_by_title(movies)

    if sort == "rating":
        movies.sort(key=lambda item: item["rating"], reverse=True)
    elif sort == "release":
        movies.sort(key=lambda item: item["releaseDate"], reverse=True)
    else:
        movies.sort(key=lambda item: (item["showCount"], item["rating"]), reverse=True)

    return {"items": movies}


@app.get("/api/movies/recommendations")
def get_recommendations(city: str = ""):
    movies = get_movies(city=city)["items"]
    ranked = sorted(movies, key=lambda item: (item["rating"], item["showCount"]), reverse=True)
    def pick(items, limit=12):
        return items[:limit]

    def by_category(name, limit=12):
        return pick([movie for movie in ranked if name in movie.get("categories", [])], limit)

    return {
        "hero": ranked[:5],
        "trending": pick(ranked, 12),
        "recommended": pick(sorted(ranked, key=lambda item: (item["rating"] + item["imdbScore"]), reverse=True), 12),
        "topRated": pick(sorted(ranked, key=lambda item: item["imdbScore"], reverse=True), 12),
        "trendingInCity": pick([movie for movie in ranked if (not city or city in movie["cities"])], 12),
        "scifi": by_category("Sci-Fi"),
        "action": by_category("Action"),
        "romance": by_category("Romance"),
        "horror": by_category("Horror"),
        "comingSoon": pick([movie for movie in ranked if movie["comingSoon"]], 12),
        "imaxExperience": by_category("IMAX Experience"),
        "familyMovies": by_category("Family Movies"),
    }


@app.get("/api/movies/meta")
def get_movie_meta():
    movies = dedupe_movies_by_title([serialize_movie(movie) for movie in service.get_active_movies()])
    genres = sorted({genre for movie in movies for genre in movie["genre"]})
    languages = sorted({language for movie in movies for language in movie["language"]})
    cities = service.get_cities_with_theaters()
    return {
        "genres": genres,
        "languages": languages,
        "cities": cities,
        "formats": sorted({fmt for show in service.shows for fmt in infer_screen_formats(service.get_screen(show.screen_id).screen_name)}),
    }


@app.get("/api/movies/{movie_id}")
def get_movie_details(movie_id: int):
    movie = service.get_movie(movie_id)
    payload = serialize_movie(movie)
    movie_shows = [show for show in service.get_available_shows() if show.movie_id == movie_id]
    payload["shows"] = [serialize_show(show) for show in movie_shows]
    theaters = []
    for theater in service.theaters:
        screens = [screen for screen in service.screens if screen.theater_id == theater.id]
        theater_shows = [show for show in movie_shows if any(screen.id == show.screen_id for screen in screens)]
        if not theater_shows:
            continue
        profile = build_theater_profile(theater, screens, theater_shows)
        profile["screensList"] = [
            {
                "screenName": screen.screen_name,
                "seatLayout": {"rows": screen.seat_rows, "seatsPerRow": screen.seats_per_row, "capacity": screen.total_seats},
                "formats": infer_screen_formats(screen.screen_name),
                "timings": [
                    {
                        "showId": show.id,
                        "showDate": show.show_date,
                        "showTime": show.show_time,
                        "endTime": show.end_time,
                    }
                    for show in theater_shows
                    if show.screen_id == screen.id
                ],
                "pricing": [serialize_show(show)["pricing"] for show in theater_shows if show.screen_id == screen.id],
            }
            for screen in screens
            if any(show.screen_id == screen.id for show in theater_shows)
        ]
        theaters.append(profile)
    payload["theaters"] = sorted(theaters, key=lambda item: item["distance"])
    similar = [
        serialize_movie(candidate)
        for candidate in service.get_active_movies()
        if candidate.id != movie.id
    ]
    payload["similar"] = sorted(
        dedupe_movies_by_title(similar),
        key=lambda item: (
            len(set(item["genre"]).intersection(payload["genre"])),
            item["imdbScore"],
            item["rating"],
        ),
        reverse=True,
    )[:8]
    return payload


@app.get("/api/shows/{show_id}/seats")
def get_show_seats(show_id: int):
    show = service.get_show(show_id)
    screen = service.get_screen(show.screen_id)
    movie = service.get_movie(show.movie_id)
    metadata = build_movie_metadata(movie.name)
    booked_seats = set(service.get_booked_seats_for_show(show.id))
    all_seats = screen.get_seat_ids()
    premium_rows = {seat[0] for seat in all_seats[: max(1, len(all_seats) // 5)]}
    seats = []
    for seat in all_seats:
        row = seat[0]
        seats.append(
            {
                "id": seat,
                "row": row,
                "number": int(seat[1:]),
                "type": "premium" if row in premium_rows else "regular",
                "status": "booked" if seat in booked_seats else "available",
            }
        )
    return {
        "show": serialize_show(show),
        "pricing": {
            "basePrice": show.ticket_price,
            "premiumSurcharge": round(show.ticket_price * 0.25, 2),
            "weekendPrice": round(show.ticket_price * price_modifiers(screen.screen_name)["weekend"], 2),
        },
        "seats": seats,
        "foodCombos": metadata["foodCombos"],
        "coupons": metadata["coupons"],
        "paymentMethods": metadata["paymentMethods"],
        "experienceModes": ["Normal", "Wide", "IMAX"],
        "countdownSeconds": 600,
    }


@app.post("/api/bookings")
def create_booking(payload: BookingRequest, current_user=Depends(get_current_user)):
    if current_user.get("role") != "user":
        raise HTTPException(status_code=403, detail="Only users can create bookings.")
    try:
        booking = service.book_seats(current_user["id"], payload.show_id, payload.seat_numbers)
        return serialize_booking(booking)
    except (InvalidInput, InvalidSeatSelection, InsufficientSeats) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/bookings/me")
def get_my_bookings(current_user=Depends(get_current_user)):
    if current_user.get("role") != "user":
        raise HTTPException(status_code=403, detail="Only users can view booking history.")
    bookings = [serialize_booking(booking) for booking in service.get_user_bookings(current_user["id"])]
    return {"items": list(reversed(bookings))}


@app.get("/api/admin/analytics")
def get_admin_analytics(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    stats = service.get_user_statistics()
    revenue_by_movie = []
    movie_sales = Counter()
    for movie in service.get_active_movies():
        revenue = service.get_revenue_by_movie(movie.id)
        seats_sold = sum(
            len(booking.booked_seat_numbers)
            for booking in service.bookings
            if service.get_show(booking.show_id).movie_id == movie.id and booking.status in {"active", "completed"}
        )
        movie_sales[movie.name] = seats_sold
        revenue_by_movie.append({"movie": movie.name, "revenue": revenue, "tickets": seats_sold})

    recent_bookings = [serialize_booking(booking) for booking in service.bookings[-8:]][::-1]
    occupancy_by_movie = []
    for movie in service.get_active_movies():
        movie_shows = [show for show in service.get_available_shows() if show.movie_id == movie.id]
        total_capacity = sum(service.get_screen(show.screen_id).total_seats for show in movie_shows) or 1
        total_booked = sum(len(service.get_booked_seats_for_show(show.id)) for show in movie_shows)
        occupancy_by_movie.append({"movie": movie.name, "occupancy": round((total_booked / total_capacity) * 100, 1)})

    booking_heatmap = []
    hour_slots = ["09:00", "12:00", "15:00", "18:00", "21:00"]
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for weekday_index, day in enumerate(weekdays):
        for slot_index, hour in enumerate(hour_slots):
            booking_heatmap.append(
                {
                    "day": day,
                    "hour": hour,
                    "value": ((weekday_index + 2) * (slot_index + 3) * 7) % 100,
                }
            )
    return {
        "overview": {
            "revenue": service.get_revenue_total(),
            "activeMovies": len(service.get_active_movies()),
            "theaters": len(service.theaters),
            "screens": len(service.screens),
            "shows": len(service.shows),
            **stats,
        },
        "revenueByMovie": revenue_by_movie,
        "occupancyByMovie": occupancy_by_movie,
        "cityPerformance": [
            {
                "city": city,
                "shows": len(
                    [
                        show
                        for show in service.get_available_shows()
                        if service.get_theater(service.get_screen(show.screen_id).theater_id).city == city
                    ]
                ),
            }
            for city in service.get_cities_with_theaters()
        ],
        "bookingHeatmap": booking_heatmap,
        "recentBookings": recent_bookings,
        "activeUsers": [{"name": user.username, "joined": user.registration_date} for user in service.users[-8:]][::-1],
        "topSellingMovie": movie_sales.most_common(1)[0][0] if movie_sales else None,
        "realTimeStats": {
            "liveUsers": max(24, len(service.users) * 3),
            "liveBookings": max(14, len(service.bookings) + 9),
            "occupancyRate": round(sum(item["occupancy"] for item in occupancy_by_movie) / max(1, len(occupancy_by_movie)), 1),
        },
    }


@app.get("/api/admin/movies")
def get_admin_movies(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return {"items": [serialize_movie(movie) for movie in service.movies]}


@app.post("/api/admin/movies")
def create_movie(payload: MovieCreateRequest, current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    try:
        service.add_movie(payload.name, payload.language, payload.release_date)
        created = service.movies[-1]
        return serialize_movie(created)
    except InvalidInput as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/api/admin/movies/{movie_id}")
def delete_movie(movie_id: int, current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    try:
        service.remove_movie(movie_id)
        return {"message": "Movie archived successfully."}
    except InvalidInput as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/admin/theaters")
def create_theater(payload: TheaterCreateRequest, current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    try:
        theater = service.add_theater(payload.name, payload.city)
        return {"id": theater.id, "name": theater.name, "city": theater.city}
    except InvalidInput as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/admin/screens")
def create_screen(payload: ScreenCreateRequest, current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    try:
        screen = service.add_screen(
            payload.theater_id,
            payload.screen_name,
            payload.total_seats,
            payload.seat_rows,
            payload.seats_per_row,
        )
        return {
            "id": screen.id,
            "theaterId": screen.theater_id,
            "name": screen.screen_name,
            "totalSeats": screen.total_seats,
        }
    except InvalidInput as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/admin/shows")
def create_show(payload: ShowCreateRequest, current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    try:
        service.assign_movie_to_screen(payload.movie_id, payload.screen_id, payload.show_time, payload.ticket_price, payload.show_date)
        show = service.shows[-1]
        return serialize_show(show)
    except InvalidInput as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/admin/catalog")
def get_admin_catalog(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return {
        "theaters": [
            build_theater_profile(
                theater,
                [screen for screen in service.screens if screen.theater_id == theater.id],
                [show for show in service.get_available_shows() if service.get_screen(show.screen_id).theater_id == theater.id],
            )
            for theater in service.theaters
        ],
        "screens": [
            {
                "id": screen.id,
                "name": screen.screen_name,
                "theaterId": screen.theater_id,
                "totalSeats": screen.total_seats,
                "formats": infer_screen_formats(screen.screen_name),
            }
            for screen in service.screens
        ],
        "shows": [serialize_show(show) for show in service.get_available_shows()],
    }


@app.get("/api/search/suggestions")
def get_search_suggestions(q: str = Query(default="")):
    query = q.strip().lower()
    titles = list(dict.fromkeys(movie.name for movie in service.get_active_movies()))
    if not query:
        return {"items": titles[:6]}
    return {"items": [title for title in titles if query in title.lower()][:8]}
