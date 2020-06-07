import pandas as pd
import ast


def main():
    movies_raw_df = pd.read_csv('movies.csv')
    ratings_raw_df = pd.read_csv('ratings.csv')

    # First we set a new df to be a proper and cleaner set, we keep only the genres, ids and titles of the movie.

    generes_df = movies_raw_df.loc[:, ('genres', 'title', 'id')]
    generes_df.drop_duplicates(['id'], inplace=True)
    generes_df.dropna()

    """
    Preparing our genres column for usage
    Genres are stored as JSONs in our dataset, lets convert to it to hot-one format
    """
    genres_list = set()
    for index, row in generes_df.iterrows():  # Todo its a bad practice to use iterrows
        # extract genres
        movies_genres = ast.literal_eval(row['genres'])
        for genre in movies_genres:
            # if genre is not a column, generate the column and set all to 0
            if genre['name'] not in generes_df:
                genres_list.add(genre['name'])
                generes_df[genre['name']] = 0
            generes_df.at[index, genre['name']] = 1
    generes_df.drop(columns=['genres'], inplace=True)
    generes_df.set_index('id', inplace=True)

    # Now for every user we will its genres ratings

    genres = list(generes_df.drop(columns=['title']).columns)
    genre_ratings = pd.DataFrame()
    for genre in genres:
        genre_movies = generes_df[generes_df[genre] == 1]
        avg_genre_votes_per_user = ratings_raw_df[ratings_raw_df['movieId'].isin(
            genre_movies.index)].loc[:, ['userId', 'rating']].groupby(
            ['userId'])['rating'].mean().round(2)
        genre_ratings = pd.concat([genre_ratings, avg_genre_votes_per_user], axis=1)
    genre_ratings.columns = genres
    print(genre_ratings.head())
    print(genre_ratings.shape)


if __name__ == '__main__':
    main()
