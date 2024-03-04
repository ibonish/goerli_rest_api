import validators


def validate_data(owner, media_url):
    if not (20 <= len(owner) <= 50) or not validators.url(media_url):
        raise ValueError('Некорректный URL-адрес или адрес владельца')
