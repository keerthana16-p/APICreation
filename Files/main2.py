from typing import Optional, Union, List
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import json

app = FastAPI()

# Pydantic model for the product data
class ProductData(BaseModel):
    id: str
    name: str
    data: Optional[Union[dict, None]]
#Optional[dict] --> it can be of dict type or None
#Union[dict,None] --> it can be of one of the type in the  brackets

# Pydantic model to wrap a list of ProductData objects
class ProductList(BaseModel):
    products: List[ProductData]

# Pydantic model for a list of product IDs
class ProductIDList(BaseModel):
    ids: List[str]

# Endpoint to retrieve all products from the JSON file
@app.get("/products/", response_model=ProductList)
async def get_products():
    try:
        # Read data from products.json
        data_file = "products.json"
        with open(data_file, "r") as f:
            products = json.load(f)
        return {"products": products}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Products file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Unable to decode JSON data")

# Endpoint to store data to the JSON file
@app.post("/products/", response_model=dict)
async def store_products(products: ProductList):
    try:
        # Extract products list from the request
        products_list = products.products

        # Convert Pydantic models to dictionaries
        products_dict = [product.dict() for product in products_list]

        # Write data to products.json
        data_file = "products.json"
        with open(data_file, "w") as f:
            json.dump(products_dict, f, indent=2)

        return {"message": "Products stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve a product by its ID from the JSON file
@app.get("/products/{item_id}", response_model=ProductData)
async def get_product(item_id: str = Path(..., title="The ID of the product to fetch")):
    try:
        # Read data from products.json
        data_file = "products.json"
        with open(data_file, "r") as f:
            products = json.load(f)
        
        # Find the product by item_id
        for product in products:
            if product["id"] == item_id:
                return product
        
        # If product with item_id is not found, raise 404 HTTPException
        raise HTTPException(status_code=404, detail=f"Product with id {item_id} not found")
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Products file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Unable to decode JSON data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve details for multiple products by their IDs using post
@app.post("/products/details/", response_model=ProductList)
async def get_products_details(product_ids: ProductIDList):
    try:
        # Read data from products.json
        data_file = "products.json"
        with open(data_file, "r") as f:
            products = json.load(f)
        
        # Filter products based on the provided IDs
        filtered_products = [product for product in products if product["id"] in product_ids.ids]
        
        # If any of the requested IDs are not found, raise 404 HTTPException
        if len(filtered_products) != len(product_ids.ids):
            not_found_ids = set(product_ids.ids) - {product["id"] for product in filtered_products}
            raise HTTPException(status_code=404, detail=f"Products with ids {not_found_ids} not found")
        
        return {"products": filtered_products}
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Products file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Unable to decode JSON data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

