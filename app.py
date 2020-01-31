from flask import Flask, render_template, request, redirect, url_for
from flask_moment import Moment
from forms import CreateUserForm
import shelve, User, pathlib

app = Flask(__name__)
moment = Moment(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
    createUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and createUserForm.validate():
        usersDict = {}
        path = pathlib.Path('storage.db')
        if path.exists() == False:
            db = shelve.open('storage.db', 'c')
        else:
            db = shelve.open('storage.db', 'a')

        try:
            usersDict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = User.User(createUserForm.firstName.data, createUserForm.lastName.data, createUserForm.gender.data,
                         createUserForm.email.data, createUserForm.remarks.data)
        usersDict[user.get_userID()] = user
        db['Users'] = usersDict
        db.close()
        return redirect(url_for('home'))
    return render_template('createUser.html', form=createUserForm)

@app.route('/retrieveUsers')
def retrieveUsers():
    usersDict = {}
    db = shelve.open('storage.db', 'r')
    usersDict = db['Users']
    db.close()

    usersList = []
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)
    return render_template('retrieveUsers.html',usersList=usersList, count=len(usersList))

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def updateUser(id):
    updateUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        userDict = {}
        db = shelve.open('storage.db', 'w')
        userDict = db['Users']

        user = userDict.get(id)
        user.set_firstName(updateUserForm.firstName.data)
        user.set_lastName(updateUserForm.lastName.data)
        user.set_email(updateUserForm.email.data)
        user.set_gender(updateUserForm.gender.data)
        user.set_remarks(updateUserForm.remarks.data)

        db['Users'] = userDict
        db.close()

        return redirect(url_for('retrieveUsers'))
    else:
        userDict = {}
        db = shelve.open('storage.db', 'r')
        userDict = db['Users']
        db.close()

        user = userDict.get(id)
        updateUserForm.firstName.data = user.get_firstName()
        updateUserForm.lastName.data = user.get_lastName()
        updateUserForm.email.data = user.get_email()
        updateUserForm.gender.data = user.get_gender()
        updateUserForm.remarks.data = user.get_remarks()

        return render_template('updateUser.html', form=updateUserForm)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def deleteUser(id):
    usersDict = {}
    db = shelve.open('storage.db', 'w')
    usersDict = db['Users']

    usersDict.pop(id)

    db['Users'] = usersDict
    db.close()

    return redirect(url_for('retrieveUsers'))

@app.route('/contactUsFAQ')
def FAQ():
    return render_template('contactUsFAQ.html')

@app.route('/login')
def login() :
    return render_template('login.html')

@app.route('/staff')
def staff() :
    return render_template('staffDash.html')

@app.route('/test')
def test() :
    return render_template('proof.html')

if __name__ == '__main__' :
    app.run()

