# LOL Items API

This is a FastAPI-based REST API for managing League of Legends (LOL) items. It provides endpoints for creating, reading, updating, and deleting item information, along with user authentication and authorization.

## Features

*   **Item Management:** Create, read, update, and delete item records.
*   **User Authentication and Authorization:** Secure API with JWT-based authentication and role-based authorization.
*   **Data Storage:** Uses SQLite database for persistent storage via SQLAlchemy.
*   **Dependencies:** Uses FastAPI dependency injection for managing database connections.
*   **API Endpoints:**
    *   `/`: Welcome message.
    *   `/items/{item_name}`: Retrieve item details by name.
    *   `/items/`: List all items, with optional filtering by stats and price.
    *   `/items/`: Create a new item (requires authentication).
    *   `/items/{item_name}`: Update an existing item (requires authentication).
    *   `/items/{item_name}`: Delete an item (requires authentication).
    *   `/token`: Obtain a JWT access token for authentication.
    *   `/users/me`: Get details of the currently logged-in user.
    *   `/users/{user_name}`: Get details of a specific user.
    *   `/users/`: Create a new user.
    *   `/users/{user_name}`: Update an existing user.
    *   `/users/deactivate/{user_name}`: Deactivate a user.
    *   `/users/{user_name}`: Delete a user.

## Technologies Used

*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Pydantic:** Data validation and settings management using Python type annotations.
*   **SQLAlchemy:** Python SQL toolkit and Object-Relational Mapper that gives application developers the full power and flexibility of SQL.
*   **SQLite:** A self-contained, high-reliability, embedded, full-featured, public-domain, SQL database engine.
*   **JWT (JSON Web Tokens):** For secure authentication and authorization.
*   **bcrypt:** For secure password hashing.
*   **Python 3.7+**

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    Create a file called `requirements.txt` with the following inside:

    ```
    fastapi
    uvicorn
    pydantic
    SQLAlchemy
    python-dotenv
    passlib[bcrypt]
    python-jose
    ```

4.  **Configure Security:**

    *   Create a `config.ini` file in the root directory of the project.
    *   Add a `security` section with a `secret_key` value.  **Important:** Generate a strong, random secret key and store it securely.  **Do not commit the config.ini file to version control (e.g., Git).** Example `config.ini`:

    ```ini
    [security]
    secret_key = YOUR_SECURE_RANDOM_KEY_HERE
    ```

5.  **Run the application:**

    ```bash
    uvicorn main:app --reload
    ```

    (Replace `main` with the name of your main FastAPI file if it's different.)

6.  **Access the API:**

    Open your browser and navigate to `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs` to explore the available endpoints and test them out.

## API Endpoints

| Method | Endpoint                     | Description                                  | Request Body (Example)                                                                                                                                                                                                                | Response (Example)                                                                                                                                                                                                         |
| ------ | ---------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GET    | `/`                          | Returns a welcome message.                     | None                                                                                                                                                                                                                               | `{"message": "Welcome to LOL items API"}`                                                                                                                                                                               |
| POST   | `/token`                     | Obtains a JWT access token (login).          | Form data with `username` and `password`.                                                                                                                                                                                           | `{"access_token": "...", "token_type": "bearer"}`                                                                                                                                                                 |
| GET    | `/items/{item_name}`         | Retrieves an item by name.                   | None                                                                                                                                                                                                                               | See `pydantic_classes.Item` definition. Example: `{"name": "B.F. Sword", "stats": {"Armor": 0, "Health": 0}, "description": "A powerful sword", "price": 1300.0, "sell_price": 910.0}`                               |
| POST   | `/items/`                      | Creates a new item (requires authentication).| See `pydantic_classes.Item` definition. Requires a valid JWT token in the `Authorization` header.  Example: `{"name": "B.F. Sword", "stats": {"Armor": 0, "Health": 0}, "description": "A powerful sword", "price": 1300.0, "sell_price": 910.0}`                                                                                                       |                                                                                        |
| PUT    | `/items/{item_name}`         | Updates an existing item (requires authentication). | See `pydantic_classes.Item` definition.  Requires a valid JWT token in the `Authorization` header.                                                                                                                                                                                          | `{"name": "B.F. Sword", "stats": {"Armor": 5, "Health": 50}, "description": "A powerful sword (upgraded)", "price": 1300.0, "sell_price": 910.0}`                                                              |
| DELETE | `/items/{item_name}`         | Deletes an item (requires authentication). Requires a valid JWT token in the `Authorization` header.                            | None                                                                                                                                                                                                                               | `204 No Content` (no response body)                                                                                                                                                                             |
| GET    | `/items/`                      | Retrieves all items, optionally filtered by stats and price. | Query parameters: `stats` (list of stats, e.g., `stats=Armor&stats=Health`), `price` (integer), `price_greater_than` (boolean)                                                                                       | `{"item_name": {"name": "...", "stats": {...}, "description": "...", "price": ..., "sell_price": ...}}`                                                                                                             |
| GET    | `/users/me`                  | Retrieves details of the currently logged-in user (requires authentication). | Requires a valid JWT token in the `Authorization` header.                                                                                                                                              | See `pydantic_classes.UserNoPass` definition. Example: `{"user_name": "testuser", "active": true}`                                                                                                                   |
| GET    | `/users/{user_name}`            | Retrieves details of a specific user (requires authentication).        | Requires a valid JWT token in the `Authorization` header.                                                                                                                                              | See `pydantic_classes.User` definition. Example: `{"user_name": "testuser", "password": "hashed_password", "active": true}`                                                                                              |
| POST   | `/users/`                     | Creates a new user (requires authentication).        | See `pydantic_classes.User` definition. Requires a valid JWT token in the `Authorization` header.                                                                                                                                              | {"OK": 200}                                                                                              |
| PUT   | `/users/{user_name}`                     | Updates a new user (requires authentication).        | See `pydantic_classes.User` definition. Requires a valid JWT token in the `Authorization` header.                                                                                                                                              | {"OK": 200}                                                                                              |
| PUT   | `/users/deactivate/{user_name}`                     | Deactivates a new user (requires authentication).        | See `pydantic_classes.User` definition. Requires a valid JWT token in the `Authorization` header.                                                                                                                                              | {"OK": 200}                                                                                              |
| DELETE  | `/users/{user_name}`                     | Deletes a new user (requires authentication).        | See `pydantic_classes.User` definition. Requires a valid JWT token in the `Authorization` header.                                                                                                                                              |  `204 No Content` (no response body)                                                                                                                                                                             |

## Code Structure

*   `main.py`: The main FastAPI application file.
*   `items.py`: Defines the API routes related to items.
*   `users.py`: Defines the API routes related to users.
*   `security.py`: Defines security-related functions, including JWT token creation, password hashing, and authentication dependencies.
*   `pydantic_classes.py`: Defines the Pydantic models used for data validation and serialization (e.g., `Item`, `User`).
*   `data_base/`: Contains database-related files:
    *   `database_provider.py`: Provides a dependency injection function for accessing the database service.
    *   `database_service.py`: Defines the abstract base class for database services.
    *   `database_service_impl.py`: Implements the database service using SQLAlchemy.
    *   `sqlalchemy_db.py`: Defines the SQLAlchemy models and database setup.
*   `exception_handlers.py`: Defines custom exception handlers for the API.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.