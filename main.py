from service import (
    TicketService,
    InvalidCredentials,
    DuplicateUsername,
    InvalidInput,
    InvalidSeatSelection,
    InsufficientSeats,
)
import getpass
def prompt_password(prompt_text: str) -> str:
    try:
        return getpass.getpass(prompt_text)
    except Exception:
        return input(prompt_text)
def format_seat_grid(screen, booked_seats):
    seat_ids = screen.get_seat_ids()
    rows = screen.seat_rows
    cols = screen.seats_per_row
    grid_lines = []
    for row_index in range(rows):
        row_letter = chr(65 + row_index)
        row_values = []
        for col in range(1, cols + 1):
            seat_id = f"{row_letter}{col}"
            if seat_id not in seat_ids:
                row_values.append("  ")
            elif seat_id in booked_seats:
                row_values.append("XX")
            else:
                row_values.append(seat_id)
        grid_lines.append(" ".join(row_values))
    return "\n".join(grid_lines)


def admin_menu(service: TicketService):
    while True:
        print("\n--- Admin Menu ---")
        print("1. View total revenue")
        print("2. View revenue by movie")
        print("3. View movies running in theaters")
        print("4. Add movie")
        print("5. Remove movie")
        print("6. Add new theater")
        print("7. Add new screen")
        print("8. Assign movie to screen")
        print("9. Back")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            print(f"Total revenue: ₹{service.get_revenue_total():.2f}")

        elif choice == "2":
            movies = service.get_active_movies()
            for movie in movies:
                print(f"{movie.id}. {movie.name} ({movie.language})")
            movie_id = input("Enter movie ID for revenue details: ").strip()
            try:
                movie_id = int(movie_id)
                revenue = service.get_revenue_by_movie(movie_id)
                print(f"Revenue for movie {movie_id}: ₹{revenue:.2f}")
            except ValueError:
                print("Invalid movie ID. Please type a number.")

        elif choice == "3":
            schedule = service.view_movie_in_theaters()
            if not schedule:
                print("No movies currently assigned to screens.")
            for item in schedule:
                print(
                    f"Show ID {item['show_id']}: {item['movie_name']} at {item['theater_name']} / {item['screen_name']} "
                    f"({item['city']}) on {item['show_time']} | Price: ₹{item['ticket_price']:.2f}"
                )

        elif choice == "4":
            try:
                name = input("Movie name: ").strip()
                language = input("Language: ").strip()
                release_date = input("Release date (YYYY-MM-DD): ").strip()
                service.add_movie(name, language, release_date)
                print("Movie added successfully.")
            except InvalidInput as exc:
                print(f"Error: {exc}")

        elif choice == "5":
            try:
                movies = service.get_active_movies()
                for movie in movies:
                    print(f"{movie.id}. {movie.name} ({movie.language})")
                movie_id = int(input("Enter ID of movie to remove: ").strip())
                service.remove_movie(movie_id)
                print("Movie removed successfully.")
            except ValueError:
                print("Movie ID must be a number.")
            except InvalidInput as exc:
                print(f"Error: {exc}")

        elif choice == "6":
            try:
                city = input("City for new theater: ").strip()
                theater_name = input("Theater name: ").strip()
                theater = service.add_theater(theater_name, city)
                print(f"Theater '{theater.name}' added successfully in {theater.city}.")
            except InvalidInput as exc:
                print(f"Error: {exc}")

        elif choice == "7":
            try:
                theaters = service.get_cities_with_theaters()
                if not theaters:
                    print("No theaters available to add a screen.")
                    continue
                print("Cities with theaters:")
                for city in theaters:
                    print(f"- {city}")
                city = input("Enter city for the new screen: ").strip()
                selected_theaters = service.get_theaters_in_city(city)
                if not selected_theaters:
                    print("No theaters found in that city.")
                    continue
                print("Theaters:")
                for theater in selected_theaters:
                    print(f"{theater.id}. {theater.name}")
                theater_id = int(input("Select theater ID: ").strip())
                screen_name = input("Screen name: ").strip()
                total_seats = int(input("Total seats: ").strip())
                seat_rows = int(input("Rows (e.g. 10): ").strip())
                seats_per_row = int(input("Seats per row (e.g. 10): ").strip())
                service.add_screen(theater_id, screen_name, total_seats, seat_rows, seats_per_row)
                print("Screen added successfully.")
            except ValueError:
                print("Numeric values required for theater ID, total seats, rows, and seats per row.")
            except InvalidInput as exc:
                print(f"Error: {exc}")

        elif choice == "8":
            try:
                movies = service.get_active_movies()
                screens = service.get_all_screens()
                if not movies:
                    print("No active movies available to assign.")
                    continue
                if not screens:
                    print("No screens available.")
                    continue
                print("Movies:")
                for movie in movies:
                    print(f"{movie.id}. {movie.name} ({movie.language})")
                print("Screens:")
                for screen in screens:
                    theater = service.get_theater(screen.theater_id)
                    print(f"{screen.id}. {screen.screen_name} at {theater.name} ({theater.city})")
                movie_id = int(input("Movie ID: ").strip())
                screen_id = int(input("Screen ID: ").strip())
                show_time = input("Show time (e.g. 19:00): ").strip()
                ticket_price = float(input("Ticket price: ").strip())
                service.assign_movie_to_screen(movie_id, screen_id, show_time, ticket_price)
                print("Movie assigned to screen successfully.")
            except ValueError:
                print("Numeric values required for IDs and ticket price.")
            except InvalidInput as exc:
                print(f"Error: {exc}")

        elif choice == "9":
            break
        else:
            print("Please choose a valid option.")


