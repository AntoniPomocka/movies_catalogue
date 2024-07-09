import pytest
from unittest.mock import Mock
import tmdb_client
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_single_movie(monkeypatch):
    mock_single_movie = {'title': 'The Matrix'}

    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_single_movie

    monkeypatch.setattr("requests.get", requests_mock)

    movie = tmdb_client.get_single_movie(movie_id=603)
    assert movie == mock_single_movie
    requests_mock.assert_called_once_with("https://api.themoviedb.org/3/movie/603?api_key=47035f2a1486621c8368dfe3f027f867&language=en-US")

def test_get_single_movie_cast(monkeypatch):
    mock_cast = [{'name': 'Keanu Reeves', 'character': 'Neo'}]

    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = {'cast': mock_cast}

    monkeypatch.setattr("requests.get", requests_mock)

    cast = tmdb_client.get_single_movie_cast(movie_id=603)
    assert cast == mock_cast
    requests_mock.assert_called_once_with("https://api.themoviedb.org/3/movie/603/credits?api_key=47035f2a1486621c8368dfe3f027f867&language=en-US")

def test_get_random_backdrop(monkeypatch):
    mock_backdrop_path = '/path/to/backdrop.jpg'
    mock_movie_images = {'backdrops': [{'file_path': mock_backdrop_path}], 'posters': []}

    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movie_images

    monkeypatch.setattr("requests.get", requests_mock)

    backdrop = tmdb_client.get_random_backdrop(movie_id=603)
    assert backdrop == mock_backdrop_path
    requests_mock.assert_called_once_with("https://api.themoviedb.org/3/movie/603/images?api_key=47035f2a1486621c8368dfe3f027f867&language=en-US")

def test_movie_details_endpoint(client, monkeypatch):
    mock_single_movie = {
        'id': 603,
        'title': 'The Matrix',
        'tagline': 'Welcome to the Real World',
        'overview': 'A computer hacker learns about the true nature of reality.',
        'budget': 63000000,
        'genres': [{'name': 'Action'}, {'name': 'Sci-Fi'}],
        'vote_average': 8.1,
        'release_date': '1999-03-31',
        'cast': [{'name': 'Keanu Reeves', 'character': 'Neo', 'profile_path': '/profile.jpg'}],
        'backdrop_path': '/path/to/backdrop.jpg'
    }

    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_single_movie

    def mock_get(url, *args, **kwargs):
        if 'credits' in url:
            return Mock(json=lambda: {'cast': mock_single_movie['cast']})
        elif 'images' in url:
            return Mock(json=lambda: {'backdrops': [{'file_path': mock_single_movie['backdrop_path']}]})
        return Mock(json=lambda: mock_single_movie)

    monkeypatch.setattr("requests.get", mock_get)

    movie_id = 603
    response = client.get(f'/movie/{movie_id}')
    assert response.status_code == 200
    assert b'The Matrix' in response.data
    assert b'Welcome to the Real World' in response.data
    assert b'A computer hacker learns about the true nature of reality.' in response.data
    assert b'$63,000,000.00' in response.data
    assert b'Action' in response.data
    assert b'Sci-Fi' in response.data
    assert b'8.1' in response.data
    assert b'1999-03-31' in response.data
    assert b'Keanu Reeves' in response.data
    assert b'Neo' in response.data
    assert b'/path/to/backdrop.jpg' in response.data