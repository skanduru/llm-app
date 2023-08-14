from tortoise import fields, models

# Define the models that correspond to the CSV data using Tortoise ORM syntax
class Rating(models.Model):
    user_id = fields.IntField(pk=True)
    movie_id = fields.IntField()
    rating = fields.FloatField()
    timestamp = fields.DatetimeField()

    class Meta:
         table = "ratings"

    def __str__(self):
        return f"Rating: {self.rating}"

class Movie(models.Model):
    movie_id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    genres = fields.CharField(max_length=255)

    class Meta:
         table = "movies"

    def __str__(self):
        return self.title

class Link(models.Model):
    movie_id = fields.IntField(pk=True)
    imdb_id = fields.CharField(max_length=255)
    tmdb_id = fields.CharField(max_length=255)

    class Meta:
         table = "links"

    def __str__(self):
        return self.movie_id

class GenomeScore(models.Model):
    movie_id = fields.IntField(pk=True)
    tag_id = fields.IntField()
    relevance = fields.FloatField()

    class Meta:
         table = "scores"

    def __str__(self):
        return self.relevance

class GenomeTag(models.Model):
    tag_id = fields.IntField(pk=True)
    tag = fields.CharField(max_length=255)

    class Meta:
         table = "tags"

    def __str__(self):
        return self.tag
