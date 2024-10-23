# HBnB Project

## Overview

HBnB is a clone Airbnb website for users, places, reviews, and amenities. The project follows a clean and modular architecture, using the Facade design pattern to manage interactions between the presentation, business logic, and persistence layers. This initial version uses an in-memory repository to store and validate objects, but it will later be replaced with a database-backed solution.

## Project Structure

The project is organized into multiple layers, each handling a specific responsibility:

```text
    hbnb/
    ├── app/
    │   ├── __init__.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── v1/
    │   │       ├── __init__.py
    │   │       ├── users.py
    │   │       ├── places.py
    │   │       ├── reviews.py
    │   │       ├── amenities.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   ├── amenity.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── facade.py
    │   ├── persistence/
    │       ├── __init__.py
    │       ├── repository.py
    ├── run.py
    ├── config.py
    ├── requirements.txt
    ├── README.md
```

### Key Components

- **app/**: Contains the core application logic, including API routes, models, services, and the persistence layer.
- **api/**: Handles API endpoints, organized by version (`v1/`). The following API endpoints are implemented:
  - **users.py**: API for user operations (create, update, retrieve).
  - **places.py**: API for managing places (CRUD operations).
  - **reviews.py**: API for handling reviews associated with places and users.
  - **amenities.py**: API for managing amenities available for places.
- **models/**: Defines the business logic for managing users, places, reviews, and amenities.
- **services/**: Implements the Facade design pattern to simplify interactions between the API, business logic, and persistence layers.
- **persistence/**: Provides an in-memory repository for object storage and validation. This will be replaced with a database solution in future updates.
- **run.py**: The entry point for running the Flask application.
- **config.py**: Contains environment-specific configuration settings.

## Installation

To set up and run this project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Morg92b/holbertonschool-hbnb.git
   cd hbnb
   ```

2. **Install the dependencies:**
   Use `pip` to install the required Python packages listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   You can start the Flask application by running the `run.py` file:
   ```bash
   python run.py
   ```

## Future Plans

In future parts of this project, the in-memory repository will be replaced with a database-backed solution (e.g., using SQLAlchemy). API endpoints and full business logic for users, places, reviews, and amenities will also be implemented.

## Requirements

- Python 3.8+
- Flask
- Flask-RESTx

## Authors

- [Morgan Bouaziz](https://github.com/Morg92b)
- [Keiko Bisou](https://github.com/bisoukeiko)
