# Movie Recommendation System

A full-stack movie discovery and ticket-booking project with a FastAPI backend, a React + Vite frontend, and Excel-based persistence.

The app includes movie browsing, theater discovery, real-time seat selection, booking confirmation, user authentication, and an admin dashboard for managing catalog and show data.

## Tech Stack

- Backend: FastAPI, Python
- Frontend: React, Vite, Tailwind CSS
- Storage: Excel workbook via `openpyxl`
- HTTP client: Axios

## Features

- Browse movies with rich metadata, trailers, and themed detail pages
- Discover theaters and shows by city
- Select seats with live availability and booking limits
- Preview seat perspective in the booking flow
- User signup/login and booking history
- Admin login and dashboard for operational insights
- Excel-backed data storage with default bootstrap records

## Project Structure

```text
.
|-- api/
|   |-- main.py
|   |-- schemas.py
|   `-- catalog.py
|-- frontend/
|   |-- src/
|   |-- public/
|   `-- package.json
|-- model.py
|-- service.py
|-- main.py
|-- app.py
|-- data.xlsx
`-- plan.md
```

## Backend

The backend entrypoint is `app.py`, which exposes the FastAPI app from `api/main.py`.

Important environment variables:

- `MOVIE_APP_DATA`: path to the Excel workbook. Defaults to `data.xlsx`
- `MOVIE_APP_SECRET`: secret used for token signing

Install backend dependencies:

```bash
pip install fastapi uvicorn openpyxl
```

Run the backend:

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Frontend

Install frontend dependencies:

```bash
cd frontend
npm install
```

Run the frontend:

```bash
npm run dev
```

By default, the frontend runs at `http://127.0.0.1:5173` and talks to:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Authentication

The service bootstraps a default admin account if none exists:

- Username: `admin`
- Password: `admin123`

## Data Storage

Application data is stored in `data.xlsx`. The workbook contains sheets for:

- Movies
- Theaters
- Screens
- Shows
- Users
- Bookings
- Admins

If the workbook is missing, the service initializes the required sheets and default seed data on startup.

## Console Mode

This repository also includes a console-based workflow in `main.py` for admin and user ticket-booking flows.

Run it with:

```bash
python main.py
```

## Notes

- The frontend `README.md` inside `frontend/` is the default Vite template and can be replaced later with project-specific frontend documentation if needed.
- Excel is used here as a lightweight persistence layer for local development and demos.
