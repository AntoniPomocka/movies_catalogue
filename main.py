from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    movies = [
        {
            "poster_url": "http://placehold.it/300x500",
            "title": "Tytuł filmu 1",
            "description": "Opis filmu 1",
            "url": "/movie/1"
        },
        {
            "poster_url": "http://placehold.it/300x500",
            "title": "Tytuł filmu 2",
            "description": "Opis filmu 2",
            "url": "/movie/2"
        },
        {
            "poster_url": "http://placehold.it/300x500",
            "title": "Tytuł filmu 3",
            "description": "Opis filmu 3",
            "url": "/movie/3"
        },
        {
            "poster_url": "http://placehold.it/300x500",
            "title": "Tytuł filmu 4",
            "description": "Opis filmu 4",
            "url": "/movie/4"
        },
    ]
    return render_template("homepage.html", movies=movies)

if __name__ == '__main__':
    app.run(debug=True)