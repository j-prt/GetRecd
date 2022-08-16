import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms import FormField, FieldList
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect
from helpers import MainForm, GameForm, get_games, get_recs, centroid

X = np.load('data/x_compact.npz')['X']
nn = NearestNeighbors(p=1, n_neighbors=10).fit(X)

df = pd.read_csv('data/data_compact.csv')
titles = set(df.title.values)

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['WTF_CSRF_ENABLED'] = False
app.jinja_env.globals.update(zip=zip) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():

    games = [{'game':''}, {'game':''}, {'game':''},
            {'game':''}, {'game':''}]
    form = MainForm(games=games)
    if form.validate_on_submit():
        complexity = int(request.form['complexity'])
        players = int(request.form['players'])
        games = [
            request.form['games-0-game'],
            request.form['games-1-game'],
            request.form['games-2-game'],
            request.form['games-3-game'],
            request.form['games-4-game']
        ]
        games = list(set(games))
        games = get_games(games, titles)
        recs = get_recs(games, df, nn, X, complexity, players)
        return render_template('results.html', recs=recs, games=games)

    return render_template('search.html', form=form)






if __name__ == '__main__':
    app.run(debug=True, port=5001)

    