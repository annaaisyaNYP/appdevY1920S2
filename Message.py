class Message:
    countID = 0

    def __init__(self,name, email,subject, message):
        Message.countID += 1
        self.__messageID = Message.countID
        self.__name = name
        self.__email = email
        self.__subject = subject
        self.__message = message

    def get_messageID(self):
        return self.__messageID
    def get_name(self):
        return self.__name
    def get_email(self):
        return self.__email
    def get_subject(self):
        return self.__subject
    def get_message(self):
        return self.__message

    def set_messageID(self, messageID):
        self.__messageID = messageID
    def set_name(self, name):
        self.__name = name
    def set_email(self, email):
        self.__email = email
    def set_subject(self, subject):
        self.__subject = subject
    def set_message(self, message):
        self.__message = message