def user_menu(service: TicketService, user):
    while True:
        print("\n--- User Menu ---")
        print("1. Browse available movies")
        print("2. Filter movies by language")
        print("3. Book tickets")
        print("4. View my bookings")
        print("5. Back")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            movies = service.get_active_movies()
            if not movies:
                print("No movies are available right now.")
            for movie in movies:
                cities = service.get_movie_cities(movie.id)
                city_label = ", ".join(cities) if cities else "Not running in any city"
                print(f"{movie.id}. {movie.name} ({movie.language}) | Cities: {city_label}")

        elif choice == "2":
            languages = service.get_available_languages()
            if not languages:
                print("No available languages at the moment.")
            else:
                print("Available languages:")
                print(", ".join(languages))
            language = input("Enter language to filter: ").strip()
            filtered = service.filter_movies_by_language(language)
            if not filtered:
                print("No movies found for that language.")
            for movie in filtered:
                cities = service.get_movie_cities(movie.id)
                city_label = ", ".join(cities) if cities else "Not running in any city"
                print(f"{movie.id}. {movie.name} ({movie.language}) | Cities: {city_label}")

        elif choice == "3":
            try:
                city = input("Enter city: ").strip()
                theaters = service.get_theaters_in_city(city)
                if not theaters:
                    print("No theaters found in that city.")
                    continue
                print("Theaters in city:")
                for theater in theaters:
                    print(f"{theater.id}. {theater.name}")
                theater_id = int(input("Select theater ID: ").strip())
                screens = service.get_screens_in_theater(theater_id)
                if not screens:
                    print("No screens found for that theater.")
                    continue
                print("Screens:")
                for screen in screens:
                    print(f"{screen.id}. {screen.screen_name}")
                screen_id = int(input("Select screen ID: ").strip())
                shows = service.get_shows_for_screen(screen_id)
                if not shows:
                    print("No shows available for this screen.")
                    continue
                print("Shows:")
                for show in shows:
                    movie = service.get_movie(show.movie_id)
                    print(f"{show.id}. {movie.name} at {show.show_time} | ₹{show.ticket_price:.2f}")
                show_id = int(input("Select show ID: ").strip())
                show = service.get_show(show_id)
                screen = service.get_screen(show.screen_id)
                seat_layout = format_seat_grid(screen, service.get_booked_seats_for_show(show.id))
                print("\nSeat map (XX = booked):")
                print(seat_layout)
                seats_text = input(
                    "Enter seat numbers separated by commas (max 4 seats, e.g. A1,A2): "
                ).strip()
                seat_numbers = [seat.strip().upper() for seat in seats_text.split(",") if seat.strip()]
                if not seat_numbers:
                    print("No seat selection provided.")
                    continue
                booking = service.book_seats(user.id, show_id, seat_numbers)
                print(
                    f"Booking confirmed. Seats {', '.join(booking.booked_seat_numbers)} booked for ₹{booking.amount_paid:.2f}."
                )
            except ValueError:
                print("Numeric values required for theater/screen/show selection.")
            except (InvalidInput, InvalidSeatSelection, InsufficientSeats) as exc:
                print(f"Error: {exc}")

        elif choice == "4":
            bookings = service.get_user_bookings(user.id)
            if not bookings:
                print("You have no bookings yet.")
                continue
            for booking in bookings:
                show = service.get_show(booking.show_id)
                movie = service.get_movie(show.movie_id)
                theater = service.get_theater(service.get_screen(show.screen_id).theater_id)
                print(
                    f"Booking {booking.id}: {movie.name} at {theater.name} "
                    f"on {show.show_time} seats {', '.join(booking.booked_seat_numbers)} "
                    f"| ₹{booking.amount_paid:.2f}"
                )

        elif choice == "5":
            break
        else:
            print("Please choose a valid option.")


def admin_access(service: TicketService):
    print("\n--- Admin Login ---")
    username = input("Username: ").strip()
    password = prompt_password("Password: ")
    try:
        service.login_admin(username, password)
        print("Admin login successful.")
        admin_menu(service)
    except (InvalidCredentials, InvalidInput) as exc:
        print(f"Login failed: {exc}")


def user_access(service: TicketService):
    while True:
        print("\n--- User Portal ---")
        print("1. Login")
        print("2. Register")
        print("3. Back")
        choice = input("Choose an action: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = prompt_password("Password: ")
            try:
                user = service.login_user(username, password)
                print("Login successful.")
                user_menu(service, user)
            except (InvalidCredentials, InvalidInput) as exc:
                print(f"Login failed: {exc}")

        elif choice == "2":
            try:
                username = input("Choose username: ").strip()
                email = input("Email: ").strip()
                password = prompt_password("Choose password: ")
                user = service.register_user(username, email, password)
                print(f"Registration successful. Welcome, {user.username}!")
                user_menu(service, user)
            except (DuplicateUsername, InvalidInput) as exc:
                print(f"Registration failed: {exc}")

        elif choice == "3":
            break
        else:
            print("Please choose a valid option.")


def main():
    service = TicketService()
    print("Welcome to Movie Ticket Booking System")
    while True:
        print("\n--- Main Menu ---")
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        option = input("Choose an option: ").strip()
        if option == "1":
            admin_access(service)
        elif option == "2":
            user_access(service)
        elif option == "3":
            print("Thank you for visiting our movie booking system. Come back soon for another great show!")
            break
        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()
