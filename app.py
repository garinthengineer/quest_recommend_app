from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)
data = pd.read_csv('quests.csv', sep=";", encoding='cp1251')
rated = data[data[u'Атмосфера']>0].values

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        req = str(request.form['questname'])
        numb = int(request.form['number'])
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
    return render_template('index.html')

@app.route('/result')
def result(output, url, req):
    return render_template('result.html', output=output, url=url, req=req)

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
