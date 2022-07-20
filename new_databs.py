import mysql.connector
def get():
	a = []
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  password="khadde",
	  database="Typing"
	)
	mycursor = mydb.cursor()

	mycursor.execute("SELECT Time, Accuracy, WPM FROM Data")
	myresult = mycursor.fetchall()
	for x in myresult:
	  a += [x]
	return a
a = get()
print(a[0])
