import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import csv

def movies_table(reader, mycursor, mydb):
    reader.seek(1)
    for row in reader:     
        try:
            mycursor.execute("INSERT INTO Movies (id, overview, release_date, tagline, title, vote_avg, vote_count) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                      (row['id'], row['overview'], row['release_date'], row['tagline'],
                       row['title'], row['vote_average'], row['vote_count']))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                continue  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions        
    mydb.commit()
    
def Keywords_table(reader_movies_csv, mycursor, mydb):
    reader_movies_csv.seek(1)
    for row in reader_movies_csv:
        if row['keywords']:
            # Extract keywords data from the 'keywords' column
            keywords = eval(row['keywords'])
            # Insert each keyword into the Keywords table
            for keyword in keywords:
                keyword_id = keyword['id']
                keyword_name = keyword['name']
                try:
                    mycursor.execute("INSERT INTO Keywords (id, name) VALUES (%s, %s)", (keyword_id, keyword_name))
                except mysql.connector.IntegrityError as e:
                    if e.errno == 1062:
                        continue  # Skip insertion for existing keyword ID
                    else:
                        raise e  # Raise other IntegrityError exceptions
    mydb.commit()
    
def Movie_keywords_table(reader_movies_csv, mycursor, mydb):
    reader_movies_csv.seek(1)
    for row in reader_movies_csv:
        if row['keywords']:
            # Extract keywords data from the 'keywords' column
            keywords = eval(row['keywords'])
            # Insert each keyword into the Keywords table
            for keyword in keywords:
                keyword_id = keyword['id']
                try:
                    mycursor.execute("INSERT INTO Movie_keywords (movie_id, keyword_id) VALUES (%s, %s)", (row['id'], keyword_id)) #row['id'] is movie id
                except mysql.connector.IntegrityError as e:
                    if e.errno == 1062:
                        continue  # Skip insertion for existing keyword ID
                    else:
                        raise e  # Raise other IntegrityError exceptions
    mydb.commit()
    
def genres_table(reader_movies_csv, mycursor, mydb):
    reader_movies_csv.seek(1)
    for row in reader_movies_csv:
        if row['genres'] and row['genres'] != '[]':
            # Extract genres data from the 'genres' column
            genres = eval(row['genres'])
            # Insert each genre into the Genres table
            for genre in genres:
                genre_id = genre['id']
                genre_name = genre['name']
                try:
                    mycursor.execute("INSERT INTO Genres (id, name) VALUES (%s, %s)", (genre_id, genre_name))
                except mysql.connector.IntegrityError as e:
                    if e.errno == 1062:
                        continue  # Skip insertion for existing genre ID
                    else:
                        raise e  # Raise other IntegrityError exceptions
    mydb.commit()
    
def Genres_movies_table(reader_movies_csv, mycursor, mydb):
    reader_movies_csv.seek(0)
    for row in reader_movies_csv:
        movie_id = row['id']
        if row['genres'] and row['genres'] != '[]':
            # Extract genres data from the 'genres' column
            genres = eval(row['genres'])
            # Insert each genre into the Genres table
            for genre in genres:
                genre_id = genre['id']
                # Insert into Genres_movies table
                try:
                    mycursor.execute("INSERT INTO Genres_movies (genre_id, movie_id) VALUES (%s, %s)", (genre_id, movie_id))
                except mysql.connector.IntegrityError as e:
                    if e.errno == 1062:
                        continue  # Skip insertion for existing genre_id, movie_id pair
                    else:
                        raise e  # Raise other IntegrityError exceptions
    mydb.commit()
    
def Person_Cast_Crew_MovieCrew_MoviesActors_tables(reader, mycursor, mydb):
    reader.seek(1)
    for row in reader:
        cast = eval(row['cast'])
        crew = eval(row['crew'])
        movie_id = row['movie_id']
        
        insert_cast(cast, mycursor, mydb)
        insert_crew(movie_id, crew, mycursor, mydb)
            
def insert_cast(movie_id, cast, mycursor, mydb):
    for person in cast:
        name = person['name']
        id = person['id']
        gender = person['gender']
        
        try:
            mycursor.execute("INSERT INTO Person (name, id, gender) VALUES (%s, %s, %s)", (name, id, gender))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                continue  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions
            
        try:
            mycursor.execute("INSERT INTO cast (id) VALUES (%s, %s, %s)", (name, id, gender))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                continue  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions
            
        try:
            mycursor.execute("INSERT INTO Actor_movies (movie_id, crew_id) VALUES (%s, %s)", (movie_id, id))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                continue  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions
    mydb.commit()
    
def insert_crew(movie_id, crew, mycursor, mydb):
    for person in crew:
        name = person['name']
        id = person['id']
        gender = person['gender']
        job = person['job']
        
        try:
            mycursor.execute("INSERT INTO Person (name, id, gender) VALUES (%s, %s, %s)", (name, id, gender))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                continue  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions
        
            
        try:
            mycursor.execute("INSERT INTO crew (crew_id) VALUES (%s)", (id))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                continue  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions
        
        try:
            mycursor.execute("INSERT INTO MovieCrew (movie_id, crew_id, job) VALUES (%s, %s, %s)", (movie_id, id, job))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                continue  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions
    mydb.commit()        

def main():
    mydb = mysql.connector.connect(host="localhost", user="hagarleap", password="hagar30040", database="hagarleap", port=3305)
    mycursor = mydb.cursor(buffered=True)
    movies_csv = "tmdb_5000_movies.csv"
    crew_csv = "tmdb_5000_credits.csv"

    with open(movies_csv, "r", encoding="utf-8") as movie_file:
        with open(crew_csv, "r", encoding="utf-8") as crew_file:
            
            movie_reader = csv.reader(movie_file)
            crew_reader = csv.reader(crew_file)

            movie_reader = csv.DictReader(movie_file)
            crew_reader = csv.DictReader(crew_file)
            
            movies_table(movie_reader, mycursor, mydb)
            Keywords_table(movie_reader, mycursor, mydb)
            Movie_keywords_table(movie_reader, mycursor, mydb)
            genres_table(movie_reader, mycursor, mydb)
            Genres_movies_table(movie_reader, mycursor, mydb)
            Person_Cast_Crew_MovieCrew_MoviesActors_tables(crew_reader, mycursor, mydb)

    # Commit the changes and close the cursor and database connection

    mycursor.close()
    mydb.close()

if __name__ == "__main__":
    main()
