from . import UserInput, MovieInput, TagInput, GenreInput
from agents import MovieLensAgent, get_agent

# Define a router hook for movies response that takes a movie input and an agent as dependencies and returns a movies response using the get_movies_response method of the agent
@app.post("/movies")
def movies_response(movie_input: MovieInput, agent: MovieLensAgent = Depends(get_agent)):
    # Get the movie_id from the movie input
    movie_id = movie_input.movie_id
    # Get the movies response from the agent
    movies_response = agent.get_movies_response(movie_id)
    # Return the movies response as JSON
    return movies_response
