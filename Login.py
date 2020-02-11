class Login:
    status = False
    def __init__(self,status, session):
        self.__status = status
        # True == Logged in
        # False == Logged out
        self.__session = session
        # staff / customer

    def get_status(self):
        return self.__status
    def get_session(self):
        return self.__session

    def set_status(self, status):
        self.__status = status
    def set_session(self,session):
        self.__session = session


