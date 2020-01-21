from flask import Flask, render_template, request, redirect, url_for
from forms import CreateUserForm

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
 createUserForm = CreateUserForm(request.form)
 if request.method == 'POST' and createUserForm.validate():
    return redirect(url_for('home'))
 return render_template('createUser.html', form=createUserForm)

@app.route('/contactUsFAQ')
def FAQ():
    return render_template('contactUsFAQ.html')

if __name__ == '__main__' :
    app.run()

