# FastAPI Product Management API

This is a FastAPI application for managing a list of products. It provides endpoints to retrieve all products, store new products, retrieve a product by ID, and retrieve multiple products by their IDs.

## Requirements

- Python 
- FastAPI
- Pydantic
- Uvicorn

## Setup

1. **Install the required packages:**
    ```sh
    pip install fastapi pydantic uvicorn
    ```

2. **Create the `main.py` file** and add the logic to create endpoints

3. **Run the application:**
    ```sh
    uvicorn main:app --reload
    ```

## Endpoints

- **GET /products/**: Retrieve all products.
- **POST /products/**: Store new products.
- **GET /products/{item_id}**: Retrieve a product by ID.
- **POST /products/details/**: Retrieve details for multiple products by their IDs.
