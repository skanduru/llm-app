import tecton
from tecton import Template, SequentialChain, RouterChain
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from .agents.movieAgent import get_agent, MovieLensAgent
from . import UserInput


# Define a dependency function that returns a MovieLensAgent object with the repository, context, and api_key as arguments

# Define a router hook for movie recommendations based on sequential and router chains that takes a user input and an agent as dependencies and returns a struct of user, movies and ratings in descending order using the get_ratings_feature_vector and lookup_movie methods of the repository and the get_response method of the agent
@app.post("/recommendations/chain")
def recommendations_chain(user_input: UserInput, agent: MovieLensAgent = Depends(get_agent)):
    # Get the user_id from the user input
    user_id = user_input.user_id
    # Get the ratings feature vector for the user_id from the repository
    ratings_fv = agent.repository.get_ratings_feature_vector(user_id)
    # Get the movie ids and ratings from the feature vector
    movie_ids = ratings_fv.get_value("movie_id")
    ratings = ratings_fv.get_value("rating")
    # Sort the movie ids by ratings in descending order
    sorted_movie_ids = sorted(movie_ids, key=lambda x: ratings[x], reverse=True)
    # Get the top 10 movie ids
    top_movie_ids = sorted_movie_ids[:10]
    # Get the movie titles and genres for each movie id using the lookup_movie method of the repository
    movies = [agent.repository.lookup_movie(movie_id) for movie_id in top_movie_ids]
    # Format the movies as a list of strings with title and genres separated by comma
    movies_str = [f"{title}, {genres}" for title, genres in movies]
    # Join the movies with newline character
    movies_nl = "\n".join(movies_str)
    
    # Define a sequential chain that takes a user_id as input and returns a prompt for ratings based on relevance per user using the ratings_prompt_per_user method of the template
    ratings_chain = SequentialChain(
        name="ratings_chain",
        description="A chain that returns a prompt for ratings based on relevance per user",
        input=user_id,
        output=agent.template.ratings_prompt_per_user(user_id)
    )
    
    # Define a router chain that takes a movie_id as input and returns a prompt for movies based on relevance per tag using the movies_prompt_per_tag method of the template or a response using the get_response method of the agent depending on the most probable token from the previous chain
    movies_chain = RouterChain(
        name="movies_chain",
        description="A chain that returns a prompt for movies based on relevance per tag or a response depending on the most probable token",
        input=movie_id,
        output={
            "Yes": agent.template.movies_prompt_per_tag(movie_id),
            "No": agent.get_response(ratings_chain.output)
        },
        condition=ratings_chain.most_probable_token
    )
    
    # Return a dictionary with user_id, movies_nl, ratings_chain.output, and movies_chain.output as keys and values as JSON
    return {
        "user_id": user_id,
        "movies": movies_nl,
        "ratings_prompt": ratings_chain.output,
        "movies_prompt_or_response": movies_chain.output
    }
