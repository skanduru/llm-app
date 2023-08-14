import tecton
import openai
import json
from tecton import Template
from .services import 

from dotenv import find_dotenv, load_dotenv

# Define a dependency function that returns a MovieLensAgent object with the repository, context, and api_key as arguments
def get_agent():
    repository = MovieLensRepository(context=tecton.get_context())
    context = tecton.get_context()
    api_key = os.environ['OPENAI_API_KEY']
    return MovieLensAgent(repository, context, api_key)

# Define a response schema class that inherits from tecton.ResponseSchema
class MovieLensResponseSchema(tecton.ResponseSchema):

    # Define the constructor that takes a prompt and a response as arguments
    def __init__(self, prompt, response):
        self.prompt = prompt
        self.response = response
    
    # Define a method that parses the response and returns a dictionary with the relevant fields
    def parse(self):
        # Parse the response as a JSON object
        response_json = json.loads(self.response)
        # Get the choices from the response
        choices = response_json["choices"]
        # Get the first choice as the best choice
        best_choice = choices[0]
        # Get the text from the best choice
        text = best_choice["text"]
        # Get the logprobs from the best choice
        logprobs = best_choice["logprobs"]
        # Get the top_logprobs from the logprobs
        top_logprobs = logprobs["top_logprobs"]
        # Get the first top_logprob as the most probable token
        most_probable_token = top_logprobs[0]
        # Return a dictionary with the prompt, text, and most_probable_token as keys and values
        return {
            "prompt": self.prompt,
            "text": text,
            "most_probable_token": most_probable_token
        }

# Define an agent class that inherits from tecton.Agent
class MovieLensAgent(tecton.Agent):

    # Define the constructor that takes a repository, a context, and an openai api key as arguments
    def __init__(self, repository, context, api_key):
        self.repository = repository
        self.context = context
        self.api_key = api_key
    
    # Define a method that takes a user_id and returns a ratings prompt using the ratings_prompt_per_user method of the repository
    def get_ratings_prompt(self, user_id):
        return self.repository.ratings_prompt_per_user(user_id)
    
    # Define a method that takes a movie_id and returns a movies prompt using the movies_prompt_per_tag method of the repository
    def get_movies_prompt(self, movie_id):
        return self.repository.movies_prompt_per_tag(movie_id)
    
    # Define a method that takes a prompt and returns a response using the openai completion API with temperature, stream, functions and function_calls parameters
    def get_response(self, prompt):
        # Set the openai api key using skiff library
        skiff.set_api_key(self.api_key)
        # Create a completion object using openai library
        completion = openai.Completion()
        # Create a stream object using openai library
        stream = openai.Stream()
        # Create a function object using openai library
        function = openai.Function()
        # Create a function_call object using openai library
        function_call = openai.FunctionCall()
        
        # Define the parameters for the completion API
        params = {
            "engine": "davinci",
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.8,
            "stream": True,
            "logprobs": 10,
            "functions": [function],
            "function_calls": [function_call]
        }
        
        # Call the completion API with the parameters and return the response as a string
        response = completion.create(**params)
        return str(response)
    
    # Define a method that takes a user_id and returns a ratings response using the get_ratings_prompt and get_response methods and the MovieLensResponseSchema class
    def get_ratings_response(self, user_id):
        # Get the ratings prompt for the user_id
        ratings_prompt = self.get_ratings_prompt(user_id)

