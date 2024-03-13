import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import csv
from datetime import datetime

def movies_table(reader, mycursor, mydb):
    for row in reader:
        try:
            id_val = row.get('id')
            overview_val = row.get('overview')
            tagline_val = row.get('tagline')
            title_val = row.get('title')
            vote_avg_val = row.get('vote_average')
            vote_count_val = row.get('vote_count')
            
            # Check for release_date
            release_date_val = row.get('release_date')
            if release_date_val:
                try:
                    release_date_val = datetime.strptime(release_date_val, '%Y-%m-%d').date()
                except ValueError:
                    release_date_val = None
            else:
                release_date_val = None
            
            # Check for vote_avg
            if vote_avg_val:
                try:
                    vote_avg_val = float(vote_avg_val)
                except ValueError:
                    vote_avg_val = None
            
            # Check for vote_count
            if vote_count_val:
                try:
                    vote_count_val = int(vote_count_val)
                except ValueError:
                    vote_count_val = None
            
            mycursor.execute("INSERT INTO Movies (id, overview, release_date, tagline, title, vote_avg, vote_count) "
                             "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                             (id_val, overview_val, release_date_val, tagline_val,
                              title_val, vote_avg_val, vote_count_val))
            print(f"")
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                continue  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions   
    print("Movie table has been created successfuly")
    mydb.commit()
    
def Keywords_table(reader_movies_csv, mycursor, mydb):
    #reader_movies_csv.seek(1)
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
    #reader_movies_csv.seek(1)
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
    # reader_movies_csv.seek(1)
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
    # reader_movies_csv.seek(0)
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
    # reader.seek(1)
    for row in reader:
        cast = eval(row['cast'])
        crew = eval(row['crew'])
        movie_id = row['movie_id']
        
        insert_cast(movie_id, cast, mycursor, mydb)
        
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
                print("err1 occurred")
                raise e  # Raise other IntegrityError exceptions
            
        try:
            mycursor.execute("INSERT INTO Actor_movies (actor_id, movie_id) VALUES (%s, %s)", (id, movie_id))
            print(f"{id}, {movie_id})")
        except mysql.connector.IntegrityError as e:
            print("err occurred")
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
                pass  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions
        
        try:
            mycursor.execute("INSERT INTO MovieCrew (movie_id, crew_id, job) VALUES (%s, %s, %s)", (movie_id, id, job))
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                pass  # Skip insertion for existing keyword ID
            else:
                raise e  # Raise other IntegrityError exceptions
    
    mydb.commit()        

def main():
    mydb = mysql.connector.connect(host="localhost", user="hagarleap", password="hagar30040", database="hagarleap", port=3305)
    mycursor = mydb.cursor(buffered=True)
    movies_csv = "csvs/tmdb_5000_movies.csv"
    crew_csv = "csvs/tmdb_5000_credits.csv"

    with open(movies_csv, "r", encoding="utf-8") as movie_file:
        with open(crew_csv, "r", encoding="utf-8") as crew_file:
            
            movie_reader = csv.reader(movie_file)
            crew_reader = csv.reader(crew_file)

            movie_reader = csv.DictReader(movie_file)
            crew_reader = csv.DictReader(crew_file)
            
            #movies_table(movie_reader, mycursor, mydb)
            # Keywords_table(movie_reader, mycursor, mydb)
            # Movie_keywords_table(movie_reader, mycursor, mydb)
            # genres_table(movie_reader, mycursor, mydb)
            # Genres_movies_table(movie_reader, mycursor, mydb)
            Person_Cast_Crew_MovieCrew_MoviesActors_tables(crew_reader, mycursor, mydb)

    # Commit the changes and close the cursor and database connection

    mycursor.close()
    mydb.close()

if __name__ == "__main__":
    main()
