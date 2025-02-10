# LOL Items API

This is a FastAPI-based REST API for managing League of Legends (LOL) items. It provides endpoints for creating, reading, updating, and deleting item information.

## Features

*   **Item Management:** Create, read, update, and delete item records.
*   **Data Storage:** Uses SQLite database for persistent storage via SQLAlchemy.
*   **Dependencies:** Uses FastAPI dependency injection for managing database connections.
*   **Basic API Endpoints:**
    *   `/`: Welcome message
    *   `/items/{item_name}`: Retrieve item details by name.
    *   `/items/`: List all items.
    *   `/items/`: Create a new item.
    *   `/items/{item_id}`: Update an existing item.
    *   `/items/{item_id}`: Delete an item.
*   **Example Endpoints:** Includes example endpoints like `/hello/{name}`, `/models/{model_name}`, `/items_opt/{item_id}`, and `/users/{user_id}/items/{item_id}` to showcase FastAPI functionalities.

## Planned Features

1.  **Validation:**
    *   Implement data validation for request payloads (e.g., using Pydantic) to ensure data integrity.
    *   Validate the existence of related entities (e.g., ensuring an item with a specific ID exists before updating it).

2.  **Error Management with Descriptive Messages:**
    *   Implement comprehensive error handling to catch potential exceptions.
    *   Return informative error messages to the client to aid in debugging.
    *   Use custom exception classes for specific error scenarios.

3.  **Filtering System:**
    *   Implement a flexible filtering system for retrieving items based on various criteria (e.g., price range, specific stats).
    *   Support filtering via query parameters in the `/items/` endpoint.

## Technologies Used

*   **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Pydantic:** Data validation and settings management using Python type annotations.
*   **SQLAlchemy:** Python SQL toolkit and Object-Relational Mapper that gives application developers the full power and flexibility of SQL.
*   **SQLite:** A self-contained, high-reliability, embedded, full-featured, public-domain, SQL database engine.
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
   Create a file called `requirements.txt` with the following inside
    ```
    fastapi
    uvicorn
    pydantic
    SQLAlchemy
    python-dotenv
    ```

4.  **Run the application:**

    ```bash
    uvicorn main:app --reload
    ```

    (Replace `main` with the name of your main FastAPI file if it's different.)

5.  **Access the API:**

    Open your browser and navigate to `http://localhost:8000` (or the address where your API is running). You can also access the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

| Method | Endpoint                     | Description                                  | Request Body (Example)                                                                                                                                                                                                         | Response (Example)                                                                     |
| ------ | ---------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| GET    | `/`                          | Returns a welcome message.                     | None                                                                                                                                                                                                                         | `{"message": "Welcome to LOL items API"}`                                              |
| GET    | `/items/{item_name}`         | Retrieves an item by name.                   | None                                                                                                                                                                                                                         | See `pydantic_classes.Item` definition.                                               |
| POST   | `/items/`                      | Creates a new item.                          | See `pydantic_classes.Item` definition.  Example: `{"name": "B.F. Sword", "stats": {"Armor": 0, "Health": 0}, "description": "A powerful sword", "price": 1300.0, "sell_price": 910.0}`                                                                                                       |                                                                                        |
| PUT    | `/items/{item_id}`         | Updates an existing item.                    | See `pydantic_classes.Item` definition.                                                                                                                                                                                     |                                                                                        |
| DELETE | `/items/{item_id}`         | Deletes an item.                             | None                                                                                                                                                                                                                         |                                                                                        |
| GET    | `/items/`                      | Retrieves all items.                         | None                                                                                                                                                                                                                         | `{"item_name": {"name": "...", "stats": {...}, "description": "...", "price": ..., "sell_price": ...}}`                                                                     |
| GET    | `/hello/{name}`              | Returns a greeting with the given name.      | None                                                                                                                                                                                                                         | `{"message": "Hello {name}"}`                                                         |
| GET    | `/models/{model_name}`        | Returns information about a specific model.  | None                                                                                                                                                                                                                         | `{"model_name": "{model_name}", "message": "..."}` (Message depends on model name) |
| GET    | `/items_opt/{item_id}`       | Example item endpoint with optional parameters. | Query parameters: `q` (string), `short` (boolean)                                                                                                                                                                             | `{"item_id": "{item_id}", "q": "{q}", "description": "..."}`                      |
| GET    | `/users/{user_id}/items/{item_id}` | Example user item endpoint.                 | Query parameters: `q` (string), `short` (boolean)                                                                                                                                                                             | `{"item_id": "{item_id}", "owner_id": {user_id}, "q": "{q}", "description": "..."}` |

## Code Structure

*   `main.py`: The main FastAPI application file.
*   `items.py`: Defines the API routes related to items.
*   `pydantic_classes.py`: Defines the Pydantic models used for data validation and serialization (e.g., `Item`).
*   `data_base/`: Contains database-related files:
    *   `database_provider.py`: Provides a dependency injection function for accessing the database service.
    *   `database_service.py`: Defines the abstract base class for database services.
    *   `database_service_impl.py`: Implements the database service using SQLAlchemy.
    *   `database_service_impl_as_dict.py`: Implements the database service using a dictionary (for testing/example purposes).
    *   `sqlalchemy_db.py`: Defines the SQLAlchemy models and database setup.
*   `response_model_examples.py`: Defines some examples of response models

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

[Specify the License here, e.g., MIT License]
