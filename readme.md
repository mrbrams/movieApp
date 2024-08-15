Movie App
A FastAPI application for managing movies, user authentication, ratings, and comments.

Features
User registration and login with JWT
Manage movies (add, view, edit, delete)
Rate movies and view ratings
Add and view comments, including nested comments

Getting Started
Clone the Repo: git clone https://github.com/mrbrams/movie-app.git

Set Up Environment:
Create a virtual environment

Install dependencies: pip install -r requirements.txt

Configure .env file with DATABASE_URL and SECRET_KEY

Run Migrations:
For Alembic: alembic upgrade head
For Tortoise ORM: aerich upgrade

Start the App: uvicorn main:app --host 0.0.0.0 --port 8000

API Endpoints
User: Register, login
Movie: Add, view, edit, delete
Rating: Rate, get rating
Comment: Add, view, reply to comments

Running Tests
Use pytest to run tests: pytest

Deployment
Deploy using platforms like Render, Heroku, or Vercel. Follow their documentation for specifics.

Contributing
Contributions are welcome. Open an issue or submit a pull request.

License
MIT License - see LICENSE for details.

