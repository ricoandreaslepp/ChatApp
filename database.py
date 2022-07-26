import sqlite3
import hashlib
import binascii
import getpass
import os

class Database:
    
    def __init__(self):
        self.conn = sqlite3.connect("mydatabase.db")
        self.cursor = self.conn.cursor()

        try:
            self.__reset_database()
        except sqlite3.OperationalError:
            pass

        try:
            self.__create_table()
        except sqlite3.OperationalError:
            pass

        self.__add_user("Peter", "donttellanyone")
        #self.show_table()

    def __create_table(self):
        self.cursor.execute("""CREATE TABLE creds
                                (username text, password_hash text, salt text)
                            """)

    def __reset_database(self):
        self.cursor.execute("""DELETE FROM creds""") # keeps the format
        self.conn.commit()

    def __hash_function(self, pwd, salt=None):
        if not salt:
            salt = binascii.b2a_hex(os.urandom(32))
            return salt, hashlib.sha256(pwd.encode("UTF-8")+salt).hexdigest()

        return hashlib.sha256((pwd+salt).encode("UTF-8")).hexdigest()

    def __add_user(self, name, pwd):
        salt, pwd_hash = self.__hash_function(pwd)

        self.cursor.execute("INSERT INTO creds VALUES ({!r}, {!r}, {!r})".format(name, pwd_hash, salt.decode()))
        self.conn.commit()


    def check_creds(self, user_name, user_pwd):
        # needs an error check
        self.cursor.execute("""SELECT username, password_hash, salt 
                                FROM creds WHERE username = {!r}""".format(user_name))
        db_name, db_pwd_hash, db_salt = self.cursor.fetchall()[0]

        if self.__hash_function(user_pwd, db_salt) == db_pwd_hash:
            print("Logged in!")
        else:
            print("Wrong credentials!")


    def show_table(self):
        for row in self.cursor.execute("""SELECT * FROM creds """):
            print(row)

if __name__=='__main__':
    d = Database()
    d.check_creds(input("Username: ").strip(), getpass.getpass().strip())
