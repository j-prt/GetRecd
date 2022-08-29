# Overview

This was my final project submission for [Concordia Bootcamps'](https://concordiabootcamps.ca/) Data Science program.  
If you want to skip ahead to the final product: view [the site](https://ds-bc-final.herokuapp.com/)!


The project is a board game recommendation engine based on data scraped from [BoardGameGeek](https://boardgamegeek.com), which is kind of like a wiki for board games. They have a comprehensive collection of first-party data and community-based metrics around games in the database, which made it a great source for feature engineering. After a collecting data and cleaning it, a K-Nearest Neighbors model is used to identify similar games based on distance in the vector space.

# Project Details

<div align="center">
<h3>User names 1-5 games</h3>
<img src="Screen Shot 2022-08-27 at 20.58.17.png"/>
<h3>System recommends up to 5 games based on selected parameters</h3>
<img src="Screen Shot 2022-08-27 at 20.59.30.png"/>
</div>

## Data Collection
See also: [data collection Jupyter Notebook](/data-collection.ipynb)

Data scraped from BGG based on their top rankings pages. Scraped from 3 source pages over 2+ days. 

Tools:
- pandas
- requests
- BeautifulSoup
- json
- re

## Modelling
See also: [preprocessing and modelling Jupyter Notebook](/preprocessing_modelling_v2.ipynb)

Data collected is cleaned (NaN values filled, datatypes converted), some feature engineering is done, and processed data is then fed to the [model](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html).

Tools:
- pandas
- NumPy
- scikit-learn
- K-Nearest Neighbors
- Binarization
- TF-IDF
- K-Means
- PCA

## Deployment
See also: [the live site](https://ds-bc-final.herokuapp.com/)

Finally, I built a simple static site to accept input games and produce recommendations. It uses a Bootstrap-based frontend with a Flask backend. Users are able to tweak their recommendations based on number of players and complexity (as a function of BGG's user-generated "weight" score for games). Uses fuzzy matching based on [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to interpret queries. 

Tools:
- Flask
- Bootstrap
- WTForms
- [TheFuzz](https://github.com/seatgeek/thefuzz)
- Heroku
