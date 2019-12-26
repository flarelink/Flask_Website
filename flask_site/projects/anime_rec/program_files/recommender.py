import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_site.projects.anime_rec.program_files.utils import scrape_user_data_from_username


# Helper functions
def get_name_from_id(df, id):
    """
    Get the anime name using the dataframe and anime id

    :param df: (pd.Dataframe) anime dataframe
    :param id: (int) anime id
    :return: (str) anime name
    """
    return df[df.animeID == id]["name"].values[0]


def get_id_from_name(df, name):
    """
    Get the anime id using the dataframe and anime name

    :param df: (pd.Dataframe) anime dataframe
    :param name: (str) anime name
    :return: (int) anime id
    """
    return df[df.name.str.lower() == name.lower()]["animeID"].values[0]


def combine_features(row, features, bad_chars):
    """
    Combine desired features for each row in the dataframe and filter out bad characters

    :param row: (pd row) the current row of the dataframe being assessed
    :param features: (list of str) the desired columns from dataframe
    :param bad_chars: (str trans) characters to drop from string
    :return: (str) combined features
    """
    features_string = ''
    for f in features:
        features_string += row[f] + ' '
    features_string = features_string.translate(bad_chars)
    return features_string[:-1]  # don't want the last space


# Main function
def content_based(args):
    """
    Content based recommendation using cosine similarity and sorting relative to anime scores

    :param args: input arguments containing: dataset_path, username, watching_list, sel_anime, num_recs, anime_images
    :return: (list of str, list of str, str) recommendations list, image references list, and selected anime
    """
    # load data into Dataframe
    anime_df = pd.read_csv(args.dataset_path)
    anime_df.columns = anime_df.columns.str.lstrip()  # there was a space in the anime csv column header

    # save means before stripping NaNs
    scored_mean = anime_df['scored'].mean()
    anime_df = anime_df.fillna(0)

    # single user anime list extracted
    user_df = scrape_user_data_from_username(args.username, args.watching_list)
    user_animes_seen = {}
    if not user_df.empty:
        user_animes_seen = user_df.set_index('animeID').to_dict()['scored']

    # anime to recommend based off of
    sel_anime = args.sel_anime

    if sel_anime.lower() in anime_df['name'].str.lower().values:
        sel_anime_id = get_id_from_name(anime_df, sel_anime)
        sel_anime = get_name_from_id(anime_df, sel_anime_id)
    else:
        sel_anime_id = 1  # default to Cowboy Bepop if incorrect name
        sel_anime = 'Cowboy Bepop'

    # save sel_anime row
    sel_anime_df_row = anime_df.loc[(anime_df['animeID'] == sel_anime_id)]

    # cutting data out for memory purposes and biasing
    anime_df = anime_df[anime_df.scored > scored_mean]
    anime_df = anime_df.append(sel_anime_df_row)
    anime_df = anime_df.reset_index(drop=True)

    sel_anime_index = anime_df.loc[(anime_df['animeID'] == sel_anime_id)].index[0]

    # combine features to utilize in count/similarity matrices
    features = ['genre', 'type', 'studios']
    bad_chars = str.maketrans(dict.fromkeys("[]',"))
    anime_df['sim_features'] = anime_df.apply(combine_features, args=(features, bad_chars,), axis=1)

    # Let's grab a count matrix of animes that have similar features and then use cosine similarity on that matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(anime_df['sim_features'])
    sim_matrix = cosine_similarity(count_matrix)

    # Now we sort the similar animes; ignore the first entry because it'll be the same anime specified
    similar_animes = list(enumerate(sim_matrix[sel_anime_index]))
    similar_animes_sorted = sorted(similar_animes, key=lambda x: x[1], reverse=True)[1:args.num_recs * 20]

    # Instead of just taking the most similar anime recommendation, let's instead sort them by the
    # animes that score the best relative to the number of people that scored

    # shrinkage estimator
    # https://stats.stackexchange.com/questions/6418/rating-system-taking-account-of-number-of-votes
    scoredBy_mean = anime_df['scoredBy'].mean()
    scored_mean = anime_df['scored'].mean()
    anime_df['norm_score'] = (anime_df['scoredBy'] / (anime_df['scoredBy'] + scoredBy_mean)) * anime_df['scored'] +\
                             (scoredBy_mean / (anime_df['scoredBy'] + scoredBy_mean)) * scored_mean
    similar_animes_norm_score = sorted(similar_animes_sorted, key=lambda x: anime_df['norm_score'][x[0]], reverse=True)

    # Loop through to collect the anime ids from the recommendations
    # If the anime id is already in the user's completed animes, then ignore it and get a different recommendation
    recommendations = []
    rec_img_urls = []
    i = 0

    # for anime in similar_animes_sorted:  # sort only based on similarity
    for anime in similar_animes_norm_score:  # sort based off similarity and normalized score

        anime_id = anime_df.iloc[anime[0], 0]

        if anime_id not in user_animes_seen and anime_id != sel_anime_id:
            anime_name = get_name_from_id(anime_df, anime_id)
            recommendations.append(anime_name)
            rec_img_urls.append(os.path.join(args.anime_images, str(anime_id) + '.jpg'))
            i += 1
        if i > args.num_recs - 1:
            break

    return recommendations, rec_img_urls, sel_anime
