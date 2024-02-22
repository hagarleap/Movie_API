import mysql.connector
from mysql.connector import errorcode

mydb = mysql.connector.connect(host="localhost", user="hagarleap", password="hagar30040", database="hagarleap", port=3305)
mycursor = mydb.cursor(buffered=True)


# def create_database(cursor):
try:
    mycursor.execute(
        "CREATE DATABASE hagarleap_db")
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)

# try:
#     mycursor.execute("USE {}".format("Movies_DB"))
# except mysql.connector.Error as err:
#     print("Database {} does not exists.".format("Movies_DB"))
#     if err.errno == errorcode.ER_BAD_DB_ERROR:
#         create_database(mycursor)
#         print("Database {} created successfully.".format("Movies_DB"))
#         mydb.database = "Movies_DB"
#     else:
#         print(err)
#         exit(1)