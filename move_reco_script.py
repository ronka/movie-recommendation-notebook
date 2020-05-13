import pandas as pd
import ast
from sklearn.cluster import KMeans
from sklearn import preprocessing
import dateutil
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


def get_values_from_genre_json(row, genre):
    movies_many_genres = ast.literal_eval(row['genres'])
    movies_genres = []
    for item in movies_many_genres:
        movies_genres.append(item['name'])
    if genre in movies_genres:
        return 1
    else:
        return 0


def check(row):
    if not type(row) == str:
        return row
    else:
        return None


def main():
    df = pd.read_csv('https://www.dropbox.com/s/j9vxjw3g1s7wqsg/movies_metadata.csv?dl=1')
    df = df[['id', 'imdb_id', 'title', 'budget', 'revenue', 'genres', 'runtime', 'release_date', 'vote_average',
             'vote_count', 'popularity']]
    genres_list = set()
    for index, value in df['genres'].iteritems():
        movies_genres = ast.literal_eval(value)
        for item in movies_genres:
            genres_list.add(item['name'])
    genres_list = list(genres_list)

    for genre in genres_list:
        df[genre] = df.apply(lambda x: get_values_from_genre_json(x, genre), axis=1)

    df = df.drop(columns=['genres', 'id', 'imdb_id', 'title', 'popularity'])
    df = df.dropna(subset=['release_date'])
    df = df[df['popularity'] != 'Beware Of Frost Bites']
    df['release_date'] = df['release_date'].apply(dateutil.parser.parse)

    columns = ['release_date']

    # Set concoder
    encoder = LabelEncoder()

    # Encode data frame
    encoded_df = df.copy()
    for col in columns:
        encoded_df[col] = encoder.fit_transform(df[col])

    y_pred = KMeans(n_clusters=2, random_state=0).fit(encoded_df)
    plt.subplot(221)
    plt.scatter(df, df, c=y_pred)
    plt.title("Incorrect Number of Blobs")


if __name__ == '__main__':
    main()
