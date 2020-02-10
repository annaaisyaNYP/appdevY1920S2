from wtforms import Form, StringField, RadioField, SelectField,TextAreaField, PasswordField, validators

class CreateUserForm(Form):
 firstName = StringField('First Name', [validators.Length(min=1,max=150), validators.DataRequired()])
 lastName = StringField('Last Name', [validators.Length(min=1,max=150), validators.DataRequired()])
 password = PasswordField('Password', [validators.Length(min=8, max=32), validators.DataRequired()])
 email = StringField('Email', [validators.Length(min=1,max=150), validators.DataRequired(), validators.email()])
 gender = SelectField('Gender', [validators.DataRequired()],choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],default='')
 remarks = TextAreaField('Remarks', [validators.Optional()])

class CreateMessageForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    email = StringField("Email",  [validators.Email(), validators.DataRequired()])
    subject = SelectField('Subject', [validators.DataRequired()], choices=[('', 'Select'), ('R/F', 'Review/Feedback'), ('Q', 'Question'), ('O', 'Others')], default='')
    message = TextAreaField('Message', [validators.Optional()])

class CreateLoginForm(Form):
    email = StringField('Email', [validators.Length(min=1,max=150), validators.DataRequired(), validators.email()])
    password = PasswordField('Password', [validators.Length(min=8, max=32), validators.DataRequired()])
