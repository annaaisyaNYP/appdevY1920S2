from flask import Flask, render_template, request, redirect, url_for
from flask_moment import Moment
from forms import *
import shelve, User, Message, Question, Login, Report, pathlib

app = Flask(__name__)
moment = Moment(app)
login0 = Login.Login(False, "Anonymous")

@app.route('/')
def home():
    return render_template('home.html', status=login0.get_status())

# User Management ######################################################################################################
@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
    createUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and createUserForm.validate():
        usersDict = {}
        path = pathlib.Path('user.db')
        if path.exists() == False:
            db = shelve.open('user.db', 'c')
        else:
            db = shelve.open('user.db', 'a')

        try:
            usersDict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = User.User(createUserForm.firstName.data, createUserForm.lastName.data, createUserForm.password.data, createUserForm.gender.data,
                         createUserForm.email.data, createUserForm.remarks.data)
        usersDict[user.get_userID()] = user
        db['Users'] = usersDict
        db.close()
        return redirect(url_for('thanks'))
    return render_template('U-createUser.html', form=createUserForm)

@app.route('/retrieveUsers')
def retrieveUsers():
    usersDict = {}
    db = shelve.open('user.db', 'r')
    usersDict = db['Users']
    db.close()

    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)
    return render_template('U-retrieveUsers.html',usersList=usersList, count=len(usersList))

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def updateUser(id):
    updateUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        userDict = {}
        db = shelve.open('user.db', 'a')
        userDict = db['Users']

        user = userDict.get(id)
        user.set_firstName(updateUserForm.firstName.data)
        user.set_lastName(updateUserForm.lastName.data)
        #user.set_password(updateUserForm.password.data)
        user.set_email(updateUserForm.email.data)
        user.set_gender(updateUserForm.gender.data)
        user.set_remarks(updateUserForm.remarks.data)

        db['Users'] = userDict
        db.close()

        return redirect(url_for('staff'))
    else:
        userDict = {}
        db = shelve.open('user.db', 'r')
        userDict = db['Users']
        db.close()

        user = userDict.get(id)
        updateUserForm.firstName.data = user.get_firstName()
        updateUserForm.lastName.data = user.get_lastName()
        updateUserForm.password.data = user.get_password()
        updateUserForm.email.data = user.get_email()
        updateUserForm.gender.data = user.get_gender()
        updateUserForm.remarks.data = user.get_remarks()

        return render_template('U-updateUser.html', form=updateUserForm)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def deleteUser(id):
    usersDict = {}
    db = shelve.open('user.db', 'w')
    usersDict = db['Users']

    usersDict.pop(id)

    db['Users'] = usersDict
    db.close()

    return redirect(url_for('staff'))

# Contact Us ###########################################################################################################
@app.route('/contactUs', methods=['GET', 'POST'])
def createMessage():
    createMessageForm = CreateMessageForm(request.form)
    if request.method == 'POST' and createMessageForm.validate():
        messagesDict = {}
        path = pathlib.Path('message.db')
        if path.exists() == False:
            db = shelve.open('message.db', 'c')
        else:
            db = shelve.open('message.db', 'a')

        try:
            messagesDict = db['Messages']

        except:
            print("Error in retrieving Messages from message.db.")

        message = Message.Message(createMessageForm.name.data, createMessageForm.email.data, createMessageForm.subject.data, createMessageForm.message.data)
        messagesDict[message.get_messageID()] = message
        db['Messages'] = messagesDict
        db.close()
        return redirect(url_for('thanks'))
    return render_template('C-contactUs.html', form=createMessageForm)

@app.route('/retrieveMessages')
def retrieveMessages():
    messagesDict = {}
    db = shelve.open('message.db', 'r')
    messagesDict = db['Messages']
    db.close()

    messagesList = []
    for key in messagesDict:
        message = messagesDict.get(key)
        messagesList.append(message)
    return render_template('C-getMessages.html', messagesList = messagesList, count=len (messagesList))

@app.route('/updateMessage/<int:id>/', methods=['GET', 'POST'])
def updateMessage(id):
    updateMessageForm = CreateMessageForm(request.form)
    if request.method == 'POST' and updateMessageForm.validate():
        messageDict = {}
        db = shelve.open('message.db', 'w')
        messageDict = db['Messages']

        message = messageDict.get(id)
        message.set_name(updateMessageForm.name.data)
        message.set_email(updateMessageForm.email.data)
        message.set_subject(updateMessageForm.subject.data)
        message.set_message(updateMessageForm.message.data)

        db['Messages'] = messageDict
        db.close()

        return redirect(url_for('retrieveMessage'))

    else:
        messageDict = {}
        db = shelve.open('user.db', 'r')
        messageDict = db['Messages']
        db.close()

        message = messageDict.get(id)
        updateMessageForm.name.data = message.get_name()
        updateMessageForm.email.data = message.get_email()
        updateMessageForm.subject.data = message.get_subject()
        updateMessageForm.message.data = message.get_message()

        return render_template('C-updateMessage.html', form=updateMessageForm)

