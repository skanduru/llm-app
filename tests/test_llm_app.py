import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a TestClient object using the app object
client = TestClient(app)

# Define a list of user ids for testing
user_ids = [1, 2, 3, 4, 5]

# Define a list of movie ids for testing
movie_ids = [1, 2, 3, 4, 5]

# Define a list of tags for testing
tags = ["Action", "Adventure", "Comedy", "Drama", "Romance"]

# Define a list of genres for testing
genres = ["Action|Adventure|Sci-Fi", "Comedy|Romance", "Drama|Thriller", "Horror|Mystery", "Animation|Family"]

# Define a pytest fixture that returns a user input object for each user id
@pytest.fixture(params=user_ids)
def user_input(request):
    return {"user_id": request.param}

# Define a pytest fixture that returns a movie input object for each movie id
@pytest.fixture(params=movie_ids)
def movie_input(request):
    return {"movie_id": request.param}

# Define a pytest fixture that returns a tag input object for each tag
@pytest.fixture(params=tags)
def tag_input(request):
    return {"tag": request.param}

# Define a pytest fixture that returns a genre input object for each genre
@pytest.fixture(params=genres)
def genre_input(request):
    return {"genre": request.param}

# Define a test function that tests the ratings response router hook using the user input fixture and asserts that the response status code is 200 and the response json contains the expected keys and values
def test_ratings_response(user_input):
    # Make a POST request to the ratings endpoint with the user input as json data
    response = client.post("/ratings", json=user_input)
    # Assert that the response status code is 200
    assert response.status_code == 200
    # Get the response json as a dictionary
    response_dict = response.json()
    # Assert that the response json contains the user_id key and value
    assert response_dict["user_id"] == user_input["user_id"]
    # Assert that the response json contains the movies key and value is a list of strings
    assert isinstance(response_dict["movies"], list)
    assert all(isinstance(movie, str) for movie in response_dict["movies"])
    # Assert that the response json contains the ratings_prompt key and value is a string
    assert isinstance(response_dict["ratings_prompt"], str)

# Define a test function that tests the movies response router hook using the movie input fixture and asserts that the response status code is 200 and the response json contains the expected keys and values
def test_movies_response(movie_input):
    # Make a POST request to the movies endpoint with the movie input as json data
    response = client.post("/movies", json=movie_input)
    # Assert that the response status code is 200
    assert response.status_code == 200
    # Get the response json as a dictionary
    response_dict = response.json()
    # Assert that the response json contains the movies key and value is a list of dictionaries with title, genres, and rating_count keys and values
    assert isinstance(response_dict["movies"], list)
    assert all(isinstance(movie, dict) for movie in response_dict["movies"])
    assert all("title" in movie and isinstance(movie["title"], str) for movie in response_dict["movies"])
    assert all("genres" in movie and isinstance(movie["genres"], str) for movie in response_dict["movies"])
    assert all("rating_count" in movie and isinstance(movie["rating_count"], int) for movie in response_dict["movies"])

# Define a test function that tests the recommendations chain router hook using the user input fixture and asserts that the response status code is 200 and the response json contains the expected keys and values
def test_recommendations_chain(user_input):

