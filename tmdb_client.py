import requests
import random

API_KEY = '47035f2a1486621c8368dfe3f027f867'

def get_movies(list_name):
    url = f"https://api.themoviedb.org/3/movie/{list_name}?api_key={API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["results"]

def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_single_movie(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_single_movie_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["cast"]

def get_random_backdrop(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    response.raise_for_status()
    backdrops = response.json()["backdrops"]
    if backdrops:
        random_backdrop = random.choice(backdrops)
        return random_backdrop["file_path"]
    else:
        return None