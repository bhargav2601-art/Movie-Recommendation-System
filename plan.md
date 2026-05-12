# Plan: Movie Ticket Management System - Admin & User Console

Build a console-based movie ticket booking system with:

- **Admin panel**: Revenue tracking, movie/theater management, user analytics
- **User interface**: Movie browsing (by language), city/theater selection, seat booking (max 4 tickets)
- **Data storage**: All data persisted in Excel (data.xlsx) using openpyxl library
- **Architecture**: model.py (data classes) → service.py (business logic) → main.py (console menu)

---

## Steps

### Phase 1: Data Models & Structure (model.py)

1. Define `Movie` class: id, name, language, release_date, status (active/inactive)
2. Define `Theater` class: id, name, city, total_screens
3. Define `Screen` class: id, theater_id, screen_name, total_seats, seat_layout (generate A1-J10, etc.)
4. Define `Show` class: id, screen_id, movie_id, show_time, ticket_price, booked_seats (list of seat numbers like ['A1', 'A2', 'B5'])
5. Define `User` class: id, username, email, password_hash, registration_date
6. Define `Booking` class: id, user_id, show_id, booked_seat_numbers (list), booking_date, amount_paid
7. Define `Admin` class: id, username, password_hash (for admin authentication)
8. Define `ExcelManager` helper class: methods to read/write to data.xlsx (load all sheets into memory, save all data back)
9. Add custom exception classes: `InvalidCredentials`, `DuplicateUsername`, `InvalidSeatSelection`, `InsufficientSeats`, `InvalidInput`

### Phase 2: Business Logic (service.py)

**Admin Services:**

1. `register_admin(username, password)` → Register new admin (raise DuplicateUsername, hash password)
2. `login_admin(username, password)` → Authenticate admin (raise InvalidCredentials if wrong)
3. `add_movie(name, language, release_date)` → Add new movie to system
4. `remove_movie(movie_id)` → Mark movie as inactive
5. `view_all_movies()` → List all active movies
6. `assign_movie_to_screen(movie_id, screen_id, show_time, ticket_price)` → Create shows
7. `get_revenue_total()` → Sum all ticket sales
8. `get_revenue_by_movie(movie_id)` → Revenue for specific movie
9. `get_user_statistics()` → Total users, tickets sold, bookings breakdown
10. `view_movie_in_theaters()` → Show which movies running where and when

**User Services:**

1. `register_user(username, email, password)` → User registration (raise DuplicateUsername if exists, hash password)
2. `login_user(username, password)` → Authenticate user (raise InvalidCredentials if wrong)
3. `get_available_movies()` → List all active movies with languages
4. `filter_movies_by_language(language)` → Movies in specific language
5. `get_cities_with_theaters()` → List all cities with active theaters
6. `get_theaters_in_city(city)` → Theaters in selected city
7. `get_screens_in_theater(theater_id)` → Available screens
8. `get_shows_for_screen(screen_id)` → Running shows with times
9. `get_seat_layout(screen_id)` → Available seats with layout (e.g., A1-J10)
10. `get_booked_seats(show_id)` → List of booked seat numbers
11. `validate_seat_selection(show_id, seat_numbers)` → Check if seats are available (raise InvalidSeatSelection if occupied or invalid)
12. `book_seats(user_id, show_id, seat_numbers)` → Book specific seats (max 4), create Booking record (raise exceptions for invalid inputs)

**Excel I/O Services:**

1. `load_all_data()` → Read all sheets (Movies, Theaters, Screens, Shows, Users, Bookings)
2. `save_all_data()` → Write all data back to data.xlsx

### Phase 3: Console Menu & Execution (main.py)

1. Main menu: Choose Admin or User or Exit
2. **Admin login flow** (with exception handling):
   - Try to login with username/password
   - Catch InvalidCredentials → show error, retry or go back
   - Catch InvalidInput (non-string input) → show error, retry
3. **Admin menu loop** (after successful authentication):
   - View Revenue (Total / By Movie)
   - View User Statistics
   - View Movies Running in Theaters
   - Add Movie (validate language input)
   - Remove Movie (validate movie_id)
   - Assign Movie to Screen (validate inputs, create show)
   - Back/Exit
4. **User login/registration flow** (with exception handling):
   - Option: Login or Register
   - If register: username, email, password (validate for duplicates, empty input)
   - If login: username, password (verify credentials)
   - Catch DuplicateUsername, InvalidCredentials, InvalidInput exceptions
5. **User menu loop** (after authentication):
   - Browse available movies
   - Filter by language (validate input)
   - Select city → theater → screen → show
   - View seat layout with available/booked seats (e.g., A1-J10 grid)
   - Select specific seats (max 4) (validate seat format and availability)
   - Confirm booking
   - View my bookings
   - Back/Exit
6. Comprehensive exception handling:
   - Try-except blocks for invalid input (non-integer, out-of-range selections)
   - Seat validation (InvalidSeatSelection, InsufficientSeats)
   - File I/O errors (Excel read/write failures)
   - All errors caught and user-friendly messages shown
