# MoneyM8s Backend
A simple app to help you keep track of your and your mates' money.

## What's the plan?
A RESTful API that will allow you to create groups, add friends, and keep track of your money.
The API will be written in Python using the Flask framework.
Proposed Libraries:
- Flask
- Flask-SQLAlchemy
- Flask-RESTful

For consideration:
- Flask-Migrate
- Flask-Admin

### How to authenticate?
Authentication will be done using https://github.com/Baspla/GUARD.
After obtaining the GUARDTOKEN, you can use it to authenticate with the API and receive a JWT token.
From then on, you can use the JWT token to authenticate with the API.

### What endpoints are available?
All endpoints are prefixed with `/api/v1/`, for the time being.