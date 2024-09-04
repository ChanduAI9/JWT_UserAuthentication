# JWT-Based User Authentication System with Django Rest Framework

This project implements a JWT (JSON Web Token) based authentication system using Django Rest Framework (DRF). The application allows users to register and login using JWT tokens (access and refresh). It also supports token reuse until expiration and logs login attempts in a log file.

## Features
- User registration and login system.
- JWT-based authentication using access and refresh tokens.
- Reuse the same access token if the user logs in multiple times within the token validity period.
- Logs each login attempt with the username and access token in a `tokens.log` file.

## Technology Stack
- Python (Django Framework)
- Django Rest Framework (DRF)
- djangorestframework-simplejwt (for JWT)
- Bootstrap (for frontend styling)

## Setup and Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- Pip (Python package installer)
- Virtual environment (optional, but recommended)

### Clone the Repository
```bash
git clone https://github.com/ChanduAI9/JWT_UserAuthentication.git
cd JWT_UserAuthentication
