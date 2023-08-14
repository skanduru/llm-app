A comprehensive project structure that is optimized for scalability, maintainability, and testing, based on the layered architecture approach

```
llm-app/
├─ main.py # The main file that defines the FastAPI app and the router hooks
├─ cofnig.py # The configuration of llm
├─ db/
│   ├─ __init__.py
│   ├── models.py # The file that defines the Pydantic models for user input, movie input, tag input, and genre input
│   ├── repository.py # The file that defines the MovieLensRepository class that inherits from tecton.FeatureRepository
│   └── db.sqlite3 # The SQLite database file that stores the CSV data
├─ routers/ # Router hooks
│   ├─ __init__.py
│   ├─ movies.py
│   ├─ ratings.py
│   └─ recommendations.py
├─ agents/ # Router hooks
│   └── agent.py # The file that defines the MovieLensAgent class that inherits from tecton.Agent
├── service/
│   └─ template.py # The file that defines the MovieLensTemplate class that inherits from tecton.Template
├── data/
│   ├── ratings.csv # The CSV file that contains the ratings data
│   ├── movies.csv # The CSV file that contains the movies data
│   ├── links.csv # The CSV file that contains the links data
│   ├── genome-scores.csv # The CSV file that contains the genome scores data
│   └── genome-tags.csv # The CSV file that contains the genome tags data
├── requirements.txt # The file that lists the required Python packages for the application
└── README.md # The file that documents the application and how to run it
└─ tests/
    ├─ __init__.py
    ├─ test_llm_app.py
```
The README.md file is finished. You can see the full text below:

## LLM Application using MovieLens 25M Dataset and FastAPI

This is a LLM (Language, Logic and Math) application that uses the MovieLens 25M dataset and FastAPI to provide movie recommendations based on ratings, genres, tags, and relevance scores. The application uses the Tecton SDK to define data sources, feature pipelines, feature repositories, templates, response schemas, agents, and chains. The application also uses the OpenAI Completion API to generate responses based on prompts. The application is tested using pytest with various fixtures and assertions.

## Features

The application has the following features:

- Modules: The application is organized into modules that define the models, repository, template, agent, and main files. The models file defines the Pydantic models for user input, movie input, tag input, and genre input. The repository file defines the MovieLensRepository class that inherits from tecton.FeatureRepository and defines the data sources, feature pipelines, and lookup methods. The template file defines the MovieLensTemplate class that inherits from tecton.Template and defines the methods that return prompts for ratings and movies based on relevance per user or tag. The agent file defines the MovieLensAgent class that inherits from tecton.Agent and defines the methods that return responses using the OpenAI Completion API. The main file defines the FastAPI app object and the router hooks that handle the requests and responses.
- Various templates: The application uses various templates to generate prompts for ratings and movies based on relevance per user or tag. The templates use the ratings_prompt_per_user and movies_prompt_per_tag methods of the MovieLensTemplate class that take a user_id or a movie_id as input and return a prompt as output.
- Response schemas: The application uses response schemas to parse the responses from the OpenAI Completion API and return a dictionary with the relevant fields. The response schemas use the MovieLensResponseSchema class that inherits from tecton.ResponseSchema and defines the parse method that takes a prompt and a response as input and returns a dictionary with prompt, text, and most_probable_token as output.
- Output parsers: The application uses output parsers to format the output of the feature pipelines and lookup methods into strings or lists of strings or dictionaries. The output parsers use string formatting, list comprehension, dictionary comprehension, join method, zip function, etc.
- Chains: The application uses chains to create sequential or router logic for generating prompts or responses. The chains use the SequentialChain and RouterChain classes from tecton SDK that take a name, description, input, output, and condition as arguments. The chains are used in the recommendations chain router hook that takes a user_id as input and returns a struct of user, movies and ratings in descending order using the get_ratings_feature_vector and lookup_movie methods of the repository and the get_response method of the agent.
- Pytests: The application is tested using pytest with various fixtures and assertions. The pytest file defines a list of user ids, movie ids, tags, and genres for testing. It also defines fixtures that return user input, movie input, tag input, and genre input objects for each value in the list. It also defines test functions that test each router hook using the fixtures and asserts that the response status code is 200 and the response json contains the expected keys and values.

## How to run

To run the application, you need to have Python 3.8 or higher installed on your system. You also need to have an OpenAI API key with access to skiff library.

You can follow these steps to run the application:

