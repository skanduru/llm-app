
# Define a Pydantic model for user input
class UserInput(BaseModel):
    user_id: int

# Define a Pydantic model for movie input
class MovieInput(BaseModel):
    movie_id: int

# Define a Pydantic model for tag input
class TagInput(BaseModel):
    tag: str

# Define a Pydantic model for genre input
class GenreInput(BaseModel):
    genre: str

from .recommendations import router as recommendations_router
from .ratings import router as ratings_router
from .movies import router as movies_router
from .user.tag import router as user_tag_router
from .rating.tag import router as rating_tag_router
from .chains.tag import router as chains_tag_router

router = APIRouter()

router.include_router(recommendations_router, prefix="/recommendations")
router.include_router(ratings_router, prefix="/ratings")
router.include_router(movies_router, prefix="/movies")
router.include_router(user_tag_router, prefix="/recommendations/user/tag")
router.include_router(rating_tag_router, prefix="/recommendations/rating/tag")
router.include_router(user_tag_router, prefix="/recommendations/chains")
