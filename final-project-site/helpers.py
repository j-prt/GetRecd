import numpy as np
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms import FormField, FieldList
from wtforms.validators import DataRequired
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def get_recs(games, df, model, X, complexity, players):
    games_idx = list(df.loc[df.title.isin(games)].index.values)
    if len(games_idx) > 1:
        x = centroid(games_idx, X)
    else:
        x = X[games_idx[0]]
    if players == 1:
        df = df.loc[df.solo == 1]
    elif players == 2:
        df = df.loc[df.best_players == 2]
    if complexity == 1:
        df = df.loc[df.weight < 2]
    elif complexity == 2:
        df = df.loc[(df.weight >=2) & (df.weight < 4)]
    elif complexity == 3:
        df = df.loc[df.weight >= 4]
    recs = model.kneighbors(x.reshape(1, -1), 20, return_distance=False)[0]
    recs = df.loc[df.index.isin(recs) & ~df.index.isin(games_idx)][:5].to_dict()
        
    return recs

def get_games(game_list, titles):
    game_titles = []
    for game in game_list:
        if game == "":
            continue
        game_title = process.extractOne(
            game,
            titles,
            scorer=fuzz.token_sort_ratio)[0]
        game_titles.append(game_title)
    return game_titles


def centroid(games: list[int], X: np.ndarray) -> np.ndarray:
    """
    Calculate the centre of a list of points.
    
    Parameters:
    -----------
    games: list 
        List of indices of games the user likes
        
    Returns:
    --------
    np.ndarray 
        Vector containing the average of each dimension
    """
    
    if len(games) == 1:
        return X[games[0]]
    points = [X[game] for game in games]
    centroid = np.sum(points, axis=0) / len(points)
    return centroid

class GameForm(FlaskForm):
    game = StringField("🎲")

class MainForm(FlaskForm):
    games = FieldList(FormField(GameForm), min_entries=1, max_entries=5)
    players = RadioField(
        'Players',
        validators=[DataRequired()],
        choices=[(1, 'Solo-able'), (2, '2P'), (0, '2+')]
    )
    complexity = SelectField(
        'Complexity',
        validators=[DataRequired()],
        choices=[(0, "Any"), (1, "Simple"), (2, "Complex"), (3, "Confusing!")]
    )
    submit = SubmitField("#GetRec'd")