@app.route('/deleteMessage/<int:id>', methods=['GET', 'POST'])
def deletemessage(id):
    messagesDict = {}
    db = shelve.open('message.db', 'w')
    messagesDict = db['Messages']

    messagesDict.pop(id)

    db['Messages'] = messagesDict
    db.close()

    return redirect(url_for('retrieveMessages'))

# FAQ ##################################################################################################################
@app.route('/FAQ')
def FAQ():
    ii = 0
    try:
        faqsDict = {}
        db = shelve.open('question.db', 'r')
        faqsDict = db['Faqs']
        db.close()
        faqsList = []
        for key in faqsDict:
            faq = faqsDict.get(key)
            faqsList.append(faq)
            ii = faq.get_faqID()
            faq.set_countID(ii)
        return render_template('F-FAQ.html', faqsList = faqsList, count=len (faqsList))
    except:
        return render_template('F-FAQ.html')

@app.route('/createFaq', methods=['GET', 'POST'])
def createFaq():
    createFaqForm = CreateFaqForm(request.form)
    if request.method == 'POST' and createFaqForm.validate():
        faqsDict = {}
        path = pathlib.Path('question.db')
        if path.exists() == False:
            db = shelve.open('question.db', 'c')
        else:
            db = shelve.open('question.db', 'a')
        try:
            faqsDict = db['Faqs']
        except:
            print("Error in retrieving Users from question.db.")
        faq = Question.Faq(createFaqForm.category.data, createFaqForm.question.data, createFaqForm.answer.data)
        faqsDict[faq.get_faqID()] = faq
        db['Faqs'] = faqsDict
        db.close()
        return redirect(url_for('retrieveFaqs'))
    else:
        return render_template('F-createFaq.html', form=createFaqForm)

@app.route('/retrieveFaqs')
def retrieveFaqs():
    try:
        faqsDict = {}
        db = shelve.open('question.db', 'r')
        faqsDict = db['Faqs']
        db.close()
        faqsList = []
        for key in faqsDict:
            faq = faqsDict.get(key)
            faqsList.append(faq)
            ii = faq.get_faqID()
            faq.set_countID(ii)
        return render_template('F-editFaqs.html', faqsList = faqsList, count=len (faqsList))
    except:
        print("Error in retrieving Faqs from question.db.")
        return render_template('home.html')

@app.route('/updateFaq/<int:id>/', methods=['GET', 'POST'])
def updateFaq(id):
    updateFaqForm = CreateFaqForm(request.form)
    if request.method == 'POST' and updateFaqForm.validate():
        faqDict = {}
        db = shelve.open('question.db', 'w')
        faqDict = db['Faqs']
        faq = faqDict.get(id)
        faq.set_category(updateFaqForm.category.data)
        faq.set_question(updateFaqForm.question.data)
        faq.set_answer(updateFaqForm.answer.data)
        db['Faqs'] = faqDict
        db.close()
        return redirect(url_for('retrieveFaqs'))
    else:
        faqDict = {}
        db = shelve.open('question.db', 'r')
        faqDict = db['Faqs']
        db.close()
        faq = faqDict.get(id)
        updateFaqForm.category.data = faq.get_category()
        updateFaqForm.question.data = faq.get_question()
        updateFaqForm.answer.data = faq.get_answer()
        return render_template('F-updateFaq.html', form=updateFaqForm)

@app.route('/deleteFaq/<int:id>', methods=['GET', 'POST'])
def deleteFaq(id):
    faqsDict = {}
    db = shelve.open('question.db', 'w')
    faqsDict = db['Faqs']
    faqsDict.pop(id)
    db['Faqs'] = faqsDict
    db.close()
    return redirect(url_for('retrieveFaqs'))

# Products #############################################################################################################
# Orders ###############################################################################################################
# Delivery #############################################################################################################
@app.route('/createReport', methods=['GET', 'POST'])
def createReport():
    createReportForm = CreateReportForm(request.form)
    if request.method == 'POST' and createReportForm.validate():
        reportsDict = {}
        path = pathlib.Path('reports.db')
        if path.exists() == False:
            db = shelve.open('reports.db', 'c')
        else:
            db = shelve.open('reports.db', 'a')

        try:
            reportsDict = db['Reports']
        except:
            print("Error in retrieving Reports from reports.db.")

        report = Report.Report(createReportForm.firstName.data, createReportForm.lastName.data, createReportForm.deliveryID.data, createReportForm.method.data, createReportForm.remarks.data)
        reportsDict[report.get_reportID()] = report
        db['Reports'] = reportsDict

        db.close()

        return redirect(url_for('retrieveReport'))
    return render_template('D-createReport.html', form=createReportForm)

