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
        results = mycursor.fetchall(message)
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
                        f"g.name = {genre}"
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
        results = mycursor.fetchall(message)
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    #TODO index on genre!
    return results
    


def query_3():
    message = ( "SELECT"
                    "a1.name AS name1,"
                    "a2.name AS name2,"
                    "COUNT(*) AS movies_together_count"
                "FROM"
                    "Person a1"
                "JOIN"
                    "Actor_movies am1 ON am1.actor_id = a1.id" 
                "JOIN"
                    "Actor_movies am2 ON am1.movie_id = am2.movie_id AND am1.actor_id < am2.actor_id" 
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
        results = mycursor.fetchall(message)
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    #TODO index on release year!
    return results



#Sophie - 4.3.2023
def query_4(keyword):
    message = ( "SELECT Keywords.name AS keywords"
                "FROM Movies"
                "INNER JOIN Movie_keywords ON Movies.id = Movie_keywords.movie_id"
                "INNER JOIN Keywords ON Movie_keywords.keyword_id = Keywords.id"
                "WHERE MATCH(Keywords.name) AGAINST('{keyword}' IN NATURAL LANGUAGE MODE);"
                )
    try:
        results = mycursor.fetchall(message)
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    #TODO index on release year!
    return results




def query_5():
    message = ( "SELECT"
                    "a1.name AS name1,"
                    "a2.name AS name2,"
                    "COUNT(*) AS movies_together_count"
                "FROM"
                    "Person a1"
                "JOIN"
                    "Actor_movies am1 ON am1.actor_id = a1.id" 
                "JOIN"
                    "Actor_movies am2 ON am1.movie_id = am2.movie_id AND am1.actor_id < am2.actor_id" 
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
        results = mycursor.fetchall(message)
    except mysql.connector.Error as err:
        print("Failed fetching data: {}".format(err))
        exit(1)
    #TODO index on release year!
    return results
    
