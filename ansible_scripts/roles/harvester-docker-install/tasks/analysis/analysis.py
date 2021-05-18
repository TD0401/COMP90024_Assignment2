##### COMP90024 Cluster and Cloud Computing #####
##### Sentiment and Topic Analysis #####

#import required packages
import re
import json
import string
from pprint import pprint
import pandas as pd
import numpy as np
from functools import reduce

#import NLP packages
import nltk
from nltk.corpus import stopwords as stpwrd
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_selection import f_regression
from empath import Empath
from gensim import corpora
from gensim.models import TfidfModel
from gensim.models.ldamodel import LdaModel

#Download required datasets
nltk.download("stopwords")
nltk.download("vader_lexicon")
nltk.download("averaged_perceptron_tagger")

#Import plotting packages
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

#Import geometry packages
from geojson import Feature, FeatureCollection
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#ignore FutureWarnings
import warnings
warnings.filterwarnings("ignore", category = FutureWarning)

import couchdb
import json

def process_json(doc):
    parsed_lines = 0
    with open("victoriaTweet.json", "a+") as file:
        for row in doc:
            if -39.3 <= row['coordinates_lat'] <= -33.8:
                if 140.6 < row['coordinates_lng'] < 150.3:
                    file.writelines(json.dumps(row))
                    file.writelines(",\n")
                    parsed_lines += 1

    return parsed_lines


def main():
    couch_url = "http://admin:mrcpasswordcouch@172.26.134.25:5984/"
    couch = couchdb.Server(couch_url)
    row_limit = 5
    bookmark = None
    rows_parse = 0
    rows_fetch = 0
    error_count = 0
    with open("victoriaTweet.json", "a+") as file:
        file.writelines("[\n")
    while error_count < 3:
        try:

            mango_query = {
                "selector": {"coordinates_lat": {"$gt": -39.3}, "coordinates_lng": {"$ne": None}, "lang": {"$eq": "en"}},
                "fields": ["text", "coordinates_lat", "coordinates_lng"],
                "limit": row_limit,
                "bookmark": bookmark
            }
            print(mango_query)
            db = couch['twitterfeed']
            status, headers, data = db.resource.post_json('_find', mango_query)
            bookmark = data['bookmark']
            if data is not None and data['docs'] is not None and len(data['docs']) > 0:
                rows_fetch += len(data['docs'])
                rows_parse += process_json(data['docs'])
                print("total rows fetched :" + str(rows_fetch) + ", total rows parsed:" + str(rows_parse) + ", last bookmark:" + bookmark)
            else:
                print('last bookmark: ' + bookmark)
                break
        except:
            print("error in parsing rows : " + str(rows_fetch) + " - " + str(rows_fetch + row_limit) + ", last bookmark:" + bookmark)
            error_count += 1

    with open("victoriaTweet.json", "a+") as file:
        file.writelines("]\n")

main()


#define function for data extraction
def extract(file_path, col_index, col_name):
    """
    Function extracts data from provided file with standard geoJSON format
    
    Keyword Arguments:
    file_path -- path of file to extract
    col_index -- index of features to extract (should be in required order)
    col_name -- names of features (should follow col_index order)
    
    Returns: dataframe
    """
    #lga_code must be provided as a feature
    if "lga_code" not in col_name:
        return "ERROR - lga_code needs to be provided as feature"
    
    df = pd.read_json(file_path, lines = True)["features"]
    df = pd.json_normalize(df[0]).iloc[:, col_index]
    df.columns = col_name
    
    #extracts information only for LGAs within VIC
    df["lga_code"] = pd.to_numeric(df["lga_code"])
    df = df[df["lga_code"].between(20000, 29999, inclusive = True)]
    
    return df


#(i) Import requried data
twitter = pd.read_json("victoriaTweet.json")

#Extract AURIN datasets
aurin = {}
filename = {"worklife": "AURIN_datasets/adequate_worklife.json",\
            "sleep": "AURIN_datasets/inadequate_sleep.json",\
            "lacktime": "AURIN_datasets/lacking_time.json",\
            "pressure": "AURIN_datasets/time_pressure.json"}

