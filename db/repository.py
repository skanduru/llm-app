import tecton
from tortoise import Tortoise, fields, models

# Define a data source for ratings.csv
ratings_ds = tecton.TortoiseDataSource(
    name="ratings_ds",
    model="app.models.Rating",
    event_timestamp_column="timestamp",
    created_timestamp_column="timestamp"
)

# Define a data source for movies.csv
movies_ds = tecton.TortoiseDataSource(
    name="movies_ds",
    model="app.models.Movie"
)

# Define a data source for links.csv
links_ds = tecton.TortoiseDataSource(
    name="links_ds",
    model="app.models.Link"
)

# Define a data source for genome-scores.csv
genome_scores_ds = tecton.TortoiseDataSource(
    name="genome_scores_ds",
    model="app.models.GenomeScore"
)

# Define a data source for genome-tags.csv
genome_tags_ds = tecton.TortoiseDataSource(
    name="genome_tags_ds",
    model="app.models.GenomeTag"
)

# Define a repository class that inherits from tecton.FeatureRepository
class MovieLensRepository(tecton.FeatureRepository):
    
    # Define a constructor that takes a tecton context as an argument
    def __init__(self, context):
        self.context = context
    
    # Define a lookup method that takes a movieId and returns the movie title and genres
    async def lookup_movie(self, movieId):
        # Use Tortoise async API to query the Movie model by movie_id
        movie = await Movie.get(movie_id=movieId)
        # Return the title and genres attributes as a tuple
        return (movie.title, movie.genres)
    
    # Define a lookup method that takes a movieId and returns the imdbId and tmdbId
    async def lookup_links(self, movieId):
        # Use Tortoise async API to query the Link model by movie_id
        link = await Link.get(movie_id=movieId)
        # Return the imdb_id and tmdb_id attributes as a tuple
        return (link.imdb_id, link.tmdb_id)
    
    # Define a lookup method that takes a tagId and returns the tag
    async def lookup_tag(self, tagId):
        # Use Tortoise async API to query the GenomeTag model by tag_id
        tag = await GenomeTag.get(tag_id=tagId)
        # Return the tag attribute as a string
        return tag.tag
    
    # Define a method that takes a movieId and returns the relevance scores for all tags
    async def get_relevance_scores(self, movieId):
        # Use Tortoise async API to query the GenomeScore model by movie_id
        scores = await GenomeScore.filter(movie_id=movieId).all()
        # Convert the list of scores to a dictionary with tag_id as key and relevance as value
        scores_dict = {score.tag_id: score.relevance for score in scores}
        # Return the dictionary
        return scores_dict
    
    # Define a method that takes a userId and returns the ratings for all movies
    async def get_ratings(self, userId):
        # Use Tortoise async API to query the Rating model by user_id
        ratings = await Rating.filter(user_id=userId).all()
        # Convert the list of ratings to a dictionary with movie_id as key and rating as value
        ratings_dict = {rating.movie_id: rating.rating for rating in ratings}
        # Return the dictionary
        return ratings_dict
    
    # Define a feature pipeline that computes the average rating of movies
    def movie_average_rating(self):
        return tecton.FeaturePipeline(
            name="movie_average_rating",
            description="The average rating for each movie",
            entities=[tecton.Entity(name="movie_id", dtype=int)],
            online=True,
            input=ratings_ds,
            transformation=tecton.AggregationTransform(
                groupby=["movie_id"],
                aggregations={
                    "average_rating": tecton.FeatureAggregation(
                        column="rating",
                        function="mean",
                        time_windows=["1h", "12h", "24h", "72h", "7d", "30d"]
                    )
                }
            ),
            output=tecton.FeatureOutput(
                mode="pyspark_sql_expression",
                description="The average rating for each movie"
            )
        )
    
    # Define a feature pipeline that computes the number of ratings of movies
    def movie_rating_count(self):
        return tecton.FeaturePipeline(
            name="movie_rating_count",
            description="The number of ratings for each movie",
            entities=[tecton.Entity(name="movie_id", dtype=int)],
            online=True,
            input=ratings_ds,
            transformation=tecton.AggregationTransform(
                groupby=["movie_id"],
                aggregations={
                    "rating_count": tecton.FeatureAggregation(
                        column="*",
                        function="count",
                        time_windows=["1h", "12h", "24h", "72h", "7d", "30d"]
                    )
                }
            ),
            output=tecton.FeatureOutput(
                mode="pyspark_sql_expression",
                description="The number of ratings for each movie"
            )
        )
    
    # Define a feature pipeline that computes the genres of movies
    def movie_genres(self):
        return tecton.FeaturePipeline(
            name="movie_genres",
            description="The genres of each movie",
            entities=[tecton.Entity(name="movie_id", dtype=int)],
            online=True,
            input=movies_ds,
            transformation=tecton.IdentityTransform(),
            output=tecton.FeatureOutput(
                mode="pyspark_sql_expression",
                description="The genres of each movie"
            )
        )
    
    # Define a feature pipeline that computes the relevance score of movies for a given tag
    def movie_relevance_score(self, tag):
        return tecton.FeaturePipeline(
            name=f"movie_relevance_score_{tag}",
            description=f"The relevance score of each movie for the tag {tag}",
            entities=[tecton.Entity(name="movie_id", dtype=int)],
            online=True,
            input=genome_scores_ds.join(genome_tags_ds, on="tag_id"),
            transformation=tecton.FilterTransform(filter=f"tag = '{tag}'"),
            output=tecton.FeatureOutput(
                mode="pyspark_sql_expression",
                description=f"The relevance score of each movie for the tag {tag}"
            )
        )

