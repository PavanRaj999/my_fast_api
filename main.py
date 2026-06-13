from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Product

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows your React app to connect
    allow_credentials=True,
    allow_methods=["*"],                      # Allows GET, POST, PUT, DELETE
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return "Hello world"

# list of products with 4 products like phones, laptops, pens, tables
products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

@app.get("/products/")
def get_all_products():
    return products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products/")
def create_product(product: Product):
    if any(existing.id == product.id for existing in products):
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products.append(product)
    return {"message": "Product created successfully", "product": product}

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index, product in enumerate(products):
        if product.id == product_id:
            products[index] = updated_product
            return {"message": "Product updated successfully", "product": updated_product}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product.id == product_id:
            deleted = products.pop(index)
            return {"message": "Product deleted successfully", "product": deleted}
    raise HTTPException(status_code=404, detail="Product not found")
    
