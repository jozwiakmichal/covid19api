from flask import Flask, render_template
import pandas as pd
import requests
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response

class SiteUtils():
    def requestActiveCovidCases(self):
        infections = requests.get("https://api.covid19api.com/country/poland")
        return infections

    def prepareData(self):
        infections = self.requestActiveCovidCases()

        df = pd.read_json(infections.content)
        return df

    def createFigure(self):
        df = self.prepareData()

        plot = df['Active'].plot(colormap='jet', marker='.', title="Przypadki koronawirusa w Polsce")
        plot.set_xlabel("Dni")
        plot.set_ylabel("Liczba przypadków")

        return plot.get_figure()

app=Flask(__name__)
utils=SiteUtils()

@app.route('/home')
def home():
    return "Witam!"

@app.route('/home/<string:name>')
def helloYou(name):
    return "Witam serdecznie, " + name

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/active.html')
def active():
    return render_template('aktywne.html')

@app.route('/plot.png')
def plot_png():
    fig = utils.createFigure()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__=="__main__":
    app.run(debug=True)