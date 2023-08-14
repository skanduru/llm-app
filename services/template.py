import tecton
from tecton import Template

# Define a template class that inherits from tecton.Template
class MovieLensTemplate(Template):

    # Define the constructor that takes a repository and a context as arguments
    def __init__(self, repository, context):
        self.repository = repository
        self.context = context
    
    # Define a method that takes a user_id and returns a prompt for ratings based on relevance per user
    def ratings_prompt_per_user(self, user_id):
        # Get the ratings feature vector for the user_id
        ratings_fv = self.repository.get_ratings_feature_vector(user_id)
        # Get the movie ids and ratings from the feature vector
        movie_ids = ratings_fv.get_value("movie_id")
        ratings = ratings_fv.get_value("rating")
        # Sort the movie ids by ratings in descending order
        sorted_movie_ids = sorted(movie_ids, key=lambda x: ratings[x], reverse=True)
        # Get the top 10 movie ids
        top_movie_ids = sorted_movie_ids[:10]
        # Get the movie titles and genres for each movie id using the lookup_movie method
        movies = [self.repository.lookup_movie(movie_id) for movie_id in top_movie_ids]
        # Format the movies as a list of strings with title and genres separated by comma
        movies_str = [f"{title}, {genres}" for title, genres in movies]
        # Join the movies with newline character
        movies_nl = "\n".join(movies_str)
        # Return the prompt as a string with user_id and movies_nl as placeholders
        return f"Hello, user {user_id}. Based on your ratings, here are some movies you might like:\n{movies_nl}"
    
    # Define a method that takes a movie_id and returns a prompt for movies based on relevance per tag
    def movies_prompt_per_tag(self, movie_id):
        # Get the movies feature vector for the movie_id
        movies_fv = self.repository.get_movies_feature_vector(movie_id)
        # Get the genres from the feature vector
        genres = movies_fv.get_value("genres")
        # Split the genres by pipe character and convert to a set
        genres_set = set(genres.split("|"))
        # Get the relevance feature vector for each genre using the get_relevance_feature_vector method
        relevance_fvs = [self.repository.get_relevance_feature_vector(genre) for genre in genres_set]
        # Get the movie ids and relevance scores from each feature vector and merge them into one dictionary
        movie_ids_scores = {}
        for relevance_fv in relevance_fvs:
            movie_ids = relevance_fv.get_value("movie_id")
            scores = relevance_fv.get_value("relevance")
            for movie_id, score in zip(movie_ids, scores):
                movie_ids_scores[movie_id] = score
        # Sort the movie ids by relevance scores in descending order
        sorted_movie_ids = sorted(movie_ids_scores, key=lambda x: movie_ids_scores[x], reverse=True)
        # Get the top 10 movie ids
        top_movie_ids = sorted_movie_ids[:10]
        # Get the movie titles and genres for each movie id using the lookup_movie method
        movies = [self.repository.lookup_movie(movie_id) for movie_id in top_movie_ids]
        # Format the movies as a list of strings with title, genres, and score separated by comma
        movies_str = [f"{title}, {genres}, {movie_ids_scores[movie_id]}" for title, genres, movie_id in zip(movies, top_movie_ids)]
        # Join the movies with newline character
        movies_nl = "\n".join(movies_str)
        # Return the prompt as a string with movie_id and movies_nl as placeholders
        return f"Hello, you are interested in movie {movie_id}. Based on the genres, here are some movies with high relevance scores:\n{movies_nl}"