for name, dataset in filename.items():
    col_index = np.r_[7,4,3,5,8]
    col_name = ["lga_code", "lga_name", name, "ci_high", "ci_low"]
    aurin[name] = extract(dataset, col_index, col_name)

aurin["income"] = extract("AURIN_datasets/personal_income.json", np.r_[3,4,2],\
    ["lga_code", "lga_name", "median_income"])

aurin["age"] = extract("AURIN_datasets/median_age.json", np.r_[7,4,5],\
    ["lga_code", "lga_name", "median_age"])

aurin["profile"] = extract("AURIN_datasets/lga_profile.json", np.r_[5,4,2,3,6:13],\
    ["lga_code", "lga_name", "unemploy_rate", "physical_activity", "not_yr12", "offences",\
        "good_facilities", "distress", "food_insecurity", "higher_edu", "poor_health"])

#Extract LGA polygons
aurin["lga_polygon"] = extract("AURIN_datasets/lga_regions.json", np.r_[4,7,3],\
    ["lga_code", "lga_name", "lga_polygon"])

#Merge extracted datasets into one df
data = reduce(lambda x,y: pd.merge(x, y, on = "lga_code", how = "left"),\
    [aurin["worklife"][["lga_code", "lga_name", "worklife"]], aurin["sleep"][["lga_code", "sleep"]],\
        aurin["lacktime"][["lga_code", "lacktime"]], aurin["pressure"][["lga_code", "pressure"]],\
            aurin["income"][["lga_code", "median_income"]], aurin["age"][["lga_code", "median_age"]],\
                aurin["profile"][["lga_code", "unemploy_rate", "physical_activity", "not_yr12", "offences",\
                    "good_facilities", "distress", "food_insecurity", "higher_edu", "poor_health"]],\
                        aurin["lga_polygon"][["lga_code", "lga_polygon"]]])

#(ii) Tokenize tweet text
def tokenize(df, stopwords):
    """
    Tokenizes tweet text, i.e. separates tweet text into individual tokens, while replacing 
    individual urls/numbers with "<url>" and "<number>" tags respectively and removing stopwords
    Tokenization performed using nltk TweetTokenizer() 
    
    Keyword Arguments:
    df -- dataframe of tweets
    stopwords -- list of stopwords to be removed during tokenization
    
    Returns: dataframe
    """
    tokenized_text = []
    tweet_tknzr = TweetTokenizer(preserve_case = False, reduce_len = True, strip_handles = True)
    for tweet in df["text"]:
        tokens = []
        for token in tweet_tknzr.tokenize(tweet):
            if re.search("http\S+", token): #replace urls with <url> tag
                tokens.append("<url>")
            elif re.search("^\d+", token): #replace any number with <number> tag
                tokens.append("<number>")
            elif token.lower() not in stopwords: #remove stopwords
                tokens.append(token)
        tokenized_text.append(tokens)

    df["tokenized_text"] = tokenized_text
    
    return df

#Peform tokenization of tweets
stopwords = stpwrd.words("english") + list(string.punctuation) + ["“", "”", "’", "...", "..", "…"]
twitter = tokenize(twitter, stopwords)
twitter["tokenized_text"] = twitter["tokenized_text"].apply(lambda tokens: " ".join(tokens))


##### Sentiment Analysis ##### 

#(i) Perform sentiment analysis using VADER
sid = SentimentIntensityAnalyzer()
#extract only compound sentiment polarity score
twitter["sentiment"] = twitter["tokenized_text"].apply(lambda text: sid.polarity_scores(text)["compound"])

#Plot distribution of sentiments scores
fig, ax = plt.subplots(figsize = (15, 10))
n_bins = 20
sns.distplot(twitter["sentiment"], bins = n_bins, color = "darkviolet", kde_kws = {"linewidth": 2})
ax.tick_params(axis = "both", labelsize = 14)
ax.set_xlabel("Sentiment", fontsize = 15, labelpad = 20)
ax.set_ylabel("Density", fontsize = 15, labelpad = 20)
plt.savefig("sentiment.jpg")

