import mysql.connector
from mysql.connector import errorcode
import queries_db_script as queries

def connect():
    try:
        # Establishing connection to the MySQL server with out details
        mydb = mysql.connector.connect(
            host="localhost",
            user="hagarleap",
            password="hagar30040",
            database="hagarleap",
            port=3305
        )
        
        return mydb.cursor(buffered=True), mydb #my cursor

    except:
        print('Failed to Connect!')

def disconnect(mycursor, mydb):
    mycursor.close()
    mydb.close()

def main():
    
    ######### first you must connect to the DB, you need the cursor for each function! #########
    mycursor, mydb = connect()

    try:
        
######### Actor Besties #########
        
        ### Ex 1: man and man in 1999
        print(queries.query_1(mycursor, 'male', 'male', 1999))
        ### Ex 2: man and woman in 2008
        print(queries.query_1(mycursor, 'male', 'female', 2008))
        ### Ex 3: Illegal year: 2025
        print(queries.query_1(mycursor, 'male', 'female', 2025))
        ### Ex 4: Unsupported gender: Dolphin
        print(queries.query_1(mycursor, 'dolphin', 'male', 2004))  
        
######### Suspicious Movie Reccomendations #########
        
        ### Ex 1: Horror
        print(queries.query_2(mycursor, 'Horror'))
        ### Ex 2: Science Fiction
        print(queries.query_2(mycursor, 'Science Fiction'))   
        ### Ex 3: Made up genre: Clowning
        print(queries.query_2(mycursor, 'Clowning'))
        
######### These Crew Members Ruined The Movie #########
        
        ### Ex 1: Director 
        print(queries.query_3(mycursor, 'Director'))
        ### Ex 2: Tattooist
        print(queries.query_3(mycursor, 'Tattooist'))  
        ### Ex 3: Made up job: Ballerina   
        print(queries.query_3(mycursor, 'Ballerina')) 
        
######### Movie Lookup #########
        ### Ex 1: Legal lookup
        print(queries.query_4(mycursor, "romantic horror with aliens"))
        ### Ex 2: Illegal lookup
        print(queries.query_4(mycursor, "CURSE WORDS @#$%&!"))    
          
######### Bad "similar to" Movie Reccomendations #########
        ### Ex 1: Similar to "The Godfather"
        print(queries.query_5(mycursor, "The Godfather", False))
        ### Ex 2: Similar to Animation genre
        print(queries.query_5(mycursor, "Animation", True))   
        ### Ex 3: Illegal lookup
        print(queries.query_5(mycursor, ":-)", False))    
    except:
        print("Failed to execute query!")
        
    finally:    
        ######### disconnect #########
        disconnect(mycursor, mydb)
if __name__ == '__main__':
    main()  