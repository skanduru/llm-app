from . import UserInput, MovieInput, TagInput, GenreInput
from agents import MovieLensAgent, get_agent

from fastapi import APIRouter

router = APIRouter()

# Define a router hook for movie recommendations for a given user that takes a user input and an agent as dependencies and returns a struct of user, movies and ratings in descending order using the get_ratings_feature_vector and lookup_movie methods of the repository
@app.post("/recommendations/user")
def recommendations_user(user_input: UserInput, agent: MovieLensAgent = Depends(get_agent)):
    # Get the user_id from the user input
    user_id = user_input.user_id
    # Get the ratings feature vector for the user_id from the repository
    ratings_fv = agent.repository.get_ratings_feature_vector(user_id)
    # Get the movie ids and ratings from the feature vector
    movie_ids = ratings_fv.get_value("movie_id")
    ratings = ratings_fv.get_value("rating")
    # Sort the movie ids by ratings in descending order
    sorted_movie_ids = sorted(movie_ids, key=lambda x: ratings[x], reverse=True)
    # Get the movie titles and genres for each movie id using the lookup_movie method of the repository
    movies = [agent.repository.lookup_movie(movie_id) for movie_id in sorted_movie_ids]
    # Format the movies as a list of dictionaries with title, genres, and rating as keys and values
    movies_dict = [{"title": title, "genres": genres, "rating": ratings[movie_id]} for movie_id, (title, genres) in zip(sorted_movie_ids, movies)]
    # Return a dictionary with user_id and movies as keys and values as JSON
    return {"user_id": user_id, "movies": movies_dict}

# Define a router hook for movie recommendations in general that takes an agent as dependency and returns a struct of user, movies and ratings in descending order using the movie_rating_count feature pipeline and lookup_movie method of the repository
@app.get("/recommendations/general")
def recommendations_general(agent: MovieLensAgent = Depends(get_agent)):
    # Get the movie rating count feature pipeline from the repository
    movie_rating_count = agent.repository.movie_rating_count()
    # Deploy the feature pipeline using the apply method of the repository
    agent.repository.apply(movie_rating_count)
    # Get the Spark DataFrame of the feature pipeline using the get_feature_data method of the context
    df = agent.context.get_feature_data(movie_rating_count)
    # Convert the Spark DataFrame to a pandas DataFrame using toPandas method
    pdf = df.toPandas()
    # Sort the pandas DataFrame by rating_count in descending order
    pdf.sort_values(by="rating_count", ascending=False, inplace=True)
    # Get the top 10 rows of the pandas DataFrame
    pdf_top10 = pdf.head(10)
    # Get the movie ids and rating counts from the pandas DataFrame
    movie_ids = pdf_top10["movie_id"].tolist()
    rating_counts = pdf_top10["rating_count"].tolist()
    # Get the movie titles and genres for each movie id using the lookup_movie method of the repository
    movies = [agent.repository.lookup_movie(movie_id) for movie_id in movie_ids]
    # Format the movies as a list of dictionaries with title, genres, and rating_count as keys and values
    movies_dict = [{"title": title, "genres": genres, "rating_count": rating_count} for (title, genres), rating_count in zip(movies, rating_counts)]
    # Return a dictionary with movies as key and value as JSON
    return {"movies": movies_dict}

# Define a router hook for movie recommendations for a given tag relevance per user that takes a tag input, a user input, and an agent as dependencies and returns a struct of user, tag, movies and relevance scores in descending order using the get_relevance_feature_vector and lookup_movie methods of the repository
@app.post("/recommendations/tag/user")
def recommendations_tag_user(tag_input: TagInput, user_input: UserInput, agent: MovieLensAgent = Depends(get_agent)):