#Plot distribution of sentiments scores (without sentiment = 0) 
fig, ax = plt.subplots(figsize = (15, 10))
sns.distplot(twitter[twitter["sentiment"] != 0]["sentiment"], bins = n_bins, color = "darkgrey", kde_kws = {"linewidth": 2})
ax.tick_params(axis = "both", labelsize = 14)
ax.set_xlabel("Sentiment", fontsize = 15, labelpad = 20)
ax.set_ylabel("Density", fontsize = 15, labelpad = 20)
plt.savefig("sentiment_no0.jpg")


#(ii) Understand correlation and significance between features and sentiment
#Descriptive statistics for all features
print(round(data.describe(), 2))

#Plot heatmap of correlations between features
plt.figure(figsize = (14, 12))
plt.subplots(figsize = (20, 20))
ax = sns.heatmap(data.iloc[:, np.r_[2:17, 18]].corr(), square = True, annot = True, center = 0, \
    cmap = sns.diverging_palette(145, 280, s = 85, l = 25, n = 80))
plt.savefig("heatmap.jpg")

#Pair plots for selected features
sns.pairplot(data.iloc[:, np.r_[2:7,8,10,13,16,18]], kind = "reg",\
    plot_kws = {"line_kws": {"color": "#69479b"}}, corner = True)
plt.savefig("pairs.jpg")


#Perform F-test to test null hypothesis
data_dropna = data.dropna()
f_reg = f_regression(data_dropna.iloc[:, 2:17], data_dropna.iloc[:, 18])
print("F-values: ", f_reg[0])
print("p-values: ", f_reg[1])


#(iii) Calculate mean sentiment score per LGA
#Build LGA polygons
lga_polygon = {}
for lga in data.iterrows():
    lga_code = lga[1]["lga_code"]
    polygon = Polygon(lga[1]["lga_polygon"][0][0])
    lga_polygon[lga_code] = polygon
    
#Allocate tweets to individual LGAs
tweet_lga = {}
index = 0
for tweet in twitter.iterrows():
    point = Point(tweet[1]["coordinates_lng"], tweet[1]["coordinates_lat"])
    for code, polygon in lga_polygon.items():
        if polygon.contains(point): #checks if point is within polygon
            tweet_lga[index] = code
            continue
    index += 1

#Calculate mean sentiment score per LGA
twitter["lga_code"] = twitter.index.map(tweet_lga)
lga_meanSent = pd.DataFrame(twitter.groupby("lga_code")["sentiment"].mean().reset_index())
data = pd.merge(data, lga_meanSent, on = "lga_code", how = "outer")
print("LGA w data: ", data["sentiment"].count())


#(iv) Export geoJSON for choropleth
#Format data as geoJSON
features = data["lga_polygon"].apply(lambda row: Polygon(row[0][0])).to_dict()
properties = data.fillna("").drop(["lga_polygon"], axis = 1).to_dict("index")

feature_collection = []
for i in range(len(properties)):
    feature_collection.append(Feature(geometry = features[i], properties = properties[i]))

feature_collection = FeatureCollection(feature_collection)
#pprint(feature_collection)

#Export geoJSON as file
with open("choropleth.geojson", "w") as file:
    json.dump(feature_collection, file)


##### Topic Analysis #####

#(i) Lexical Categorisation
#Calculate lexical category scores of each tweet
twitter_dropNaN = twitter.dropna().copy()
lexicon = Empath()
twitter["category_scores"] = twitter_dropNaN["tokenized_text"].apply(lambda tweet: \
    lexicon.analyze(tweet, normalize = True))

