from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms.fields import TextField, SubmitField
from wtforms.validators import NumberRange
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!' #this is to protect from CSRS attacks the string must be a secret word
data = pd.read_csv('quests.csv', sep=";", encoding='cp1251')
rated = data[data[u'Атмосфера']>0].values

class TextInput(Form):
    questname = TextField(u'Название квеста:', [InputRequired()])
    number = TextField(u'Число квестов:', [InputRequired()])
    submit = SubmitField(u'Показать')

    def validate_number(form):
        if int(form.number.data) <= 0 or int(form.number.data) > 460:
            raise ValidationError(u'Пожалуйста, введите число между 0 и 460')

@app.route('/', methods=['GET','POST'])
def index():
    form = TextInput()
    if request.method == 'POST':
        req = form.questname.data
        numb = int(form.number.data)
        rest =  rated[np.where(rated[:,1] != req)][:,0:10]
        model = rated[np.where(rated[:,1] == req)][0,0:10]
        dist_2 = []
        for i in rest[:,4:10]:
            dist_2.append(sum((model[4:]-i)**2)/len(i))
        output = []
        url = []
        for i in range(numb):
            output.append(rest[dist_2.index(min(sorted(dist_2)[i:]))][1])
            url.append('http://questguild.ru/quests/'+
                        str(rest[dist_2.index(min(sorted(dist_2)[i:]))][3]))
        return result(output=output, url=url, req=req)
    return render_template('index.html', form=form)

@app.route('/result')
def result(output, url, req):
    return render_template('result.html', output=output, url=url, req=req)

#if __name__ == '__main__':
#    app.run( debug=True)
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
