# planeks
Simple news site. Test-task for PLANEKS.

## Technologies
  + Python 3.7
  + Django 3.0
  + Celery 4.4.1
  + django-ckeditor
  + django-crispy
  + awesome-slugify
  + redis
  + Bootstrap 4
  + [SendGrid](https://sendgrid.com)

## Instalation
To setup this project run the next following steps:
1. Clone this reposetory to your project directory:
```bash
git clone https://github.com/crocodundee/planeks.git
```
2. Create and activate virtual enviroment in project's root directory:
```bash
planeks $ virtualenv venv
planeks $ source venv/bin/activate
```
3. Install all dependencies from requirements.txt:
```bash
(venv) planeks $ pip install -r requirements.txt
```
4. Configurate database for project:
```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```
5. Run it:
```bash
$ python manage.py runserver
```
## Project's structure:
        planeks/
            __init__.py          
            asgi.py              
            wsgi.py
            celery.py
            urls.py
            setting.py
        posts/
            migrations/
            templates/
                posts/
        users/
            migrations/
            templates/
                users/
        templates/
        media/
        static/
        manage.py

## Realized features
### Manage users
1. Login and sign up users by email+password.
2. Created custom user managment (model, manager, admin panel).
3. Created user's groups(admins, editors, users as default) for moderation their posts).
### News publication
1. Creating user's news via CKEditor(text posts with oppotunity to add images and attachments).
2. Adding comments to posts.
3. Posts moderations via users groups.
### Email-backend
1. Email-confirmation for user registration.
2. Email notification for post's author about comment to his post was added.

## License
Copyright 2020 &copy; crocodundee