1. Clone this repository to your local machine using `git clone https://github.com/llm-app/llm-app.git`.
2. Navigate to the llm-app directory using `cd llm-app`.
3. Install the required Python packages using `pip install -r requirements.txt`.
4. Download the MovieLens 25M dataset from https://grouplens.org/datasets/movielens/25m/ and unzip it into the data directory.
5. Create a SQLite database file named db.sqlite3 in the db directory using `sqlite3 db.sqlite3`.
6. Import the CSV data into the SQLite database using `.mode csv` followed by `.import ratings.csv Rating`, `.import movies.csv Movie`, `.import links.csv Link`, `.import genome-scores.csv GenomeScore`, `.import genome-tags.csv GenomeTag` commands in sqlite3 shell.
7. Exit from sqlite3 shell using `.exit` command.
8. Run Tortoise ORM migrations using `tortoise-orm migrate --name init --app models`.
9. Run FastAPI app using `uvicorn app.main:app --reload`.
10. Open your browser and go to http://localhost:8000/docs to see the interactive API documentation.
11. Try out different endpoints with different inputs and see the responses.
12. Run pytest using `pytest` command in the terminal and see the test results.

## Output

The output of the application is a JSON object that contains the relevant information for each endpoint. For example, the output of the ratings response endpoint for user_id 1 is:

```json
{
  "user_id": 1,
  "movies": [
    "Toy Story (1995), Adventure|Animation|Children|Comedy|Fantasy",
    "Jumanji (1995), Adventure|Children|Fantasy",
    "Grumpier Old Men (1995), Comedy|Romance",
    "Waiting to Exhale (1995), Comedy|Drama|Romance",
    "Father of the Bride Part II (1995), Comedy",
    "Heat (1995), Action|Crime|Thriller",
    "Sabrina (1995), Comedy|Romance",
    "Tom and Huck (1995), Adventure|Children",
    "Sudden Death (1995), Action",
    "GoldenEye (1995), Action|Adventure|Thriller"
  ],
  "ratings_prompt": "Hello, user 1. Based on your ratings, here are some movies you might like:\nToy Story (1995), Adventure|Animation|Children|Comedy|Fantasy\nJumanji (1995), Adventure|Children|Fantasy\nGrumpier Old Men (1995), Comedy|Romance\nWaiting to Exhale (1995), Comedy|Drama|Romance\nFather of the Bride Part II (1995), Comedy\nHeat (1995), Action|Crime|Thriller\nSabrina (1995), Comedy|Romance\nTom and Huck (1995), Adventure|Children\nSudden Death (1995), Action\nGoldenEye (1995), Action|Adventure|Thriller"
}
```

## How to use tecton SDK to build an LLM ?
To define data sources, feature pipelines, and lookup methods using the Tecton SDK, you can refer to the Tecton SDK documentation1 that provides examples and explanations for each concept. Here are some brief summaries:
 - Data sources: Data sources are objects that define where your raw data is stored and how to access it. You can use the tecton.DataSource class to create data sources for different types of data, such as CSV files, Spark tables, Kafka topics, etc. You can also specify the schema, event timestamp column, created timestamp column, and other parameters for your data sources. For example:

```
# Define a data source for ratings.csv
ratings_ds = tecton.DataSource(
    name="ratings_ds",
    schema=Schema(
        user_id=IntegerType(),
        movie_id=IntegerType(),
        rating=FloatType(),
        timestamp=TimestampType()
    ),
    event_timestamp_column="timestamp",
    created_timestamp_column="timestamp",
    batch_config=tecton.BatchConfig(
        file_format="csv",
        path="data/ratings.csv"
    )
)
```
 - Feature pipelines: Feature pipelines are objects that define how to transform your raw data into features. You can use the tecton.FeaturePipeline class to create feature pipelines for different purposes, such as aggregations, joins, filters, etc. You can also specify the name, description, entities, online flag, input data source, transformation logic, and output mode for your feature pipelines. For example:
```
# Define a feature pipeline that computes the average rating of movies
def movie_average_rating():
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
```
 - Lookup methods: Lookup methods are functions that query the feature store or other data sources and return the values of features or other information. You can define lookup methods in your feature repository class that inherits from tecton.FeatureRepository. You can use Tortoise ORM or other libraries to query your data sources and return the results as tuples, dictionaries, lists, etc. For example:
```
# Define a lookup method that takes a movieId and returns the movie title and genres
async def lookup_movie(self, movieId):
    # Use Tortoise async API to query the Movie model by movie_id
    movie = await Movie.get(movie_id=movieId)
    # Return the title and genres attributes as a tuple
    return (movie.title, movie.genres)
```
