class User:
    countID = 0

    def __init__(self, firstName, lastName, password, gender, email, remarks):
        User.countID += 1
        self.__userID = User.countID
        self.__firstName = firstName
        self.__lastName = lastName
        self.__password = password
        self.__gender = gender
        self.__email = email
        self.__remarks = remarks

    def get_userID(self):
        return self.__userID

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_password(self):
        return self.__password

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_remarks(self):
        return self.__remarks

    def set_userID(self, userID):
        self.__userID = userID

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_password(self, password):
        self.__password = password

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_remarks(self, remarks):
        self.__remarks = remarks

