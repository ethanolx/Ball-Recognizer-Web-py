python clear_cache.py
heroku login
heroku container:login
heroku container:push -a ca2-doaa03-ej-web web
heroku container:release -a ca2-doaa03-ej-web web
