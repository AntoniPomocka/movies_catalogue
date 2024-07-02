from flask import Flask, render_template, request
import tmdb_client
import random

app = Flask(__name__)

AVAILABLE_LISTS = ['popular', 'top_rated', 'now_playing', 'upcoming']

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route('/')
def homepage():
    list_type = request.args.get('list_type', 'popular')
    if list_type not in AVAILABLE_LISTS:
        list_type = 'popular'
    movies = tmdb_client.get_movies(list_type)
    random.shuffle(movies)
    movies = movies[:8]
    return render_template("homepage.html", movies=movies, current_list=list_type, available_lists=AVAILABLE_LISTS)

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    random_backdrop = tmdb_client.get_random_backdrop(movie_id)
    details['cast'] = cast
    details['random_backdrop'] = random_backdrop
    return render_template("movie_details.html", movie=details)

if __name__ == '__main__':
    app.run(debug=True)