#Extract most likely lexical category
def max_category(cat_scores):
    """
    Extracts category with maximum score from empath lexical categoriser outputs
    
    Keyword Arguments:
    cat_scores -- output from empath lexical categoriser (dict of topics and scores)
    
    Returns: empath category with max score
    """
    max_cat = max(cat_scores, key = cat_scores.get)
    
    #where all categories have score 0, supply None
    if (max_cat == "help") and (cat_scores["help"] == 0.0):
        max_cat = None
        
    return max_cat

twitter_dropNaN["max_category"] = twitter_dropNaN["category_scores"].apply(max_category)
#Output list of categories sorted by frequency count
print(twitter_dropNaN.groupby("max_category")["max_category"].count().sort_values(ascending = False))

#Extract top 10 topics/counts to JSON
twitter_dropNaN.groupby("max_category")["max_category"].count().sort_values(ascending = False).nlargest(10).to_json("top10_topics.json")


#(ii) Latent Dirichlet Allocation (LDA)
#Lemmatize tokenized tweet text
def lemmatize(text):
    """
    Lemmatizes tokenized tweet text, e.g. walking, walked, walks all return lemma walk
    Lemmatisation requires part-of-speech (POS) tag to return correct inflected form
    
    Keyword Arguments:
    text -- output from tokenized tweet text
    
    Returns: list of lemmas
    """
    text_lemma = []
    text = list(filter(None, text.split(" ")))
    for word, tag in pos_tag(text): #perform POS tagging using Penn Treebank corpus
        tag = tag[0].lower()
        #convert Penn Treebank tags to WordNet tags
        if tag.startswith("j"):
            tag = wordnet.ADJ
        elif tag.startswith("v"):
            tag = wordnet.VERB
        elif tag.startswith("n"):
            tag = wordnet.NOUN
        elif tag.startswith("r"):
            tag = wordnet.ADV
        else:
            tag = None

        lemma = nltk.stem.WordNetLemmatizer().lemmatize(word, pos = tag) if tag else word
        text_lemma.append(lemma)

    return text_lemma

twitter_dropNaN["lemmatize"] = twitter_dropNaN["tokenized_text"].apply(lemmatize)
print(twitter_dropNaN)

#Create term dictionary from tokenized text
num_topics = 10
dictionary = corpora.Dictionary(twitter_dropNaN["lemmatize"])

#Create document-term matrix, i.e. bag-of-word (BOW) corpus
bow_corpus = [dictionary.doc2bow(text) for text in twitter_dropNaN["lemmatize"]] #(word#, count)

#Create TF-IDF corpus
tfidf = TfidfModel(bow_corpus)
tfidf_corpus = tfidf[bow_corpus] #(word#, tf-idf)

#Train LDA model w BOW corpus
lda_bow = LdaModel(bow_corpus, num_topics = num_topics, id2word = dictionary, passes = 20)

#Train LDA model w TF-IDF corpus
lda_tfidf = LdaModel(tfidf_corpus, num_topics = num_topics, id2word = dictionary, passes = 20)

#Obtain top topics from trained LDA model
bow_topTopics = lda_bow.top_topics(bow_corpus)
tfidf_topTopics = lda_tfidf.top_topics(tfidf_corpus)

#LDA BOW Output
#UMass coherence (log of probabilities) = log[(D(Wi, Wj) + epsilon) / D(Wi)]
#Average topic coherence - sum of topic coherences of all topics, divided by the number of topics
avg_topicCoherence_bow = sum([topic[1] for topic in bow_topTopics]) / num_topics
print("Average Topic Coherence BOW: ", avg_topicCoherence_bow, "\n")
for index, topic in lda_bow.print_topics(-1):
    print('Topic: {} \nWord: {}\n'.format(index, topic))

print("-"*50)
    
#LDA TF-IDF Output
avg_topicCoherence_tfidf = sum([topic[1] for topic in tfidf_topTopics]) / num_topics
print("Average Topic Coherence TF-IDF: ", avg_topicCoherence_tfidf, "\n")
for index, topic in lda_tfidf.print_topics(-1):
    print('Topic: {} \nWord: {}\n'.format(index, topic))
