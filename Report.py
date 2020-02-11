class Report:
    countID = 0

    def __init__(self, firstName, lastName, deliveryID, method, remarks):
        Report.countID += 1
        self.__reportID = Report.countID
        self.__firstName = firstName
        self.__lastName = lastName
        self.__deliveryID = deliveryID
        self.__method = method
        self.__remarks = remarks

    def get_reportID(self):
        return self.__reportID

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_deliveryID(self):
        return self.__deliveryID

    def get_method(self):
        return self.__method

    def get_remarks(self):
        return self.__remarks

    def set_userID(self, userID):
        self.__userID = userID

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_deliveryID(self, deliveryID):
        self.__deliveryID = deliveryID

    def set_method(self, method):
        self.__method = method

    def set_remarks(self, remarks):
        self.__remarks = remarks
