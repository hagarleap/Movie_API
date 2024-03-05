import mysql.connector
from mysql.connector import errorcode
import queries_db_script as queries
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

except:
    print('err')
    
print(queries.query_4(mycursor, 'happy'))