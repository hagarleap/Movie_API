import mysql.connector
mydb = mysql.connector.connect(host="mysqlsrv1.cs.tau.ac.il.", user="hagarleap", password="hagar30040", database="hagarleap")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE moviesDB")