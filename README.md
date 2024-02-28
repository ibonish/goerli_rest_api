# goerli_rest_api

Сервис, взаимодействующий с контрактом стандарта ERC-721 в блокчейне Ethereum.

## Технологический стек

- Python 3.9
- **Веб-фреймворк:** DRF
- web3

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ibonish/goerli_rest_api.git
```

```
cd goerli_project
```

Собрать образ:

```
docker build -t siiiiiiiiiii .
```

Запустить контейнер:

```
docker run -d --name mycontainer -p 8000:8000 siiiiiiiiiii
```

Создать .env файл и наполнить его:

```
docker exec mycontainer sh -c "cd goerli_project && touch .env && echo PRIVAT_KEY='ваш_приватный_ключ' >> .env"
```


## Описание проекта

Создание токена происходит при помощи POST запроса на эндпоинт:

```
/tokens/create/
```

формат входных данных: 

```
{
    "media_url": "<урл с произвольным изображением>",
    "owner": "<адресс владельца токена>",
}
```

Просмотр всех созданных токенов:

```
tokens/list/
```

Информация о текущем Total supply токена:

```
/tokens/total_supply/
```

Документация доступна в файле `schema.yaml`


## Автор:

- [Скрябина Ольга](https://github.com/ibonish)