import oracledb
import datetime
try:
	con = oracledb.connect(
    user="c##kevin",
    password="manager",
    dsn="localhost:49703/xe")
	#con = oracledb.connect('sys/manager@localhost:49703/xe as sysdba')

except oracledb.DatabaseError as er:
	print('There is an error in the Oracle database:', er)
cur = con.cursor()

cur.execute("create table temp12(id int)")
cur.execute("insert into temp12 values(1)")
cur.execute("insert into temp12 values(2)")
cur.execute("select * from temp12")
print(cur.fetchall())
