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
        
        return mydb.cursor(buffered=True) #my cursor

    except:
        print('Failed to Connect!')


def main():
    
    ######### first you must connect to the DB, you need the cursor for each function! #########
    mycursor = connect()

    
    ######### Worst Crew Member #########
    
    ### Ex 1: man and man
    queries.query_1(mycursor, 'male', 'male', 1999)
    
