from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class SignupRequest(AuthRequest):
    email: str


class MovieCreateRequest(BaseModel):
    name: str
    language: str
    release_date: str


class TheaterCreateRequest(BaseModel):
    name: str
    city: str


class ScreenCreateRequest(BaseModel):
    theater_id: int
    screen_name: str
    total_seats: int = Field(default=100, gt=0)
    seat_rows: int = Field(default=10, gt=0)
    seats_per_row: int = Field(default=10, gt=0)


class ShowCreateRequest(BaseModel):
    movie_id: int
    screen_id: int
    show_date: Optional[str] = None
    show_time: str
    ticket_price: float = Field(gt=0)


class BookingRequest(BaseModel):
    show_id: int
    seat_numbers: List[str] = Field(min_length=1, max_length=4)


class UserPayload(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str


class AuthResponse(BaseModel):
    token: str
    user: UserPayload
