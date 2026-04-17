import pandas as pd
import ast

movies = pd.read_csv('movies.csv')
credits = pd.read_csv('credits.csv')

movies = movies.merge(credits, on = 'title')

unwanted_cols = ['budget', 'homepage', 'original_language', 'original_title', 'popularity', 'production_companies', 'production_countries','runtime', 'release_date', 'revenue', 'spoken_languages', 'status', 'tagline','vote_average', 'vote_count', 'movie_id']

movies = movies.drop(columns = unwanted_cols)

movies.dropna(inplace = True)

# In my dataset columns like overview cast, crew etc.. are in wierd format. I have to convert them into list. so in my current setup format is string of lists so what i'm going to do is use the function convert to go through the obj= the column and extract the weired format to list of strings.

def convert(obj):
  l = []
  for i in ast.literal_eval(obj):
    l.append(i['name'])
  return l

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

# This function helps to extrect top three cast name from the cast column.

def convert_cast(obj):
  l = []
  counter = 0
  for i in ast.literal_eval(obj):
    if counter != 3:
      l.append(i['name'])
      counter += 1
    else:
      break
  return l


movies['cast'] = movies['cast'].apply(convert_cast)

# This function helps in fetching the director name from the big column crew
def fetch_director(obj):
  l = []
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      l.append(i['name'])
      break
  return l

movies['crew'] = movies['crew'].apply(fetch_director)

# this function converts our overview column which is string into list
movies['overview'] = movies['overview'].apply(lambda x:x.split())

# this function will helps us to remove the space between 2 entities of a same word

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ", "") for i in x])

# concatenating all the columns to create new column named tags

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['id', 'title', 'tags']]




