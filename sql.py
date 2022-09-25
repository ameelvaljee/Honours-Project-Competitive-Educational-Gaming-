# importing sqlite3 module
import sqlite3
 
 
# create connection by using object
# to connect with hotel_data database
connection = sqlite3.connect('mazepy.db')
 
# query to create a table named FOOD1
connection.execute('''CREATE TABLE users
         (username TEXT PRIMARY KEY NOT NULL,
          password TEXT NOT NULL,
          highscore_time_one INT,
          highscore_time_two INT,
          highscore_time_three INT,
          highscore_point_one INT,
          highscore_point_two INT,
          highscore_point_three INT);
         ''')
 
# # insert query to insert food  details in
# # the above table
connection.execute("INSERT INTO users VALUES ('calvin', '1234', 26, 26, 26, 26, 26, 26)")
connection.execute("INSERT INTO users VALUES ('ameel', '1234', 13, 13, 13, 1360, 2330, 1420)")
#connection.execute("INSERT INTO users VALUES ('asa9', '0000', 0, 0, 0, 999, 0, 0)")
#connection.execute("INSERT INTO users VALUES ('brad', '0000', 0, 0, 0, 998, 0, 0)")
#connection.execute("INSERT INTO users VALUES ('chad', '0000', 0, 0, 0, 997, 0, 0)")
connection.execute("INSERT INTO users VALUES ('RandomStudent', '0000', 10, 10, 10, 10, 10, 10)")
#connection.execute("INSERT INTO users VALUES ('bowser', '0000', 10, 0, 0, 10, 0, 0)")
connection.execute("INSERT INTO users VALUES ('notCsStudent', '0000', 1, 1, 1, 1, 1, 1)")
#connection.execute("INSERT INTO users VALUES ('throwing', '0000', 1, 0, 0, 1, 0, 0)")
#connection.execute("INSERT INTO users VALUES ('OneMSPlayer', '0000', 120, 0, 0, 0, 0, 0)")
#connection.execute("INSERT INTO users VALUES ('FasterThanLight', '0000', 119, 0, 0, 0, 0, 0)")
#connection.execute("INSERT INTO users VALUES ('aceu', '0000', 110, 0, 0, 0, 0, 0)")
#connection.execute("INSERT INTO users VALUES ('timmy', '0000', 100, 0, 0, 0, 0, 0)")
connection.execute("INSERT INTO users VALUES ('mcZ', '0000', 300, 360, 420, 4200, 2190, 3600)")
connection.execute("INSERT INTO users VALUES ('Kakashi', '0000', 30, 30, 30, 445, 890, 890)")
connection.execute("INSERT INTO users VALUES ('thanica', '1234', 28, 28, 28, 2095, 2095, 2095)")
connection.execute("INSERT INTO users VALUES ('Batsi', '1234', 77, 59, 40, 1020, 2000, 3000)")
# connection.execute("INSERT INTO users VALUES ('bella', '9999', 999, 2000)")
# connection.execute("INSERT INTO users VALUES ('sean', '2929', 29, 2929)")
# connection.execute("INSERT INTO users VALUES ('idrees', 'hockey', 5000, 987)")

# connection.commit()
 
# print("Data in table users")
 
# create a cousor object for select query
# cursor = connection.execute("SELECT * from users")
 
# # display all data from hotel table
# for row in cursor:
#     print(row)

# # create a cousor object for select query
# cursor = connection.execute("SELECT username, highscore_time from users ORDER BY highscore_time DESC")

# # create a cousor object for select query
# users = connection.execute("SELECT username from users")

# # display all data from hotel table
# for user in users:
#     print(type(user[0]))
#     print(user[0])
#     if 'calvin' == user[0]:
#         print("This is Calvin")

# #cursor.execute("UPDATE users SET {0} = {3} WHERE {1} LIKE {2} AND  {0} < {3}".format("highscore_time", "username", "calvin", 1234))

#connection.execute("UPDATE users SET {0} = {3} WHERE {1} = '{2}' AND {0} < {3}".format('highscore_point_one', 'username', 'calvin', 1234))

connection.commit()

# cursor = connection.execute("SELECT username, highscore_time_one from users ORDER BY highscore_time DESC".format('highscore_time', 'username', 'calvin', 5000))



# connection.commit()