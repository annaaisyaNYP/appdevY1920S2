class Faq:
    countID = 0
    def __init__(self, category, question, answer):
        Faq.countID += 1
        self.__faqID = Faq.countID
        self.__category = category
        self.__question = question
        self.__answer = answer

    def get_faqID(self):
        return self.__faqID
    def get_category(self):
        return self.__category
    def get_question(self):
        return self.__question
    def get_answer(self):
        return self.__answer

    def set_faqID(self, faqID):
        self.__faqID = faqID
    def set_category(self, category):
        self.__category = category
    def set_question(self, question):
        self.__question = question
    def set_answer(self, answer):
        self.__answer = answer

    def set_countID(self, countID):
        if (Faq.countID < countID):
            Faq.countID = countID
