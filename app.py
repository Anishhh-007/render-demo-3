from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the model and data
with open('movie_recommender.pkl', 'rb') as f:
    new_data, sim, cv = pickle.load(f)

def recommended(movie):
    # Find the index of the given movie
    abel_index = new_data[new_data['title'].str.strip() == movie].index

    # Check if the movie exists
    if abel_index.empty:
        return []

    # Get the first index (assuming there's only one)
    abel_index = abel_index[0]

    # Get the distances for the specified movie
    distance = sim[abel_index]

    # Get the indices of the top 5 most similar movies, excluding the first one (itself)
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    # Return the titles of the recommended movies
    return new_data['title'].iloc[[i[0] for i in movies_list]].tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    recommendations = recommended(movie_title.title())
    return render_template('index.html', recommendations=recommendations, movie_title=movie_title)

if __name__ == '__main__':
    app.run(debug=True)