@app.route('/retrieveReport')
def retrieveReport():
    reportsDict = {}
    db = shelve.open('reports.db', 'r')
    reportsDict = db['Reports']
    db.close()

    reportsList = []
    for key in reportsDict:
        report = reportsDict.get(key)
        reportsList.append(report)

    return render_template('D-retrieveReport.html', reportsList=reportsList, count=len(reportsList))

@app.route('/updateReport/<int:id>/', methods=['GET', 'POST'])
def updateReport(id):
    updateReportForm = CreateReportForm(request.form)
    if request.method == 'POST' and updateReportForm.validate():
        reportDict = {}
        db = shelve.open('reports.db', 'w')
        reportDict = db['Reports']
        report = reportDict.get(id)
        report.set_firstName(updateReportForm.firstName.data)
        report.set_lastName(updateReportForm.lastName.data)
        report.set_deliveryID(updateReportForm.deliveryID.data)
        report.set_method(updateReportForm.method.data)
        report.set_remarks(updateReportForm.remarks.data)
        db['Reports'] = reportDict
        db.close()
        return redirect(url_for('retrieveReport'))
    else:
        reportDict = {}
        db = shelve.open('reports.db', 'r')
        reportDict = db['Reports']
        db.close()
        for id in reportDict:
            print(id)
        report = reportDict.get(id)
        updateReportForm.firstName.data = report.get_firstName()
        updateReportForm.lastName.data = report.get_lastName()
        updateReportForm.deliveryID.data = report.get_deliveryID()
        updateReportForm.method.data = report.get_method()
        updateReportForm.remarks.data = report.get_remarks()

        return render_template('D-updateReport.html', form=updateReportForm)

@app.route('/deleteReport/<int:id>', methods=['GET', 'POST'])
def deleteReport(id):
    reportsDict = {}
    db = shelve.open('reports.db', 'w')
    reportsDict = db['Reports']
    reportsDict.pop((id))
    db['Reports'] = reportsDict
    db.close()

    return redirect(url_for('retrieveReport'))

# Others ###############################################################################################################
@app.route('/login', methods=['GET','POST'])
def login():
    createLoginForm = CreateLoginForm(request.form)
    if request.method == 'POST' and createLoginForm.validate():
        user1 = User.User("", "", createLoginForm.password.data, "",createLoginForm.email.data, "")
        try:
            db = shelve.open('user.db', 'r')
            usersDict = db['Users']
            db.close()

        except:
            print("Error in retrieving Users from storage.db.")
            return render_template('home.html')

        for key in usersDict:
            user2 = usersDict.get(key)
            if ((user1.get_email() == user2.get_email()) and (user1.get_password() == user2.get_password())):
                login0.set_status(True)
                print("Log in sucessful")
                if user1.get_email() == "admin@dorcks.sg":
                    login0.set_session('Staff')
                    return render_template('U-staffDash.html')
                else:
                    login0.set_session('Customer')
                    return render_template('U-login.html', status=login0.get_status())
            else:
                print("Wrong email/password")
                return render_template('U-login.html', form=createLoginForm)
    else:
        return render_template('U-login.html', form=createLoginForm)

@app.route('/logout')
def logout():
    login0.set_status(False)
    login0.set_session("Anonymous")
    return redirect(url_for('thanks'))

@app.route('/staff')
def staff():
    usersDict = {}
    db = shelve.open('user.db', 'r')
    usersDict = db['Users']
    db.close()
    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)

    messagesDict = {}
    db = shelve.open('message.db', 'r')
    messagesDict = db['Messages']
    db.close()
    messagesList = []
    for key in messagesDict:
         message = messagesDict.get(key)
         messagesList.append(message)

    reportsDict = {}
    db = shelve.open('reports.db', 'r')
    reportsDict = db['Reports']
    db.close()
    reportsList = []
    for key in reportsDict:
        report = reportsDict.get(key)
        reportsList.append(report)

    return render_template('U-StaffDash.html',usersList=usersList, count=len(usersList),
                           reportsList=reportsList, countC=len(reportsList),
                            messagesList = messagesList, countD=len(messagesList))

@app.route('/thankyou')
def thanks():
    return render_template('ThankYou.html')

if __name__ == '__main__' :
    app.run(debug=True)

