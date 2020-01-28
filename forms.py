from wtforms import Form, StringField, RadioField, SelectField,TextAreaField, validators

class CreateUserForm(Form):
 firstName = StringField('First Name', [validators.Length(min=1,max=150), validators.DataRequired()])
 lastName = StringField('Last Name', [validators.Length(min=1,max=150), validators.DataRequired()])
 email = StringField('Email', [validators.Length(min=1,max=150), validators.DataRequired()])
 gender = SelectField('Gender', [validators.DataRequired()],choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],default='')
 remarks = TextAreaField('Remarks', [validators.Optional()])
