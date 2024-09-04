# JWT User Authentication with Django REST Framework and Bootstrap Frontend

## Installation Instructions

### 1. Clone the Repository

Clone the repository to your local machine using the following command:


git clone https://github.com/ChanduAI9/JWT_UserAuthentication.git
cd UserAuthentication

python -m venv env
source env/bin/activate   # On Windows, use `env\Scripts\activate`


pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

### Django template API

POST /api/register/: Register a new user.
POST /api/login/: Log in a user and return JWT tokens.
POST /api/token/refresh/: Refresh an expired access token using a refresh token.

### Custom Frontend API: The /api/
