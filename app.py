from flask import Flask, render_template, request, redirect, url_for
from flask_moment import Moment
from forms import *
import shelve, User, Message, pathlib

app = Flask(__name__)
moment = Moment(app)

@app.route('/')
def home():
    return render_template('home.html')

# User Management
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
        return redirect(url_for('home'))
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

# Contact Us
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
        return redirect(url_for('retrieveMessages'))
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



@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

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
                print("CONGRATULATIONS")
                return render_template('home.html')
            else:
                print("WRONG EMAIL/PASSWORD")
                return render_template('login.html', form=createLoginForm)
    else:
        return render_template('login.html', form=createLoginForm)

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
    return render_template('U-StaffDash.html',usersList=usersList, count=len(usersList))

if __name__ == '__main__' :
    app.run(debug=True)

