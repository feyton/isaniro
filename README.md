#### Isaniro Group Ltd
## Isaniro
Welcome to our repository. The project combines the blog and book store. It is developed with modern technologies and is being transformed into a React and Django project with Server Side rendering using NextJS
## Our sites
You can check our production site at
- [Isaniro.com](https://isaniro.com)
- [Heroku Staging Version](https://isaniro.herokuapp.com/)

## Running the application
Follow the following instruction to get you started
```
git clone https://github.com/feyton/isaniro.git
cd isaniro
python -m venv env
cd env/Scripts/
. activate
cd ../../
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
open http://localhost:8000/
```

## Deployment 
When deploying the application remember to run the following commands
```
python manage.py collectstatic
python manage.py compress
```
