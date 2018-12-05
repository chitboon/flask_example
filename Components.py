# adapted from https://github.com/chualc/Components
# use shelve instead of files

import shelve
from flask import Flask, render_template, request
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators

app = Flask(__name__)
data = shelve.open('data')

# This class determines the type of fields to be displayed on the web form
class webComponentsForm(Form):
    # An example of a text box
    strEg = StringField('Name', [validators.Length(min=1, max=5), validators.DataRequired()])

    # An example of a radio button with 2 choices. The default choice is Male
    radioEg = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')

    # An example of a drop down box with 5 choices
    dropDownBoxEg = SelectField('Preferred Language', [validators.DataRequired()],
                           choices=[('', 'Select'), ('C', 'C'), ('C++', 'C++'),
                                    ('Python', 'Python'), ('Java', 'Java'), ('Node.js', 'Node.js')],
                           default='')

    # An example of a text field
    synopsis = TextAreaField('Tell us about yourself')

# http://127.0.0.1:5000/ will display home.html
@app.route('/')
def home():
    return render_template('home.html')

# http://127.0.0.1:5000/webForm will display showWebForm.html
# If the submit button from the showWebForm is clicked, request.method == 'POST' will be True.
# The program will write/read to/from a file
@app.route('/webForm', methods=['POST', 'GET'])
def showWebForm():
    form = webComponentsForm(request.form)
    if request.method == 'POST' and form.validate():
        # Store the info persistence storage

        data['info'] =  [form.strEg.data, form.radioEg.data, form.dropDownBoxEg.data, form.synopsis.data]

        return render_template('table.html', readlist=data['info'])


    return render_template('showWebform.html', form=form)


if __name__ == '__main__':
    app.run(port='5000')
