

import mysql.connector
from mysql.connector import errorcode

try:
    # Establishing connection to the MySQL server with out details
    mydb = mysql.connector.connect(
        host="localhost",
        user="hagarleap",
        password="hagar30040",
        database="hagarleap",
        port=3305
    )
    mycursor = mydb.cursor(buffered=True)

   # Creating tables, if they don't exist
    table_queries = [
        """CREATE TABLE IF NOT EXISTS Movies (
            id INT PRIMARY KEY, 
            overview TEXT DEFAULT NULL, 
            release_date DATE DEFAULT NULL, 
            tagline TEXT, 
            title VARCHAR(255) DEFAULT NULL, 
            vote_avg FLOAT, 
            vote_count INT, 
            FULLTEXT INDEX idx_overview (overview),
            FULLTEXT INDEX idx_tagline (tagline)
        )""",
        """CREATE TABLE IF NOT EXISTS Keywords (
            id INT PRIMARY KEY, 
            name VARCHAR(50) NOT NULL,
            FULLTEXT INDEX idx_name (name)
        )""",
        """CREATE TABLE IF NOT EXISTS Movie_keywords (
            movie_id INT, 
            keyword_id INT, 
            PRIMARY KEY (movie_id, keyword_id), 
            FOREIGN KEY (movie_id) REFERENCES Movies(id), 
            FOREIGN KEY (keyword_id) REFERENCES Keywords(id)
        )""",
        """CREATE TABLE IF NOT EXISTS Genres (
            id INT PRIMARY KEY, 
            name VARCHAR(255) NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS Genres_movies (
            movie_id INT, 
            genre_id INT, 
            PRIMARY KEY (movie_id, genre_id), 
            FOREIGN KEY (movie_id) REFERENCES Movies(id), 
            FOREIGN KEY (genre_id) REFERENCES Genres(id)
        )""",
        """CREATE TABLE IF NOT EXISTS Person (
            id INT PRIMARY KEY, 
            name VARCHAR(255), 
            gender INT
        )""",
        """CREATE TABLE IF NOT EXISTS Actor_movies (
            actor_id INT, 
            movie_id INT, 
            PRIMARY KEY (actor_id, movie_id), 
            FOREIGN KEY (actor_id) REFERENCES Person(id), 
            FOREIGN KEY (movie_id) REFERENCES Movies(id)
        )""",
        """CREATE TABLE IF NOT EXISTS MovieCrew (
            movie_id INT, 
            crew_id INT, 
            job VARCHAR(100), 
            PRIMARY KEY (movie_id, crew_id), 
            FOREIGN KEY (movie_id) REFERENCES Movies(id), 
            FOREIGN KEY (crew_id) REFERENCES Crew(crew_id)
        )""",
        """ CREATE INDEX actor_id ON Movies (vote_count);""",

        
    ]

    for query in table_queries:
        #table_name = query.split()[5] 
        mycursor.execute(query)
        #print(f"---Table {table_name} has been created---")

except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)

finally:
    # Closing cursor and database connection
    mycursor.close()
    mydb.close()
    

#         """ALTER TABLE Genres_movies DROP INDEX genre_id;""",
#         """ALTER TABLE Movies
#         ADD FULLTEXT INDEX overview_tagline_title (overview, tagline, title);"""    

        # """ CREATE INDEX crew_jobs ON MovieCrew (job, crew_id)""",
        # """ CREATE INDEX movie_rating ON Movies (id, vote_avg);""",