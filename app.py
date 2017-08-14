from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms.fields import TextField, SubmitField, SelectField
from wtforms.validators import NumberRange, InputRequired
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' #this is to protect from CSRS attacks the string must be a secret word
data = pd.read_csv('quests.csv', sep=";", encoding='cp1251')
rated = data[data[u'Атмосфера']>0].values
choices = rated[:,1].tolist()

class TextInput(Form):
    questname = SelectField(label='Название квеста', choices=[(f, f) for f in sorted(choices)])
    number = TextField(u'Число квестов:')
    submit = SubmitField(u'Показать')

@app.route('/', methods=['GET','POST'])
def index():
    errmsg = ''
    form = TextInput()
    if request.method == 'POST':
        req = form.questname.data
        if str(form.number.data).isdigit() == False or int(form.number.data) not in range(1,460):
            errmsg = u'Ошбка, Число квестов должно быть 0 до 460'
            return render_template('index.html', form=form, errmsg=errmsg)
        numb = int(form.number.data)
        rest =  rated[np.where(rated[:,1] != req)][:,0:10]
        model = rated[np.where(rated[:,1] == req)][0,0:10]
        dist_2 = []
        for i in range(len(rest[:,4:10])):
            dist_2.append([sum((model[4:]-rest[:,4:10][i])**2)/len(rest[:,4:10][i]),i])
        output = []
        url = []
        for i in range(numb):
            output.append(rest[min(sorted(dist_2)[i:])[1]][1])
            url.append('http://questguild.ru/quests/'+
                        str(rest[min(sorted(dist_2)[i:])[1]][3]))
        return result(output=output, url=url, req=req)
    return render_template('index.html', form=form, errmsg=errmsg)

@app.route('/result')
def result(output, url, req):
    return render_template('result.html', output=output, url=url, req=req)

#if __name__ == '__main__':
#    app.run( debug=True)
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
