# reviews-api
- The reviews-api app is a [FastAPI](https://fastapi.tiangolo.com)-based backend web service centred on Pydantic validation.
- It provides endpoints to manage and fetch restaurant reviews, as well as scraping reviews from a website.
- Custom error handling and logging are also provided.
- The chosen formatter is [black](https://github.com/psf/black) , while the chosen linter is [flake8](https://pypi.org/project/flake8/) .

### 1) Clone the Repository
```bash
$ git clone https://github.com/000emanresu111/reviews-api.git
```
### 2) Navigate into the folder
```bash
$ cd reviews-api
```
### 3) Install deps with Poetry

Ensure you have [Poetry](https://python-poetry.org) installed.

```bash
$ poetry install # or "make install"
```

### 4) Start the app

#### 4.1) Locally
```bash
$ poetry run python main.py
```
This will run both the backend server on port 8086 and the MongoDB instance on port 27017.

```bash
2023-08-31 10:23:55,015 - fastapi - INFO - Connecting to MongoDB...
2023-08-31 10:23:55,019 - fastapi - INFO - Creating collection index...
2023-08-31 10:23:55,025 - fastapi - INFO - Starting server...
2023-08-31 10:23:55,163 - uvicorn.error - INFO - Started server process [25648]
2023-08-31 10:23:55,163 - uvicorn.error - INFO - Waiting for application startup.
2023-08-31 10:23:55,164 - uvicorn.error - INFO - Application startup complete.
2023-08-31 10:23:55,166 - uvicorn.error - INFO - Uvicorn running on http://0.0.0.0:8086 (Press CTRL+C to quit)
```

#### 4.2) Using Docker
Make sure your local Docker deamon is up and running.
```bash
$ docker compose build
$ docker compose up
```

### 5) Run tests
```bash
$ pytest -vv
```

### 6) Scraping
- JustEat revews pages are built using dynamic Javascript, so an headless browser to scrape the data may be easier to setup and maintain.
- If you want to test the scraping service, you need to have Chrome and ChromeDriver installed on your machine.
- You can choose the latest version from [here](https://googlechromelabs.github.io/chrome-for-testing/#stable) based on your Operating System.
- Alternatively, you can build and run the Dockerfile, which automatically downloads and install the latest version of Chrome and ChromeDriver.
- For sake of simplicity, the restaurant name given in input must match the SEO name of the restaurant on JustEat. 
  
  You can find the SEO name of a restaurant by inspecting the URL of the restaurant page on JustEat.

  For instance:

  - URL = `https://www.justeat.it/restaurants-fa-lu-cioli-1917-roma`  
    SEO Name = `fa-lu-cioli-1917-roma`

  - URL: `https://www.justeat.it/restaurants-ristorante-pizzeria-roma-roma`  
    SEO Name = `ristorante-pizzeria-roma-roma`

  - URL: `https://www.justeat.it/restaurants-pizzeria-friggitoria-mascalzone-napoli`  
    SEO Name = `pizzeria-friggitoria-mascalzone-napoli`

#### 6.1) Scraping scenarios

1. The restaurant exists and has reviews.

   In case of successful scraping, you will get the list of scraped reviews.  
   In the logs you can also find more information, such as the total amount of reviews elements.

    ```bash
    2023-08-31 11:57:28,722 - fastapi - INFO - Scraping URL: https://www.justeat.it/restaurants-fa-lu-cioli-1917-roma/reviews
    2023-08-31 11:57:32,098 - fastapi - INFO - Found 16 review elements
    2023-08-31 11:57:39,063 - fastapi - INFO - Request - Method: GET, Path: /scrape-justeat-reviews, Status: 200
    2023-08-31 11:57:39,066 - uvicorn.access - INFO - 127.0.0.1:52947 - "GET /scrape-justeat-reviews?restaurant_name=fa-lu-cioli-1917-roma HTTP/1.1" 200
    ```

2. The restaurant exists but has no reviews.
  
  
   You will get a 204 response code and an empty response body. Message is found in the headers.
    ``` 
    date: Thu,31 Aug 2023 11:38:06 GMT 
    server: uvicorn 
    x-warning-message: There are still no reviews for restaurant 'birreria-del-centro-napoli-80134' 
    ```
  
3. The restaurant does not exist.

   You will get a 404 response code and an empty response body.
    ```json
    {
      "detail": {
        "success": false,
        "error": "Restaurant 'this-doesnt-exists' not found"
      }
    }
    ```

## Project description

### Project Structure

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

### Endpoints

- `/`: Root endpoint to check the API status.
- `/reviews/add-review`: POST endpoint to add a new restaurant review.
- `/reviews/fetch-reviews`: GET endpoint to fetch all restaurant reviews.
- `/scrape-justeat-reviews`: GET endpoint to scrape reviews from a specific restaurant.

### System Architecture
The Reviews API app backend is implemented using Python, FastAPI and MongoDB.

The backend communicates with a MongoDB database for storing reviews information. 

The server exposes a RESTful API that the client can interact with to perform various operations.

### Features description
- Add a review:
Users can add a review by providing some information such as the review text, sentiment, rating, etc. The review is then stored in the db.

- Fetch reviews:
Users can fetch all reviews from the db. The reviews are returned in a paginated format.

- Scraping:
Users can scrape reviews from a specific restaurant on JustEat. The scraping process is performed asynchronously using Selenium and ChromeDriver.

## API endpoints documentation
You may perform requests using a tool such as Postman or cURL, or alternatevely you can use the Swagger UI at http://localhost:8086/doc.

## Usage Example
### 1) Add a review

#### Request
```
POST /reviews/add-review
```

```json
{
  "restaurant": {
    "restaurant_name": "Delicious Eats",
    "restaurant_rating": 4.7
  },
  "review": {
    "review_date": "01/01/2023 12:00:00",
    "review_reviewer": "John Doe",
    "review_text": "Great food and service!",
    "review_sentiment": "1",
    "review_rating": 4.5
  }
}
```

#### Response
```json
{
  "success": true,
  "data": {
    "message": "Review added successfully",
    "restaurant_review": {
      "restaurant": {
        "restaurant_name": "Delicious Eats",
        "restaurant_rating": 4.7
      },
      "review": {
        "review_date": "01/01/2023 12:00:00",
        "review_reviewer": "John Doe",
        "review_text": "Great food and service!",
        "review_sentiment": "1",
        "review_rating": 4.5
      }
    }
  }
}
```

### 2) Fetch reviews

#### Request
```
GET /reviews/fetch-reviews
```

#### Response
```json
{
  "success": true,
  "data": [
    {
      "restaurant": {
        "restaurant_name": "Delicious Eats",
        "restaurant_rating": 4.7
      },
      "review": {
        "review_date": "01/01/2023 12:00:00",
        "review_reviewer": "John Doe",
        "review_text": "Great food and service!",
        "review_sentiment": "1",
        "review_rating": 4.5
      }
    },
    {
      "restaurant": {
        "restaurant_name": "Fake restaurant",
        "restaurant_rating": 5
      },
      "review": {
        "review_date": "01/01/2024 12:00:00",
        "review_reviewer": "John Doe",
        "review_text": "Great food!",
        "review_sentiment": "1",
        "review_rating": 4.2
      }
    }
  ]
}
```

### Scrape reviews from JustEat

#### Request
```
GET /scrape-justeat-reviews?restaurant_name=pizzeria-friggitoria-mascalzone-napoli
```


#### Response
```json
{
  "reviews": [
    {
      "restaurant": {
        "restaurant_name": "restaurants-pizzeria-friggitoria-mascalzone-napoli",
        "restaurant_rating": 4.1
      },
      "review": {
        "review_date": "20/08/2023",
        "review_reviewer": "Andrea",
        "review_text": null,
        "review_sentiment": "None",
        "review_rating": 5
      }
    },
    {
      "restaurant": {
        "restaurant_name": "restaurants-pizzeria-friggitoria-mascalzone-napoli",
        "restaurant_rating": 4.1
      },
      "review": {
        "review_date": "19/08/2023",
        "review_reviewer": "Daniela",
        "review_text": "Ottima la pizza, peccato che a volte la sbagliano, a volte consegnano ordini mancanti, a volte arrivano in straritardo... peccato davvero",
        "review_sentiment": "None",
        "review_rating": 3.5
      }
    },

...
```