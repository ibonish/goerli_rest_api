from django.db import models


class Token(models.Model):
    unique_hash = models.CharField(
        max_length=20,
        unique=True
    )
    tx_hash = models.CharField(
        max_length=255
    )
    media_url = models.URLField()
    owner = models.CharField(
        max_length=255
    )

    def __str__(self):
        return f'Owner: {self.owner}, media_url: {self.media_url}'
