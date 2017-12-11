from flask import Flask, render_template, request
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'file')


# This class determines the type of fields to be displayed on the web form
class webComponentsForm(Form):
    # An example of a text box
    strEg = StringField('A string', [validators.Length(min=1, max=150), validators.DataRequired()])

    # An example of a radio button with 2 choices. The default choice is rChoice1
    radioEg = RadioField('Eg of Radio Button', choices=[('rChoice1', 'First'), ('rChoice2', 'Second')], default='rChoice1')

    # An example of a drop down box with 5 choices
    dropDownBoxEg = SelectField('Eg of Dropdown Box', [validators.DataRequired()],
                           choices=[('', 'Select'), ('FANTASY', 'Fantasy'), ('FASHION', 'Fashion'),
                                    ('THRILLER', 'Thriller'), ('CRIME', 'Crime'), ('BUSINESS', 'Business')],
                           default='')

    # An example of a text field
    synopsis = TextAreaField('Synopsis')

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
        # Store the info in write.txt
        # Use 'a' which stands for 'append' if you do not
        # want to override the previous content
        fwrite = open('C:/Users/CQZ/PycharmProjects/Flask/Sample/Components/file/write.txt', 'w')
        textList = [form.strEg.data+"\n", form.radioEg.data+"\n", form.dropDownBoxEg.data+"\n", form.synopsis.data+"\n"]
        fwrite.writelines(textList)
        fwrite.close()

        # Read info from either readdata1.txt or readdata2.txt depending on the radio button selected by user
        readlist = []
        if form.radioEg.data == 'rChoice1':
            path = 'readdata1.txt'
        else:
            path = 'readdata2.txt'

        fread = open(os.path.join(APP_STATIC, path), 'r')
        for line in fread:
            readlist.append(line)
        fread.close()

        return render_template('table.html', readlist=readlist)


    return render_template('showWebform.html', form=form)


if __name__ == '__main__':
    app.run()
