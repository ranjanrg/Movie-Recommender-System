import pandas as pd

movies = pd.read_csv('movies.csv')
credits = pd.read_csv('credits.csv')

movies = movies.merge(credits, on = 'title')

unwanted_cols = ['budget', 'homepage', 'original_language', 'original_title', 'popularity', 'production_companies', 'production_countries','runtime', 'release_date', 'revenue', 'spoken_languages', 'status', 'tagline','vote_average', 'vote_count', 'movie_id']

movies = movies.drop(columns = unwanted_cols)

movies.dropna(inplace = True)




