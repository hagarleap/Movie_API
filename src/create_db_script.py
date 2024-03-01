import mysql.connector
from mysql.connector import errorcode

mydb = mysql.connector.connect(host="localhost", user="hagarleap", password="hagar30040", database="hagarleap", port=3305)
mycursor = mydb.cursor(buffered=True)


# def create_database(cursor):
try:
    mycursor.execute(("CREATE TABLE IF NOT EXISTS Movies (id INT PRIMARY KEY, overview TEXT, release_date DATE,"
                        "tagline TEXT, title VARCHAR(255), vote_avg FLOAT, vote_count INT, FULLTEXT(overview), FULLTEXT(tagline))"))
    print("---Table Movies created---")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Keywords (id INT PRIMARY KEY, name VARCHAR(50)")
    print("---Table Keywords created---")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Movie_keywords (movie_id INT REFERENCES Movies(id), keyword_id INT REFERENCES Keywords(id))")
    print("---Table Movie_keywords created---")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Genres (id INT PRIMARY KEY, name VARCHAR(255))")
    print("---Table Genres created---")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Genres_movies (genres_id INT REFERENCES Genres(id), movies_id INT REFERENCES Movies(id))")
    print("---Table Genres_movies created---")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Person (id INT PRIMARY KEY, name VARCHAR(255), gender INT)")
    print("---Table Person created---")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Cast (cast_id int REFERENCES Person(id))")
    print("---Table Cast created---")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Crew (crew_id INT REFERENCES Person(id)")
    print("---Table Crew created---")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Actor_movies (actor_id INT REFERENCES Cast(id), movie_id INT REFERENCES Movies(id),"
                        " PRIMARY KEY (actor_id, movie_id)") 
    print("---Table Actor_movies created---")
    mycursor.execute("CREATE TABLE MovieCrew (movie_id INT, crew_id INT, job VARCHAR(100), PRIMARY KEY (movie_id, crew_id, job),"
                        "FOREIGN KEY (movie_id) REFERENCES Movies(id), FOREIGN KEY (crew_id) REFERENCES"
                        " Crew(crew_id)")
    print("---Table MovieCrew created---")
            
    
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)

finally:
    mycursor.close()
    mydb.close()
