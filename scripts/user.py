from hashlib import sha256
from sqlite3 import connect
from CTkMessagebox import CTkMessagebox as ctkm
class User:
    def __init__(self, username, password, role, id):
        self.__username = username
        self.__password = self.hashPassword(password)  # Hash the password during initialization
        self.__role = role
        self__id = id

    #hashes the password using sha256 making it more secure
    @staticmethod
    def hashPassword(password):
        hashed_password = sha256(password.encode()).hexdigest()
        return hashed_password

    #checks the password entered in through the parameters to see if it returns the same hashed value as the user's password
    @staticmethod
    def checkPassword(hashed_password, password): return hashed_password == User.hashPassword(password)

    #simply returns the role of the user to know if we should create the member main screen or the librianian main screen
    def get_role(self): return self.__role

    #this is a member only screen/function
    def borrow_book(self):
        pass

    @staticmethod
    def getCurrUser(username, password):
        with connect('user_accounts.db') as conn:
            cursor = conn.cursor()
            #i dont think i need to worry about sql injections with this implementation, but im not really sure
            cursor.execute('SELECT * FROM user_table WHERE username=? AND password=?',
                           (username, User.hashPassword(password)))
            result = cursor.fetchone()
            if result:
                user_info = {
                    'username': result[1],
                    'password': result[2],
                    'role': result[3],
                }
                return user_info

    @staticmethod
    def get_curr_id(username, password):
        with connect('user_accounts.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM user_table WHERE username=? AND password=?', (username, User.hashPassword(password)))
            result = cursor.fetchone()
            if result: return result[0]

    #this is a login check, checks if the username and password have something entered in them, then we search the database for a matching record of username and matching password
    #if one is found, we return 0 so we can use this function for further logic
    #if a record is found with a matching username but mismatching password, then alert the user that it looks like the password was incorrect
    #if no record is found at all, then alert user that no username by that name exists and tell them to either correct it or register as a new user
    @staticmethod
    def loginCheck(username, password):
        # checks if anything is actually in the username and password so we dont have unecessary checks for empty entry boxes
        # if user has entered in something, then we go through the possible outcomes
        # also we create a result variable that is initalized as empty, if a username is found with matching password, then allow the user to log in
        if username != '' and password != '':
            result = ''
            with connect('user_accounts.db') as conn:
                cursor = conn.cursor()
                cursor.execute('select password from user_table where username=?', [username])
                result = cursor.fetchone()
            if result:
                if User.checkPassword(result[0], password):
                    #this will return if the user can sucessfully log in
                    return 0
                # if a username is found but incorrect password, alert user and have them try again
                else:
                    ctkm(title='Incorrect Password', message='Looks like that password doesn\'t match try again',
                         icon='warning', option_1='Close')
                    # this will return if the user entered in a correct username, but the password was found to be incorrect
                    return 1
            # if no matching username is found at all, then this will execute alerting the user to register to account
            else:
                # this will return if the user enters a username that is not present in the user_accounts database
                ctkm(title='No user Exists',
                     message='Looks like there is no username like that, you should register an account',
                     icon='warning', option_1='Close')
                return -1

    #registers the account based on the username and password entered
    @staticmethod
    def registerUser(username, password):
        if username != '' and password != '':
            user_exists = True
            with connect('user_accounts.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM user_table WHERE username = ?", (username,))
                existing = cursor.fetchone()
                if not existing: user_exists = False

            if user_exists: ctkm(title='Registration Error', message='A username by that name already exists, try fixing your password', icon='warning', option_1='Close')
            else:
                with connect('user_accounts.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("insert into user_table(username, password, role) VALUES(?, ?, 'Member')", (username, User.hashPassword(password)))
                    conn.commit()
                ctkm(title='Registration Success', message='Account successfully registered', icon='check', option_1='Close')
        else: ctkm(title='No Entry Found', message='Please enter in a username and password to register an account', icon='warning', option_1='Close')