7. Load data.xlsx on startup, save after each critical transaction

### Phase 4: Excel Structure (data.xlsx)

Create sheets:

- **Movies**: id, name, language, release_date, status
- **Theaters**: id, name, city
- **Screens**: id, theater_id, screen_name, total_seats, seat_layout (e.g., "A,B,C,...,J" for rows; 1-10 for seat numbers)
- **Shows**: id, screen_id, movie_id, show_time, ticket_price, booked_seats (comma-separated list like "A1,A2,B5")
- **Users**: id, username, email, password_hash, registration_date
- **Bookings**: id, user_id, show_id, booked_seat_numbers (comma-separated), booking_date, amount_paid
- **Admins**: id, username, password_hash

### Phase 5: Testing & Validation

1. Implement Excel reading/writing in ExcelManager (openpyxl)
2. Test data persistence (save → reload → verify)
3. Test admin authentication (correct password → access, wrong password → InvalidCredentials exception)
4. Test user authentication (registration with duplicate username → DuplicateUsername exception)
5. Test seat layout and selection:
   - Verify seat numbers generated correctly (A1-J10 for 10×10 screen)
   - Book seats and verify they appear in booked_seats list
   - Try to book already-booked seat → InvalidSeatSelection exception
   - Try to book 5 seats → InsufficientSeats exception
6. Test input validation and exception handling:
   - Invalid menu choices (non-integer input) → InvalidInput exception caught
   - Empty passwords → InvalidInput exception caught
   - Negative seat counts → InvalidInput exception caught
7. Test revenue calculation with specific seat bookings
8. Test user workflows with explicit seat selection (book A1, A2, B1 instead of just count)
9. Manual end-to-end test: Admin login → Add movie → Assign to screen → User login → Browse → Book specific seats → Verify revenue, booked seats, user statistics

---

## Relevant Files

- `model.py` — Define all 8 classes (Movie, Theater, Screen, Show, User, Booking, plus ExcelManager)
- `service.py` — Implement 20+ methods across Admin, User, and Excel I/O services
- `main.py` — Console menu loops and user interaction flow
- `data.xlsx` — Excel workbook with 6 sheets (auto-created on first run if missing)

---

## Verification

1. **Data Models Test**: Instantiate each class and confirm attributes match requirements
2. **Excel I/O Test**: Create sample data → save to data.xlsx → close program → restart → verify data persists
3. **Admin Workflow**: Add movie → assign to screen → view in theater → check revenue increments on bookings
4. **User Workflow**: Register user → browse movies → filter language → select city/theater/show → book 3 seats → confirm seats reduced, revenue increased
5. **Constraints**: Attempt to book 5 seats (should reject), remove movie while shows exist (decide: cascade or block)
6. **Manual Console Tests**: Walk through full admin and user flows end-to-end

---

## Decisions & Assumptions

- **Excel Library**: Use `openpyxl` for read/write (install: `pip install openpyxl`)
- **Password Hashing**: Use `hashlib.sha256()` for password storage (no plaintext passwords in Excel)
- **Seat Layout**: Generate seat numbers as A1-J10 for 10-row × 10-column standard theater screen
- **Seat Selection**: Users select specific seats (e.g., A1, A2, B5) instead of just a count
- **Data Hierarchy**: City → Theater → Screen → Show (Movie scheduled on screen at specific time)
- **Booking Limit**: Hard limit of 4 seats per transaction (enforced in validation with exception)
- **Movie Status**: Soft delete via `status` field (inactive) rather than hard delete
- **Admin Authentication**: Required username + password on every admin login
- **User Authentication**: Required username + email + password for registration; username + password for login
- **Revenue Calculation**: sum(num_seats × ticket_price) for all completed bookings
- **Auto-Initialization**: If data.xlsx missing, create with sample data (2 movies, 2 cities, 3 theaters, 2 screens each, 1 default admin)
- **Exception Handling**: All exceptions caught at UI level (main.py) with user-friendly error messages; never let raw exceptions reach user

---

## Further Considerations (ALL ADDRESSED)

✅ **Show Scheduling**: Should a show automatically end after a certain date?

- Decision: Add `show_end_date` field to Shows sheet and filter inactive shows in queries

✅ **Seat Layout**: Implement seat numbers (A1, A2, B1, etc.) for detailed seat selection

- Decision: Generate A1-J10 (10 rows × 10 seats) per screen; store booked seats as comma-separated list in Excel

✅ **User Authentication**: Users need passwords on return visits

- Decision: Add `password_hash` to Users table; implement login_user(username, password) service

✅ **Admin Authentication**: Admin needs password on return visits

- Decision: Create separate Admins table with username & password_hash; implement login_admin(username, password) service

✅ **Exception Handling**: Comprehensive error handling for invalid inputs, users, admins, and seat selection

- Decision: Define 5 custom exceptions (InvalidCredentials, DuplicateUsername, InvalidSeatSelection, InsufficientSeats, InvalidInput)
- All exceptions caught in main.py with user-friendly error messages
- Validation happens at service layer; exceptions raised and caught at UI layer
