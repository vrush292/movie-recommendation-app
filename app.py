from flask import Flask, request, jsonify, render_template
import numpy as np 
import pandas as pd 
import difflib #for mistakes in input
from sklearn.feature_extraction.text import TfidfVectorizer #text to numerical data
from sklearn.metrics.pairwise import cosine_similarity #similarity comparing for recommendation

#loading data from csv file to pandas dataset
movies_data=pd.read_csv('bollywood.csv')

#selecting relevant features and creating dataset
selected_features=['genre','overview','director','cast']
#replacing missing values
for feature in selected_features:
    movies_data[feature]=movies_data[feature].fillna('')

#created selected features dataset
combined_features=movies_data['genre']+movies_data['overview']+movies_data['director']+movies_data['cast']

#converting text to feature vectors i.e numeric data
vectorizer=TfidfVectorizer()
feature_vectors=vectorizer.fit_transform(combined_features)

#getting similarity using cosine similarity
similarity=cosine_similarity(feature_vectors)

#getting movie name from user

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Make sure your HTML file is named index.html

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()  # Get the JSON data sent from the frontend
    movie_name = data.get('title')  # Extract the movie title from the data
    list_of_all_titles=movies_data['movie_name']

    #finding close match for user movie
    find_close_match=difflib.get_close_matches(movie_name,list_of_all_titles)
    if not find_close_match:  # Check if the list is empty
        return jsonify({"recommendations": []})  # Return an empty recommendations list

    close_match=find_close_match[0]

    #finding index of movie
    index_of_movie=movies_data[movies_data.movie_name==close_match]['index'].values[0]

    #getting list of similar movies
    similarity_score=list(enumerate(similarity[index_of_movie]))

    #sorting list based on similarity score
    sorted_similar_movies=sorted(similarity_score,key=lambda x:x[1],reverse=True)

    #recommending movies list
    recommendations=list()
    i=0;
    for movie in sorted_similar_movies:
        if(i==0):
            i=1
            continue
        index=movie[0]
        title_from_index=movies_data[movies_data.index==index]['movie_name'].values[0]
        if(i<4):
            recommendations.append(title_from_index)
            i=i+1
    print(recommendations)
    return jsonify({"recommendations": recommendations})  # Return recommendations as JSON

if __name__ == '__main__':
    app.run(debug=True)