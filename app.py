import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Add New User.
7) Search movie.
8) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()


def add_movie():
    """Add a new movie to the database."""
    title = input("Enter the movie title: ")
    release_date = input("Enter the release date (dd-mm-YYYY): ")

    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    release_timestamp = parsed_date.timestamp()

    response = database.add_movie(title, release_timestamp)
    print(response)


def add_user():
    """Add a new user to the database."""
    username = input("Enter the username: ")
    response = database.add_user(username)
    print(response)


def print_movies_list(heading, movies_list):
    """Print a list of movies with a specific heading."""
    print(f"\n-----{heading} Movies!-----\n")
    for _id, title, release_date in movies_list:
        dateTime = datetime.datetime.fromtimestamp(release_date)
        date = dateTime.strftime("%b %d %Y")
        print(f"{title} (Released on {date}, and the id is {_id})\n")
        print("---------\n")


def watch_movie():
    """Watch a movie by updating the watched table."""
    username = input("Username: ")
    movie_id = input("Enter the id of watched movie: ")
    database.watch_movie(username, movie_id)


def search_movies():
    """Search for movies based on the title."""
    pattern = input("Enter the title of the movie: ")
    movies_list = database.search_movies(pattern)
    if movies_list:
        print_movies_list("Found", movies_list)
    else:
        print("Found no movies :(")


while (user_input := input(menu)) != "8":

    if user_input == "1":
        add_movie()

    elif user_input == "2":
        movies_list, response = database.get_movies(True)

        if response != "OK":
            print(response)
        elif movies_list:
            print_movies_list("Upcoming", movies_list)
        else:
            print("\nNo upcoming movies :(\n")

    elif user_input == "3":
        movies_list, response = database.get_movies()
        if response != "OK":
            print(response)
        elif movies_list:
            print_movies_list("All", movies_list)
        else:
            print("No Movies available :(")

    elif user_input == "4":
        watch_movie()

    elif user_input == "5":
        username = input("Username: ")

        movies_list, response = database.get_watched_movies(username)
        if response != "OK":
            print(response)
        elif movies_list:
            print_movies_list(f"{username}'s Watched", movies_list)
        else:
            print(f"\n{username} has watched no movies yet!")

    elif user_input == "6":
        add_user()

    elif user_input == "7":
        search_movies()

    else:
        print("Invalid input, please try again!")
