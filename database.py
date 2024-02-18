import datetime
import sqlite3

connection = sqlite3.connect("data.db")

create_movie_table = """ CREATE TABLE IF NOT EXISTS movies(
    title TEXT,
    release_timestamp REAL,
    watched INTEGER
);
"""

insert_movies = """ INSERT INTO movies (title,release_timestamp,watched) VALUES (?,?,?);"""
select_all_movies = """SELECT * FROM movies;"""
select_upcoming_movies = """SELECT * FROM movies WHERE release_timestamp > ?;"""
select_watched_movies = """SELECT * FROM movies WHERE watched = 1;"""



def create_tables():
    with connection:
        connection.execute(create_movie_table)

def add_movie(title,release_timestamp,watched):
    with connection:
        connection.execute(insert_movies,(title,release_timestamp,watched))

def get_movies(upcoming = False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            #(today_timestamp,) this comma is neccssary because the parameters take a tuple
            cursor.execute(select_upcoming_movies,(today_timestamp,)) 
        else:
            cursor.execute(select_all_movies)

    return cursor.fetchall()

def get_watched_movies():
    with connection:
        cursor = connection.cursor()
        cursor.execute(select_watched_movies)

    return cursor.fetchall()