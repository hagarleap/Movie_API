from mysql.connector import errorcode
import mysql.connector


######### Actor besties by gender and year ########
def query_1(mycursor, gender1, gender2, year):
    # Actor besties by gender :
    # Get actors frequently starring together
    
    message = ( "SELECT"
                    "a1.name AS name1,"
                    "a2.name AS name2,"
                    "COUNT(*) AS movies_together_count"
                "FROM"
                    "Person a1"
                "JOIN"
                    "Actor_movies am1 ON am1.actor_id = a1.id" 
                "JOIN"
                    "Actor_movies am2 ON am1.movie_id = am2.movie_id" 
                "JOIN"
                    "Person a2 ON am2.actor_id = a2.id" 
                "JOIN"
                    "Movies m ON am1.movie_id = m.id" 
                "WHERE"
                    f"YEAR(a1.release_date) = {year} "
                    f"AND a1.gender = {gender1} AND a2.gender = {gender2}"
                "GROUP BY "
                    "a1.id, a2.id, a1.name, a2.name"
                "ORDER BY "
                    "movies_together_count DESC"
                "LIMIT 1;"
                )
    try:
        mycursor.execute(message)
        results = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    #TODO index on release year!
    return results



def query_2(mycursor, genre):
    message = ( "WITH GenreAvgRating AS ("
                    "SELECT"
                        "g.name AS genre,"
                        "AVG(m.vote_count) AS avg_vote_count"
                    "FROM"
                        "genres g"
                    "JOIN"
                        "genres_movies gm ON g.id = gm.genres_id"
                    "JOIN"
                        "Movies m ON gm.movies_id = m.id"
                    "WHERE"
                        f"g.name = '{genre}'"
                    "GROUP BY"
                        "g.name"
                ")"

                ", LowRatersMovies AS ("
                    "SELECT"
                        "m.id AS movie_id,"
                        "m.title,"
                        "m.vote_avg,"
                        "m.vote_count"
                    "FROM"
                        "Movies m"
                    "JOIN"
                        "genres_movies gm ON m.id = gm.movies_id"
                    "JOIN"
                        "GenreAvgRating gar ON gm.genres_id = gar.genre"
                    "WHERE"
                        "gar.avg_rating IS NOT NULL"
                        "AND m.vote_count < gar.avg_vote_count"
                ")"

                "-- Select the top 5 movies with the highest ratings from the low raters group"
                "SELECT"
                    "lrm.movie_id,"
                    "lrm.title,"
                    "lrm.vote_avg,"
                    "lrm.vote_count"
                "FROM"
                    "LowRatersMovies lrm"
                "ORDER BY"
                    "lrm.vote_avg DESC"
                "LIMIT 5;"
                )
    try:
        mycursor.execute(message)
        results = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    #TODO index on genre!
    return results
    


def query_3(mycursor, job):
    message = ( f""" SELECT
                    p.name AS crewName,
                    AVG(m.vote_avg) AS AvgRating
                FROM
                    Person p
                JOIN
                    MovieCrew mc ON mc.crew_id = p.id
                JOIN
                    Movies m ON mc.movie_id = m.id

                WHERE
                    mc.job = '{job}'
                    AND m.vote_count > (SELECT
                                        AVG(m.vote_count) AS avg_vote_count
                                    FROM
                                        Movies m
                                    ) 
                    AND m.vote_avg != 0
                    
                GROUP BY
                    mc.crew_id
                ORDER BY
                    AvgRating ASC
                LIMIT 5; """
                )
    try:
        mycursor.execute(message)
        results = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    return results



def query_4(mycursor, keywords):
    message =  f"""SELECT 
                    m.title AS Title,
                    YEAR(m.release_date) AS ReleaseYear,
                    m.vote_avg Rating
                FROM 
                    Movies m
                WHERE 
                    MATCH (m.overview, m.tagline, m.title) AGAINST ('{keywords}' IN NATURAL LANGUAGE MODE) AND
                    m.release_date IS NOT NULL
                ORDER BY ReleaseYear DESC;"""
                
    try:
        mycursor.execute(message)
        results = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    return results



def query_5(mycursor, title, is_genre):
    #### if genre, fetch random movie title from genre###
    if is_genre:
        message = f"""SELECT 
                            m.title
                        FROM 
                            Movies m
                        JOIN
                            Genres_movies gm ON gm.movie_id = m.id
                        JOIN
                            Genres g ON g.id = gm.genre_id
                        JOIN 
                            Movie_keywords mk ON m.id = mk.movie_id
                        Where
                            g.name = '{title}'
                        ORDER BY RAND()
                        LIMIT 1;   """
                    
        try:
            mycursor.execute(message)
            title = mycursor.fetchall()[0]
        except mysql.connector.Error as err:
            print("Failed fetching data: {}".format(err))
            exit(1)   
            
                         
    message_1 = f"""SELECT 
                        k.name
                    FROM 
                        Keywords k
                    JOIN 
                        Movie_keywords mk ON k.id = mk.keyword_id
                    JOIN 
                        Movies m on mk.movie_id = m.id
                    Where
                        m.title = '{title}' """
               
                
    try:
        mycursor.execute(message_1)
        keywords = mycursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    
    delimiter = ' '

    keywords = delimiter.join(word for word in keywords)    
            
    return query_4(mycursor, keywords)
    
