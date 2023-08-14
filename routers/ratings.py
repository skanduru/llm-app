from . import UserInput, MovieInput, TagInput, GenreInput
from agents import MovieLensAgent, get_agent

# Define a router hook for ratings response that takes a user input and an agent as dependencies and returns a ratings response using the get_ratings_response method of the agent
@app.post("/ratings")
def ratings_response(user_input: UserInput, agent: MovieLensAgent = Depends(get_agent)):
    # Get the user_id from the user input
    user_id = user_input.user_id
    # Get the ratings response from the agent
    ratings_response = agent.get_ratings_response(user_id)
    # Return the ratings response as JSON
    return ratings_response
