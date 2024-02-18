import datetime
import sqlite3

connection = sqlite3.connect("data.db")
connection.execute(
    "PRAGMA foreign_keys = ON;"
)  # only after this foreign_keys support starts

create_movie_table = """ CREATE TABLE IF NOT EXISTS movies(
id INTEGER PRIMARY KEY,
title TEXT COLLATE NOCASE,
release_timestamp REAL,
UNIQUE (title,release_timestamp) );"""
create_user_table = (
    """CREATE TABLE IF NOT EXISTS users(username TEXT COLLATE NOCASE PRIMARY KEY);"""
)
create_watched_table = """CREATE TABLE IF NOT EXISTS watched (
username TEXT COLLATE NOCASE,
movie_id INTEGER,
PRIMARY KEY (username, movie_id),
FOREIGN KEY (username) REFERENCES users(username),
FOREIGN KEY (movie_id) REFERENCES movies(id)
);"""
select_watched_movies = """SELECT movies.* 
FROM movies 
JOIN watched ON movies.id = watched.movie_id
WHERE watched.username = ?;"""
insert_movies = """INSERT INTO movies (title,release_timestamp) VALUES (?,?);"""
insert_user = """INSERT INTO users (username) VALUES (?);"""
insert_watched_movies = """INSERT INTO watched(username,movie_id) VALUES (?,?);"""
select_all_movies = """SELECT * FROM movies;"""
select_upcoming_movies = """SELECT * FROM movies WHERE release_timestamp > ?;"""
update_watch_movie = """UPDATE moviesSET watched = 1 WHERE title = ?;"""
search_movies_query = """SELECT * FROM movies WHERE title LIKE ?;"""
check_user = "SELECT 1 FROM users WHERE username = ?;"


def create_tables():
    with connection:
        connection.execute(create_user_table)
        connection.execute(create_movie_table)
        connection.execute(create_watched_table)


def add_movie(title, release_timestamp):
    try:
        with connection:
            connection.execute(insert_movies, (title, release_timestamp))
        return "Movie added Successfully!"
    except Exception as e:
        return f"Error: {e}.\n"


def add_user(username):
    try:
        with connection:
            connection.execute(insert_user, (username,))
        return "User Created Successfully!"
    except Exception as e:
        return f"Error: {e}\n"


def get_movies(upcoming=False):
    cursor = connection.cursor()
    try:
        with connection:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                # (today_timestamp,) this comma is neccssary because the parameters take a tuple
                cursor.execute(select_upcoming_movies, (today_timestamp,))
            else:
                cursor.execute(select_all_movies)

        return cursor.fetchall(), "OK"
    except Exception as e:
        return [], f"Error: {e}\n"


def check_user_exists(username):
    cursor = connection.cursor()
    with connection:
        cursor.execute(check_user, (username,))
    result = cursor.fetchone()

    if result is not None:
        return True

    return False


def get_watched_movies(username):

    if check_user_exists(username) == True:
        cursor = connection.cursor()
        try:
            with connection:
                cursor.execute(select_watched_movies, (username,))

            return cursor.fetchall(), "OK"
        except Exception as e:
            return [], f"Error: {e}\n"
    else:
        return [], f"Error: {username} does not exists!\n"


def watch_movie(username, movie_id):
    try:
        with connection:
            connection.execute(insert_watched_movies, (username, movie_id))
    except Exception as e:
        print(f"Error: {e}\n")


def search_movies(pattern):
    cursor = connection.cursor()
    with connection:
        cursor.execute(search_movies_query, (f"%{pattern}%",))

    return cursor.fetchall()
