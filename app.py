import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()


def add_movie():
    title = input("Enter the movie title: ")
    release_date = input("Enter the release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    release_timestamp = parsed_date.timestamp()
    database.add_movie(title, release_timestamp)


def print_movies_list(heading, movies_list):
    print(f"-----{heading} Movies!-----\n")
    for row in movies_list:
        dateTime = datetime.datetime.fromtimestamp(row[1])
        date = dateTime.strftime("%b %d %Y")
        print(f"Title: {row[0]} (Released on {date})\n")
        print("---------\n")


def watch_movie():
    title = input("Enter the title of watched movie: ")
    database.watch_movie(title)


while (user_input := input(menu)) != "6":
    if user_input == "1":
        add_movie()
    elif user_input == "2":
        movies_list = database.get_movies(True)
        print_movies_list("Upcoming", movies_list)
    elif user_input == "3":
        movies_list = database.get_movies()
        print_movies_list("All", movies_list)
    elif user_input == "4":
        watch_movie()
    elif user_input == "5":
        movies_list = database.get_watched_movies()
        print_movies_list("Watched", movies_list)
    else:
        print("Invalid input, please try again!")
