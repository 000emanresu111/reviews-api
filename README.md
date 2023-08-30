# reviews-api

[FastAPI](https://fastapi.tiangolo.com)-based backend web service centred on Pydantic validation.
It provides endpoints to manage and fetch restaurant reviews, as well as scraping reviews from a website.
## Project Structure

The project is organized as follows:

- `app`: The main application directory containing the application logic.
  - `controllers`: Contains the CRUD controllers for managing reviews.
  - `database`: Handles the database connection and interaction.
  - `middlewares`: Custom middleware for handling errors.
  - `models`: Pydantic schema models for validation.
  - `routes`: FastAPI router for defining API endpoints.
  - `scraper`: Contains code for scraping restaurant reviews from a website.
  - `utils`: Utility functions and custom exceptions.
- `tests`: Contains unit tests for the application.
- `main.py`: Main entry point for the FastAPI application.
- `Makefile`: Makefile with common tasks and commands.
- `poetry.lock`: Poetry lock file.
- `pyproject.toml`: Poetry project configuration.
- `README.md`: Project documentation.

## Setup

1. Clone the repository: `git clone https://github.com/your-username/reviews-api.git`
2. Navigate to the project directory: `cd reviews-api`
3. Install dependencies: `poetry install`
4. Run the application: `poetry run uvicorn main:app --host 0.0.0.0 --port 8000`

## Run tests
```bash
$ pytest -vv
```
## Endpoints

- `/`: Root endpoint to check the API status.
- `/reviews/add-review`: POST endpoint to add a new restaurant review.
- `/reviews/fetch-reviews`: GET endpoint to fetch all restaurant reviews.
- `/scrape-justeat-reviews`: GET endpoint to scrape reviews from a specific restaurant.

## Code formatting

This project uses [black](https://github.com/psf/black) code formatter.
