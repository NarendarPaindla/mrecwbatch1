```
# FastAPI E-Commerce API Classroom Curriculum

This README consolidates all module content and responses provided during our course on building a real-world E-Commerce API with FastAPI and MySQL.

---

## Module 1: Project Setup & First API  
*Objective:* Get students up and running with FastAPI, Uvicorn, and a MySQL connection. By the end of this module, they will be able to:  
- Install necessary packages  
- Establish a project folder structure  
- Spin up a “ping” endpoint  
- Connect to a MySQL database and verify via MySQL Workbench  

---

### 1. Prerequisites  
- Python 3.8+ installed  
- MySQL Server running locally (default port 3306)  
- MySQL Workbench installed and connected to your local server  
- Basic familiarity with terminal/command-line  

---

### 2. Folder Structure  
```bash
ecom-fastapi/  
├── .env                 # environment variables  
├── main.py              # FastAPI entrypoint  
├── db/                  
│   └── init.sql         # manual SQL scripts  
└── requirements.txt     # pinned dependencies  


---

### 3. Step-by-Step Instructions

1. **Create your project directory**

   ```bash
   mkdir ecom-fastapi && cd ecom-fastapi
   ```

2. **Initialize a virtual environment & activate**

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Create `requirements.txt`**

   ```
   fastapi
   uvicorn[standard]
   mysql-connector-python
   python-dotenv
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   Create a file named `.env` in the project root:

   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=fastapi_ecom
   ```

   > **Teaching Tip:** Emphasize **never** committing `.env` to version control.

6. **Manually create the sample database & table**

   * Open MySQL Workbench, connect to `localhost:3306`.
   * Run:

     ```sql
     CREATE DATABASE IF NOT EXISTS fastapi_ecom;
     USE fastapi_ecom;

     CREATE TABLE ping_test (
       id INT AUTO_INCREMENT PRIMARY KEY,
       message VARCHAR(50) NOT NULL
     );

     INSERT INTO ping_test (message) VALUES ('pong');
     ```

   > **Teaching Tip:** Have students watch you create the schema in MySQL Workbench UI.

7. **Create `main.py` with “ping” endpoint & DB connection**

   ```python
   # main.py
   from fastapi import FastAPI, HTTPException
   import mysql.connector
   from mysql.connector import Error
   from dotenv import load_dotenv
   import os

   # 1. Load env vars
   load_dotenv()
   DB_CONFIG = {
       'host': os.getenv('DB_HOST'),
       'port': os.getenv('DB_PORT'),
       'user': os.getenv('DB_USER'),
       'password': os.getenv('DB_PASSWORD'),
       'database': os.getenv('DB_NAME'),
   }

   app = FastAPI(title="E-Com API")

   # 2. Utility to get DB connection
   def get_db_connection():
       try:
           conn = mysql.connector.connect(**DB_CONFIG)
           return conn
       except Error as e:
           raise HTTPException(status_code=500, detail=f"DB Connection Error: {e}")

   # 3. /ping endpoint
   @app.get("/ping")
   def ping():
       conn = get_db_connection()
       cursor = conn.cursor(dictionary=True)
       cursor.execute("SELECT message FROM ping_test LIMIT 1;")
       result = cursor.fetchone()
       cursor.close()
       conn.close()

       if not result:
           raise HTTPException(status_code=404, detail="No ping record found")
       return {"message_from_db": result["message"]}
   ```

---

### 4. Live Coding Walkthrough

1. **Line 1–5:** Imports and `.env` loader
2. **Line 7–12:** Build a `DB_CONFIG` dict from environment variables
3. **Line 15:** Instantiate FastAPI app with a friendly title
4. **Line 18–25:** `get_db_connection()` tries to connect, raises 500 on failure
5. **Line 28–39:** Define `GET /ping`, execute a simple SELECT, return JSON

---

### 5. Running & Testing

1. **Start the server**

   ```bash
   uvicorn main:app --reload
   ```
2. **Postman (or curl) test**

   * **Request:** `GET http://127.0.0.1:8000/ping`
   * **Expected Response (200):**

     ```json
     {
       "message_from_db": "pong"
     }
     ```
3. **Verify in MySQL Workbench**

   * Refresh your schema in Workbench
   * View `ping_test` table and its `pong` row

---

### 6. Teaching Notes & Common Pitfalls

* **“ModuleNotFoundError: mysql.connector”** ⇒ forgot to install `mysql-connector-python`.
* **Connection refused** ⇒ MySQL isn’t running or credentials/port mismatch.
* **404 No ping record found** ⇒ table empty or typo in table name.

---

### 7. Mini Assignment

1. **DIY Table:** Create a new table `health_check(id, status)` with a single row `('OK')`.
2. **New Endpoint:** Add `GET /health` in `main.py` that queries `health_check` and returns its status.
3. **Postman:** Validate both `/ping` and `/health`.

---

### 8. Best Practices

* Always close cursors and connections in a `finally` block (or use context managers in later modules).
* Store secrets in `.env` and add it to `.gitignore`.
* Use a consistent project structure from day one.

---

✅ **Module 1 complete.**
*When you’re ready, say “Continue to next module”.*

---

## Module 2: Product Management APIs

*Objective:*
Implement full CRUD for a `products` resource using raw SQL in FastAPI. By the end of this module, students will be able to:

* Define a MySQL table for products
* Write Pydantic schemas for request/response bodies
* Perform Create, Read, Update, Delete via FastAPI endpoints
* View changes live in both Postman and MySQL Workbench

---

### 1. Create the `products` Table

1. **Open MySQL Workbench** and connect to your `fastapi_ecom` database.
2. **Run the following SQL**:

   ```sql
   USE fastapi_ecom;

   CREATE TABLE IF NOT EXISTS products (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(100) NOT NULL,
     description TEXT,
     price DECIMAL(10,2) NOT NULL
   );
   ```
3. **Verify** by refreshing the schema and doing:

   ```sql
   SELECT * FROM products;
   ```

   — you should see an empty result set.

> **Teaching Tip:** Emphasize using `DECIMAL` for money values to avoid floating-point rounding issues.

---

### 2. Define Pydantic Schemas

In **`main.py`**, add at the top:

```python
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
```

* **`ProductCreate`** is used for `POST`/`PUT` bodies.
* **`Product`** is the shape of data returned to clients.

---

### 3. Implement CRUD Endpoints

Below your existing `/ping` route, add:

```python
from fastapi import status

# 3.1 Create (POST /products)
@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
      INSERT INTO products (name, description, price)
      VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (payload.name, payload.description, payload.price))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return Product(id=new_id, **payload.dict())

# 3.2 Read All (GET /products)
@app.get("/products", response_model=list[Product])
def list_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Product(**row) for row in rows]

# 3.3 Read One (GET /products/{id})
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**row)

# 3.4 Update (PUT /products/{id})
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, payload: ProductCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
      UPDATE products
      SET name = %s, description = %s, price = %s
      WHERE id = %s
    """
    cursor.execute(sql, (payload.name, payload.description, payload.price, product_id))
    if cursor.rowcount == 0:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    conn.commit()
    cursor.close()
    conn.close()
    return Product(id=product_id, **payload.dict())

# 3.5 Delete (DELETE /products/{id})
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s;", (product_id,))
    if cursor.rowcount == 0:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    conn.commit()
    cursor.close()
    conn.close()
    return
```

---

### 4. Live Coding Walkthrough

1. **Parameterization**: All SQL uses `%s` placeholders—avoids SQL injection.
2. **`cursor.lastrowid`**: Retrieves the newly inserted record’s ID.
3. **Error paths**: Check `rowcount` for updates/deletes to raise 404 if no rows affected.
4. **Closing & Committing**: Always `commit()` after writes, and close cursor/connection.

---

### 5. Testing & Expected Outputs

| Endpoint                          | Request Body (JSON)                                                | Expected Response                                     |
| --------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------- |
| **POST** `/products`              | `{ "name":"T-shirt", "description":"Cotton", "price":19.99 }`      | `201 Created`<br>`{ "id":1, "name":"T-shirt", ... }`  |
| **GET** `/products`               | —                                                                  | `200 OK`<br>`[ { "id":1, "name":"T-shirt", ... } ]`   |
| **GET** `/products/1`             | —                                                                  | `200 OK`<br>`{ "id":1, "name":"T-shirt", ... }`       |
| **PUT** `/products/1`             | `{ "name":"T-shirt", "description":"100% cotton", "price":21.99 }` | `200 OK`<br>`{ "id":1, ...updated... }`               |
| **DELETE** `/products/1`          | —                                                                  | `204 No Content` (empty body)                         |
| **GET** `/products/1` (after del) | —                                                                  | `404 Not Found`<br>`{ "detail":"Product not found" }` |

> **Workbench Check:**
> After POST, run `SELECT * FROM products;` in MySQL Workbench and confirm your new row appears.

---

### 6. Teaching Tips & Common Pitfalls

* **Forgetting `conn.commit()`** → INSERT/UPDATE/DELETE won’t persist.
* **Mixing up parameter order** → `%s` placeholders must align with tuple order.
* **Leaving connections open** can exhaust MySQL connection pool.
* **Not handling non-existent IDs** → always check `rowcount` and return `404`.

---

### 7. Mini Assignments

1. **Add a `stock` column** (`INT NOT NULL DEFAULT 0`) to `products`.
2. **Extend** all CRUD endpoints and Pydantic models to handle `stock`.
3. **New Feature:** Create `GET /products?min_price=&max_price=` to filter products by price range.

---

### 8. Best Practices

* **Parameterize** all queries.
* **Use context managers** (`with conn.cursor() as cursor:`) in later modules to auto-close.
* **Centralize DB logic** via FastAPI dependencies when you refactor (Module 7+).
* **Keep error responses consistent**—consider a standard response schema in Module 7.

---

✅ **Module 2 complete.**
*When you’re ready, say “Continue to next module.”*

---

## Updated Module 2: Product Management APIs (with Folder Separation)

---

### 📁 Project Structure

```
ecom-fastapi/
├── app/
│   ├── db/
│   │   └── connection.py          # MySQL connection logic
│   ├── schemas/
│   │   └── product.py             # Pydantic models
│   ├── crud/
│   │   └── product.py             # Raw-SQL CRUD functions
│   ├── routes/
│   │   └── product.py             # FastAPI router for products
│   └── main.py                    # App entrypoint
├── .env
└── requirements.txt
```

---

#### 1. Update `app/db/connection.py`

```python
# app/db/connection.py
from mysql.connector import connect, Error
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("DB_HOST"),
    "port":     os.getenv("DB_PORT"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

def get_db_connection():
    try:
        return connect(**DB_CONFIG)
    except Error as e:
        raise HTTPException(status_code=500, detail=f"DB Connection Error: {e}")
```

#### 2. Update `app/schemas/product.py`

```python
# app/schemas/product.py
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
```

#### 3. Update `app/crud/product.py`

```python
# app/crud/product.py
from mysql.connector import connect
from app.db.connection import get_db_connection
from app.schemas.product import ProductCreate, Product
from fastapi import HTTPException, status

def create_product(payload: ProductCreate) -> Product:
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)"
    cursor.execute(sql, (payload.name, payload.description, payload.price))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return Product(id=new_id, **payload.dict())

def list_products() -> list[Product]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Product(**r) for r in rows]

def get_product_by_id(product_id: int) -> Product:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**row)

def update_product(product_id: int, payload: ProductCreate) -> Product:
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = ("UPDATE products SET name=%s, description=%s, price=%s "
           "WHERE id=%s")
    cursor.execute(sql, (payload.name, payload.description, payload.price, product_id))
    if cursor.rowcount == 0:
        conn.rollback()
        raise HTTPException(status_code=404, detail="Product not found")
    conn.commit()
    cursor.close()
    conn.close()
    return Product(id=product_id, **payload.dict())

def delete_product(product_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s;", (product_id,))
    if cursor.rowcount == 0:
        conn.rollback()
        raise HTTPException(status_code=404, detail="Product not found")
    conn.commit()
    cursor.close()
    conn.close()
```

#### 4. Update `app/routes/product.py`

```python
# app/routes/product.py
from fastapi import APIRouter, status
from app.crud.product import (
    create_product, list_products,
    get_product_by_id, update_product, delete_product
)
from app.schemas.product import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
def api_create_product(payload: ProductCreate):
    return create_product(payload)

@router.get("", response_model=list[Product])
def api_list_products():
    return list_products()

@router.get("/{product_id}", response_model=Product)
def api_get_product(product_id: int):
    return get_product_by_id(product_id)

@router.put("/{product_id}", response_model=Product)
def api_update_product(product_id: int, payload: ProductCreate):
    return update_product(product_id, payload)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_product(product_id: int):
    delete_product(product_id)
```

#### 5. Update `app/main.py`

```python
# app/main.py
from fastapi import FastAPI
from app.routes.product import router as product_router

app = FastAPI(title="E-Com API")
app.include_router(product_router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
```

#### 6. Live Coding Walkthrough

* **Folder setup:** `app/` holds all code; keeps concerns separated.
* **Connection module:** centralized DB logic.
* **Schemas:** only Pydantic models here.
* **CRUD:** raw SQL lives in `crud/`.
* **Routes:** FastAPI routers import only what they need.
* **Main:** minimal, just wires in routers.

#### 7. Testing & Expected Outputs

Use Postman or curl exactly as before—the behavior doesn’t change. In Workbench you’ll still see the same `products` rows.

#### 8. Teaching Tips & Pitfalls

* **Import errors** ⇒ check your `PYTHONPATH` or adjust `uvicorn app.main:app --reload`.
* **Circular imports** ⇒ keep `crud` free of router imports.
* **Missing commits** ⇒ no row changes appear in Workbench.

#### 9. Mini Assignment

1. Refactor your **health** endpoint (from Module 1) into the same folder layout:

   * `app/schemas/health.py`
   * `app/crud/health.py`
   * `app/routes/health.py`
2. Wire the new router in `main.py`.
3. Test `/health` in Postman and verify in Workbench.

#### 10. Best Practices

* Consistent folder naming (singular vs plural)
* Keep each file <200 LOC
* Centralize shared utilities (e.g., error handlers) in `app/core/` in Module 7+

---

**Module 2 (refactored) complete.**
Continuing with **Module 3: Category APIs** below.

---

## Module 3: Category APIs

---

### 📁 Updated Project Structure

```
ecom-fastapi/
└── app/
    ├── db/
    │   └── connection.py
    ├── schemas/
    │   ├── product.py
    │   └── category.py
    ├── crud/
    │   ├── product.py
    │   └── category.py
    ├── routes/
    │   ├── product.py
    │   └── category.py
    └── main.py
```

---

### 1. Create `categories` Table & Foreign Key

```sql
USE fastapi_ecom;

CREATE TABLE IF NOT EXISTS categories (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

ALTER TABLE products
  ADD COLUMN category_id INT NULL,
  ADD CONSTRAINT fk_prod_cat
    FOREIGN KEY (category_id)
    REFERENCES categories(id);
```

---

### 2. Define `app/schemas/category.py`

```python
# app/schemas/category.py
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# Extended response: product + category
class ProductWithCategory(Product):
    category: Category | None
```

---

### 3. Implement `app/crud/category.py`

```python
# app/crud/category.py
from app.db.connection import get_db_connection
from app.schemas.category import Category, CategoryCreate
from fastapi import HTTPException

def create_category(payload: CategoryCreate) -> Category:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO categories (name) VALUES (%s)", (payload.name,))
    conn.commit()
    new_id = cur.lastrowid
    cur.close(); conn.close()
    return Category(id=new_id, **payload.dict())

def list_categories() -> list[Category]:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM categories;")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return [Category(**r) for r in rows]

def get_category(cat_id: int) -> Category:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM categories WHERE id=%s", (cat_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(404, "Category not found")
    return Category(**row)

# BONUS: join products + category
def list_products_by_category(cat_id: int) -> list[dict]:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    sql = """
      SELECT p.id,p.name,p.description,p.price,
             c.id AS category_id, c.name AS category_name
      FROM products p
      JOIN categories c ON p.category_id = c.id
      WHERE c.id = %s
    """
    cur.execute(sql, (cat_id,))
    rows = []
    for r in cur.fetchall():
        rows.append({
          "id":           r["id"],
          "name":         r["name"],
          "description":  r["description"],
          "price":        r["price"],
          "category": {
            "id":   r["category_id"],
            "name": r["category_name"]
          }
        })
    cur.close(); conn.close()
    return rows
```

---

### 4. Implement `app/routes/category.py`

```python
# app/routes/category.py
from fastapi import APIRouter, status
from app.crud.category import (
    create_category, list_categories,
    get_category, list_products_by_category
)
from app.schemas.category import Category, CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def api_create_category(payload: CategoryCreate):
    return create_category(payload)

@router.get("", response_model=list[Category])
def api_list_categories():
    return list_categories()

@router.get("/{cat_id}", response_model=Category)
def api_get_category(cat_id: int):
    return get_category(cat_id)

@router.get("/{cat_id}/products")
def api_list_products_by_category(cat_id: int):
    return list_products_by_category(cat_id)
```

---

### 5. Update `app/main.py`

```python
# app/main.py
from fastapi import FastAPI
from app.routes.product import router as product_router
from app.routes.category import router as category_router

app = FastAPI(title="E-Com API")
app.include_router(product_router)
app.include_router(category_router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
```

---

### 6. Live Coding & Testing

* **Create & link categories** in Workbench.
* **POST** `/categories` → `{ "name": "Clothing" }` → 201 + new ID.
* **PUT** on products to assign `category_id`.
* **GET** `/categories/{id}/products` → list of products with category object.

---

### 7. Teaching Tips

* Show **Workbench EER Diagram** to illustrate FK relation.
* Emphasize how joins work under the hood.
* Common error: “Cannot add foreign key constraint” → data type mismatch or missing index.

---

### 8. Assignment

1. Add **DELETE** and **PUT** endpoints for categories (similar to products).
2. Protect **DELETE** so it fails if products exist (use SQL `ON DELETE RESTRICT`).
3. Test all flows in Postman and verify side by side in Workbench.

---

### 9. Best Practices

* Keep your `JOIN` logic in `crud/`, not in routes.
* Return nested objects, not flat DB rows—map them in Python.

---

✅ **Module 3 complete.**
*Continuing next with **Module 4: Cart System**…*

---

## Module 4: Cart System

*Objective:*
Implement a simple cart system (per-user, mocked) with `cart` and `cart_items` tables. Students will learn:

* Designing related tables
* Raw SQL for multi-table operations
* Exposing cart APIs (add/remove/view)
* Handling “session” or “current user” in lieu of auth

---

### 📁 Project Structure

```
app/
├── schemas/
│   ├── product.py
│   ├── category.py
│   └── cart.py           # NEW
├── crud/
│   ├── product.py
│   ├── category.py
│   └── cart.py           # NEW
├── routes/
│   ├── product.py
│   ├── category.py
│   └── cart.py           # NEW
└── db/connection.py
```

---

### 1. Create Tables in MySQL Workbench

```sql
USE fastapi_ecom;

CREATE TABLE IF NOT EXISTS cart (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  user_id  INT NOT NULL,             -- in real app: FK to users
  created  DATETIME DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cart_items (
  id        INT AUTO_INCREMENT PRIMARY KEY,
  cart_id   INT NOT NULL,
  product_id INT NOT NULL,
  quantity  INT NOT NULL DEFAULT 1,
  CONSTRAINT fk_ci_cart FOREIGN KEY (cart_id) REFERENCES cart(id),
  CONSTRAINT fk_ci_prod FOREIGN KEY (product_id) REFERENCES products(id)
);
```

> **Teaching Tip:** Explain why we separate `cart` and `cart_items` (1\:N relationship).

---

### 2. Define **`app/schemas/cart.py`**

```python
# app/schemas/cart.py
from pydantic import BaseModel

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    created: str           # ISO timestamp
    items: list[CartItem] = []

    class Config:
        orm_mode = True
```

---

### 3. Implement **`app/crud/cart.py`**

```python
# app/crud/cart.py
from app.db.connection import get_db_connection
from app.schemas.cart import CartCreate, Cart, CartItemCreate, CartItem
from fastapi import HTTPException

# Helper: ensure cart exists (or create it)
def get_or_create_cart(user_id: int) -> int:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM cart WHERE user_id=%s;", (user_id,))
    row = cur.fetchone()
    if row:
        cart_id = row["id"]
    else:
        cur.execute("INSERT INTO cart (user_id) VALUES (%s);", (user_id,))
        conn.commit()
        cart_id = cur.lastrowid
    cur.close(); conn.close()
    return cart_id

def add_item_to_cart(user_id: int, payload: CartItemCreate) -> CartItem:
    cart_id = get_or_create_cart(user_id)
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    # If item exists, increment quantity
    cur.execute(
      "SELECT id, quantity FROM cart_items WHERE cart_id=%s AND product_id=%s;",
      (cart_id, payload.product_id)
    )
    row = cur.fetchone()
    if row:
        new_qty = row["quantity"] + payload.quantity
        cur.execute(
          "UPDATE cart_items SET quantity=%s WHERE id=%s;",
          (new_qty, row["id"])
        )
        item_id = row["id"]
    else:
        cur.execute(
          "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s,%s,%s);",
          (cart_id, payload.product_id, payload.quantity)
        )
        item_id = cur.lastrowid
    conn.commit()

    # Retrieve updated item
    cur.execute("SELECT * FROM cart_items WHERE id=%s;", (item_id,))
    item = cur.fetchone()
    cur.close(); conn.close()
    return CartItem(**item)

def remove_item_from_cart(user_id: int, item_id: int) -> None:
    cart_id = get_or_create_cart(user_id)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
      "DELETE FROM cart_items WHERE id=%s AND cart_id=%s;",
      (item_id, cart_id)
    )
    if cur.rowcount == 0:
        conn.rollback()
        raise HTTPException(status_code=404, detail="Cart item not found")
    conn.commit()
    cur.close(); conn.close()

def view_cart(user_id: int) -> Cart:
    cart_id = get_or_create_cart(user_id)
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    # Get cart meta
    cur.execute("SELECT * FROM cart WHERE id=%s;", (cart_id,))
    cart_row = cur.fetchone()
    # Get items
    cur.execute("SELECT * FROM cart_items WHERE cart_id=%s;", (cart_id,))
    items = [CartItem(**r) for r in cur.fetchall()]
    cur.close(); conn.close()
    return Cart(id=cart_row["id"], user_id=user_id, created=cart_row["created"], items=items)
```

---

### 4. Implement **`app/routes/cart.py`**

```python
# app/routes/cart.py
from fastapi import APIRouter, Depends, status
from app.crud.cart import add_item_to_cart, remove_item_from_cart, view_cart
from app.schemas.cart import CartItemCreate, Cart
from typing import Dict

router = APIRouter(prefix="/cart", tags=["cart"])

# Dummy “get current user” (mock)
def get_current_user() -> Dict[str,int]:
    # In real app: extract from JWT; here we hardcode
    return {"user_id": 1}

@router.post(
    "/items",
    response_model=CartItemCreate,
    status_code=status.HTTP_201_CREATED
)
def api_add_to_cart(
    payload: CartItemCreate,
    user=Depends(get_current_user)
):
    return add_item_to_cart(user["user_id"], payload)

@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def api_remove_from_cart(
    item_id: int,
    user=Depends(get_current_user)
):
    remove_item_from_cart(user["user_id"], item_id)

@router.get("", response_model=Cart)
def api_view_cart(user=Depends(get_current_user)):
    return view_cart(user["user_id"])
```

---

### 5. Update **`app/main.py`**

```python
from fastapi import FastAPI
from app.routes.product import router as product_router
from app.routes.category import router as category_router
from app.routes.cart import router as cart_router

app = FastAPI(title="E-Com API")
app.include_router(product_router)
app.include_router(category_router)
app.include_router(cart_router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
```

---

### 6. Live Coding & Testing

1. **Create tables** in Workbench as above.
2. **POST** `/cart/items`

   ```json
   { "product_id": 2, "quantity": 3 }
   ```

   → `201 Created` + `{ "product_id":2, "quantity":3 }`
3. **GET** `/cart`

   ```json
   {
     "id": 1,
     "user_id": 1,
     "created": "2025-07-21T15:30:00",
     "items":[ { "id":5, "product_id":2, "quantity":3 } ]
   }
   ```
4. **DELETE** `/cart/items/5` → `204 No Content`

In MySQL Workbench, run:

```sql
SELECT * FROM cart;
SELECT * FROM cart_items;
```

to see the persisted rows.

---

### 7. Teaching Tips & Pitfalls

* **Mocked user**: clarify that auth will come later in Module 9.
* **Foreign key errors**: ensure `product_id` exists in `products`.
* **Quantity logic**: test adding the same product twice (should increment).

---

### 8. Mini Assignment

1. Extend **`api_add_to_cart`** to reject `quantity < 1`.
2. Add a **`PUT /cart/items/{item_id}`** to update quantity directly.
3. Test edge cases: removing non-existent item, viewing empty cart.

---

### 9. Best Practices

* Centralize “current user” logic in a dependency (will evolve in Module 9).
* Use transactions (BEGIN/COMMIT) when multi-step operations become complex (Module 5).

---

✅ **Module 4 complete.**
*When you’re ready, say “Continue to next module.”*

---

## Consolidated API Endpoints (Modules 1–4)

Here’s a consolidated list of all the endpoints you’ve built so far (Modules 1–4), with example requests and responses. You can plug these into Postman or curl as shown.

---

### 1. General Health Check

#### **GET** `/ping`

> **Purpose:** Verify server and DB connectivity.

```bash
curl http://127.0.0.1:8000/ping
```

**Response 200 OK**

```json
{
  "message_from_db": "pong"
}
```

---

### 2. Products

#### **POST** `/products`

> **Create a new product**

**Request**

```
POST /products
Content-Type: application/json

{
  "name": "T-shirt",
  "description": "100% cotton",
  "price": 19.99
}
```

**Response 201 Created**

```json
{
  "id": 1,
  "name": "T-shirt",
  "description": "100% cotton",
  "price": 19.99
}
```

---

#### **GET** `/products`

> **List all products**

```bash
curl http://127.0.0.1:8000/products
```

**Response 200 OK**

```json
[
  {
    "id": 1,
    "name": "T-shirt",
    "description": "100% cotton",
    "price": 19.99
  },
  {
    "id": 2,
    "name": "Mug",
    "description": "Ceramic mug, 350 ml",
    "price": 9.50
  }
]
```

---

#### **GET** `/products/{product_id}`

> **Get one product by ID**

```bash
curl http://127.0.0.1:8000/products/1
```

**Response 200 OK**

```json
{
  "id": 1,
  "name": "T-shirt",
  "description": "100% cotton",
  "price": 19.99
}
```

**Response 404 Not Found**

```json
{ "detail": "Product not found" }
```

---

#### **PUT** `/products/{product_id}`

> **Update an existing product**

**Request**

```
PUT /products/1
Content-Type: application/json

{
  "name": "T-shirt",
  "description": "100% organic cotton",
  "price": 21.99
}
```

**Response 200 OK**

```json
{
  "id": 1,
  "name": "T-shirt",
  "description": "100% organic cotton",
  "price": 21.99
}
```

**Response 404 Not Found**

```json
{ "detail": "Product not found" }
```

---

#### **DELETE** `/products/{product_id}`

> **Delete a product**

```bash
curl -X DELETE http://127.0.0.1:8000/products/1
```

**Response 204 No Content** (empty body)

**Response 404 Not Found**

```json
{ "detail": "Product not found" }
```

---

### 3. Categories

#### **POST** `/categories`

> **Create a new category**

**Request**

```
POST /categories
Content-Type: application/json

{
  "name": "Clothing"
}
```

**Response 201 Created**

```json
{
  "id": 1,
  "name": "Clothing"
}
```

---

#### **GET** `/categories`

> **List all categories**

```bash
curl http://127.0.0.1:8000/categories
```

**Response 200 OK**

```json
[
  {
    "id": 1,
    "name": "Clothing"
  },
  {
    "id": 2,
    "name": "Home & Kitchen"
  }
]
```

---

#### **GET** `/categories/{cat_id}`

> **Get one category by ID**

```bash
curl http://127.0.0.1:8000/categories/1
```

**Response 200 OK**

```json
{
  "id": 1,
  "name": "Clothing"
}
```

**Response 404 Not Found**

```json
{ "detail": "Category not found" }
```

---

#### **GET** `/categories/{cat_id}/products`

> **List products in a category (with nested category info)**

```bash
curl http://127.0.0.1:8000/categories/1/products
```

**Response 200 OK**

```json
[
  {
    "id": 2,
    "name": "Mug",
    "description": "Ceramic mug, 350 ml",
    "price": 9.50,
    "category": {
      "id": 1,
      "name": "Clothing"
    }
  }
]
```

---

### 4. Cart System

> **Note:** We’re mocking `user_id=1` via a dependency until Module 9.

#### **POST** `/cart/items`

> **Add product to cart (or increment quantity)**

**Request**

```
POST /cart/items
Content-Type: application/json

{
  "product_id": 2,
  "quantity": 3
}
```

**Response 201 Created**

```json
{
  "id": 5,
  "product_id": 2,
  "quantity": 3
}
```

---

#### **GET** `/cart`

> **View current user’s cart**

```bash
curl http://127.0.0.1:8000/cart
```

**Response 200 OK**

```json
{
  "id": 1,
  "user_id": 1,
  "created": "2025-07-21T15:30:00",
  "items": [
    {
      "id": 5,
      "product_id": 2,
      "quantity": 3
    }
  ]
}
```

---

#### **DELETE** `/cart/items/{item_id}`

> **Remove an item from cart**

```bash
curl -X DELETE http://127.0.0.1:8000/cart/items/5
```

**Response 204 No Content** (empty body)

**Response 404 Not Found**

```json
{ "detail": "Cart item not found" }
```

---

*That’s all the endpoints to date!* Let me know when you’re ready to move on or if you need example curl/Postman collections exported.

---

## Module 5: Order Placement

*Objective:*
Implement “place order” functionality using SQL transactions and provide APIs to place an order, view a single order, and list all orders. By the end of this module, students will be able to:

* Design `orders` and `order_items` tables
* Use transactions (`BEGIN`/`COMMIT`/`ROLLBACK`) in raw SQL
* Compute and persist order totals & item-level prices
* Expose POST/GET endpoints in FastAPI

---

### 1. Create Tables in MySQL Workbench

```sql
USE fastapi_ecom;

-- Orders table with total_amount snapshot
CREATE TABLE IF NOT EXISTS orders (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  user_id       INT NOT NULL,
  total_amount  DECIMAL(10,2) NOT NULL,
  created       DATETIME DEFAULT NOW()
);

-- Order items with price snapshot at time of purchase
CREATE TABLE IF NOT EXISTS order_items (
  id                   INT AUTO_INCREMENT PRIMARY KEY,
  order_id             INT NOT NULL,
  product_id           INT NOT NULL,
  quantity             INT NOT NULL,
  price_at_purchase    DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_oi_order FOREIGN KEY (order_id) REFERENCES orders(id),
  CONSTRAINT fk_oi_prod  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

> **Teaching Tip:**
>
> * Emphasize **why** we snapshot `price_at_purchase` (so historical orders aren’t affected by later price changes).
> * Show EER diagram to illustrate 1→N from `orders` to `order_items`.

---

### 2. Define Schemas (`app/schemas/order.py`)

```python
# app/schemas/order.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price_at_purchase: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    total_amount: float
    created: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True
```

---

### 3. CRUD Logic (`app/crud/order.py`)

```python
# app/crud/order.py
from app.db.connection import get_db_connection
from app.schemas.order import OrderCreate, Order
from fastapi import HTTPException
from mysql.connector import Error

def place_order(payload: OrderCreate) -> Order:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()

        # 1. Compute total_amount
        total = 0.0
        for item in payload.items:
            cur.execute("SELECT price FROM products WHERE id = %s;", (item.product_id,))
            prod = cur.fetchone()
            if not prod:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            total += prod["price"] * item.quantity

        # 2. Insert into orders
        cur.execute(
            "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s);",
            (payload.user_id, total)
        )
        order_id = cur.lastrowid

        # 3. Insert each order_item
        for item in payload.items:
            # reuse price snapshot
            cur.execute("SELECT price FROM products WHERE id = %s;", (item.product_id,))
            price = cur.fetchone()["price"]
            cur.execute(
                """INSERT INTO order_items
                   (order_id, product_id, quantity, price_at_purchase)
                   VALUES (%s, %s, %s, %s);""",
                (order_id, item.product_id, item.quantity, price)
            )

        conn.commit()

        # 4. Return full order
        return get_order_by_id(order_id)

    except HTTPException:
        conn.rollback()
        raise
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Order placement failed: {e}")
    finally:
        cur.close()
        conn.close()

def get_order_by_id(order_id: int) -> Order:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    # Fetch order meta
    cur.execute("SELECT * FROM orders WHERE id = %s;", (order_id,))
    order_row = cur.fetchone()
    if not order_row:
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Order not found")

    # Fetch items
    cur.execute("SELECT * FROM order_items WHERE order_id = %s;", (order_id,))
    items = cur.fetchall()

    cur.close(); conn.close()
    return Order(
        id=order_row["id"],
        user_id=order_row["user_id"],
        total_amount=float(order_row["total_amount"]),
        created=order_row["created"],
        items=[{**item} for item in items]
    )

def list_orders() -> list[Order]:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM orders ORDER BY created DESC;")
    order_ids = [row["id"] for row in cur.fetchall()]
    cur.close(); conn.close()
    return [get_order_by_id(o) for o in order_ids]
```

---

### 4. Routes (`app/routes/order.py`)

```python
# app/routes/order.py
from fastapi import APIRouter, status, Depends
from app.schemas.order import OrderCreate, Order
from app.crud.order import place_order, get_order_by_id, list_orders
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

# Mocked dependency
def get_current_user():
    return {"user_id": 1}

@router.post(
    "",
    response_model=Order,
    status_code=status.HTTP_201_CREATED
)
def api_place_order(
    payload: OrderCreate,
    user=Depends(get_current_user)
):
    payload.user_id = user["user_id"]
    return place_order(payload)

@router.get(
    "",
    response_model=List[Order]
)
def api_list_orders():
    return list_orders()

@router.get(
    "/{order_id}",
    response_model=Order
)
def api_get_order(order_id: int):
    return get_order_by_id(order_id)
```

---

### 5. Update `app/main.py`

```python
# app/main.py
from fastapi import FastAPI
from app.routes.product  import router as product_router
from app.routes.category import router as category_router
from app.routes.cart     import router as cart_router
from app.routes.order    import router as order_router

app = FastAPI(title="E-Com API")
app.include_router(product_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
```

---

### 6. Live Coding & Testing

1. **Start server**

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Place Order**

   ```
   POST /orders
   Content-Type: application/json

   {
     "items": [
       { "product_id": 2, "quantity": 1 },
       { "product_id": 3, "quantity": 2 }
     ]
   }
   ```

   **Response 201 Created**

   ```json
   {
     "id": 1,
     "user_id": 1,
     "total_amount": 39.48,
     "created": "2025-07-21T16:00:00",
     "items": [
       { "id": 1, "product_id": 2, "quantity": 1, "price_at_purchase": 9.50 },
       { "id": 2, "product_id": 3, "quantity": 2, "price_at_purchase": 14.99 }
     ]
   }
   ```

3. **List Orders**

   ```
   GET /orders
   ```

   **Response 200 OK**

   ```json
   [
     { /* order #1 as above */ }
   ]
   ```

4. **Get One Order**

   ```
   GET /orders/1
   ```

   **Response 200 OK**

   ```json
   { /* same payload as POST response */ }
   ```

---

### 7. Teaching Tips & Common Pitfalls

* **Transactions:** Always `ROLLBACK` on exceptions to avoid partial data.
* **Price Snapshot:** If you forget to snapshot price, later price changes will corrupt past orders.
* **Multiple Queries:** Be mindful of cursor reuse; fetch product price once per item.

---

### 8. Mini Assignment

1. Add an **`order_status`** column (`ENUM('PENDING','SHIPPED','CANCELLED')`) to `orders`, default `PENDING`.
2. Create a **`PATCH /orders/{order_id}/status`** endpoint to update status.
3. Test status transitions and ensure invalid statuses result in `400 Bad Request`.

---

### 9. Best Practices

* Keep business logic (transactions, validation) in `crud/`, routes stay thin.
* Consider moving repeated SQL (e.g. price lookup) into helper functions.
* Use proper isolation levels for concurrent orders in a production setting.

---

✅ **Module 5 complete.**
*When you’re ready, say “Continue to next module.”*

---

## Module 6: Pagination, Search, and Sorting

*Objective:*
Enhance the product listing endpoint to support pagination, keyword search (on name/description), and price-based sorting. By the end of this module, students will be able to:

* Accept query parameters (`page`, `size`, `search`, `sort`) in routes
* Dynamically build raw SQL with `WHERE`, `ORDER BY`, `LIMIT OFFSET`
* Return paginated subsets of products efficiently
* Validate query inputs

---

### 1. Update CRUD Logic: `app/crud/product.py`

```python
# app/crud/product.py
from typing import Optional
from app.db.connection import get_db_connection
from app.schemas.product import Product

def list_products(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    sort: Optional[str] = None
) -> list[Product]:
    offset = (page - 1) * size
    # Base query
    sql = "SELECT * FROM products"
    params: list = []

    # 1. Filtering
    if search:
        sql += " WHERE name LIKE %s OR description LIKE %s"
        params += [f"%{search}%", f"%{search}%"]

    # 2. Sorting
    if sort == "price_asc":
        sql += " ORDER BY price ASC"
    elif sort == "price_desc":
        sql += " ORDER BY price DESC"
    else:
        sql += " ORDER BY id ASC"

    # 3. Pagination
    sql += " LIMIT %s OFFSET %s"
    params += [size, offset]

    # Execute
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [Product(**row) for row in rows]
```

---

### 2. Update Route to Accept Query Params: `app/routes/product.py`

```python
# app/routes/product.py
from typing import List, Optional
from fastapi import APIRouter, Query
from app.crud.product import list_products
from app.schemas.product import Product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[Product])
def api_list_products(
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(
        None,
        title="Search term",
        description="Filter products by name or description"
    ),
    sort: Optional[str] = Query(
        None,
        regex="^price_(asc|desc)$",
        description="Sort by price: 'price_asc' or 'price_desc'"
    )
):
    """
    List products with optional pagination, search, and sorting.
    """
    return list_products(page, size, search, sort)
```

---

### 3. Live Coding Walkthrough

1. **Query Params**: We use `fastapi.Query` to enforce constraints (`ge=1`, regex for `sort`).
2. **Dynamic SQL**:

   * **Filtering**: Append `WHERE name LIKE %s OR description LIKE %s` when `search` is provided.
   * **Sorting**: Use `ORDER BY price ASC/DESC` or fallback to `id ASC`.
   * **Pagination**: `LIMIT size OFFSET (page−1)*size`.
3. **Parameterization**: All user inputs go into parameter tuple—protects against SQL injection.
4. **Result Mapping**: Convert each DB row to a `Product` via Pydantic for consistent serialization.

---

### 4. Testing & Expected Outputs

| Request                                                 | Description                    | Example Response                        |
| ------------------------------------------------------- | ------------------------------ | --------------------------------------- |
| `GET /products`                                         | Default list (page 1, size 10) | Array of first 10 products              |
| `GET /products?page=2&size=5`                           | Page 2, 5 items per page       | Products 6–10                           |
| `GET /products?search=shirt`                            | Name/desc contains “shirt”     | Only products matching “shirt”          |
| `GET /products?sort=price_desc`                         | Sort by price high→low         | All products sorted descending by price |
| `GET /products?page=1&size=3&search=mug&sort=price_asc` | Combined filters               | First 3 “mug” products sorted low→high  |

#### Example JSON (`GET /products?page=1&size=2&search=shirt&sort=price_asc`):

```json
[
  {
    "id": 4,
    "name": "Blue T-shirt",
    "description": "Lightweight",
    "price": 12.99
  },
  {
    "id": 8,
    "name": "Green T-shirt",
    "description": "Organic cotton",
    "price": 14.50
  }
]
```

---

### 5. Teaching Tips & Common Pitfalls

* **Off-by-one**: Remember `OFFSET = (page−1)*size`.
* **SQL syntax**: Ensure the `WHERE` clause is only added once—avoid appending multiple `WHERE`s.
* **Parameter order**: The `params` list must match the `%s` placeholders in sequence.
* **Validation**: Use `Query()` constraints to catch invalid input early.

---

### 6. Mini Assignment

1. **Return metadata**: Modify route to return `{ "total": <count>, "page":…, "size":…, "products":[…] }`.
2. **Category filter**: Add `category_id` as an optional query param to filter by category.
3. **Multi-field sort**: Allow `sort=name_asc` or `name_desc` in addition to price sorting.

---

### 7. Best Practices

* For large tables, consider adding indexes on `name`/`description` or use full-text search.
* Always limit maximum `size` to prevent very large payloads.
* In production, consider keyset pagination for high-volume APIs.

---

✅ **Module 6 complete.**
*When you’re ready, say “Continue to next module.”*

---

## Module 7: Error Handling & Validation

*Objective:*
Improve robustness by adding strict input validation and centralized error handling so that all errors return a consistent JSON structure.

---

### 1. Strengthen Pydantic Schemas

Use `Field()` for length, value, and pattern checks. Example update in **`app/schemas/product.py`**:

```python
from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Product name, 1–100 chars")
    description: Optional[str] = Field(None, max_length=500,
                                       description="Optional, up to 500 chars")
    price: float = Field(..., gt=0,
                         description="Must be greater than 0")
```

Similarly, update other schemas:

* **CategoryBase**: `name: str = Field(..., min_length=1, max_length=100)`
* **CartItemBase**: `quantity: int = Field(..., ge=1, le=100, description="1–100")`
* **OrderItemBase**: same quantity constraints

---

### 2. Standardize Success Responses

Create **`app/core/response.py`**:

```python
# app/core/response.py
from pydantic import BaseModel
from typing import Any

class SuccessResponse(BaseModel):
    success: bool = True
    data: Any
```

---

### 3. Global Exception Handlers

Update **`app/main.py`** to catch and wrap all errors:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes.product  import router as product_router
# … import other routers …

app = FastAPI(title="E-Com API")

# Include routers
app.include_router(product_router)
# … other routers …

# 1. HTTPException handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

# 2. Validation errors (Pydantic)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": exc.errors()}
    )

# 3. Fallback for uncaught exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # In production: log exc
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal Server Error"}
    )

@app.get("/ping")
def ping():
    return {"message": "pong"}
```

---

### 4. Wrap Success in Routes

Example refactor of **`app/routes/product.py`** (only the list endpoint shown; apply similarly elsewhere):

```python
from fastapi import APIRouter, Query
from typing import List, Optional
from app.crud.product import list_products
from app.schemas.product import Product
from app.core.response import SuccessResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=SuccessResponse)
def api_list_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    sort: Optional[str] = None
):
    products = list_products(page, size, search, sort)
    return SuccessResponse(data=products)
```

> **Teaching Tip:**
>
> * Show before/after of a raw list vs. wrapped JSON.
> * Remind students to update **all** routes to use `SuccessResponse`.

---

### 5. Demonstration & Testing

1. **Validation error** (empty name & negative price):

   ```bash
   POST /products  
   { "name": "", "price": -5 }
   ```

   **Response 422**

   ```json
   {
     "success": false,
     "error": [
       { "loc":["body","name"], "msg":"ensure this value has at least 1 characters", … },
       { "loc":["body","price"], "msg":"value must be greater than 0", … }
     ]
   }
   ```

2. **DB connection failure** (stop MySQL, then):

   ```bash
   GET /ping
   ```

   **Response 500**

   ```json
   {
     "success": false,
     "error": "DB Connection Error: 2003: Can't connect to MySQL server on 'localhost' (10061)"
   }
   ```

3. **Successful list**:

   ```bash
   GET /products
   ```

   **Response 200**

   ```json
   {
     "success": true,
     "data": [
       { "id":1, "name":"T-shirt", … },
       { "id":2, … }
     ]
   }
   ```

---

### 6. Common Pitfalls & Tips

* **Unwrapped exceptions**: forgetting to raise `HTTPException` in CRUD leads to generic 500 without detail.
* **Inconsistent schemas**: ensure all routes’ `response_model` match the wrapped structure.
* **Overly strict validators**: use balanced `min_length`/`max_length` to avoid rejecting valid data.

---

### 7. Mini Assignment

1. Update **all** your route functions to return `SuccessResponse`.
2. Apply `Field()` validations to **Category**, **CartItem**, and **OrderItem** schemas.
3. (Bonus) Create a middleware that logs every incoming request’s path and method.

---

✅ **Module 7 complete.**
*When you’re ready, say “Continue to next module.”*

---

## Module 8: Schema Migrations

*Objective:*
Show how to evolve your database schema safely—first via manual changes in MySQL Workbench, then introduce Alembic for automated migrations if you transition to SQLAlchemy ORM later.

---

### 1. Manual Schema Changes in MySQL Workbench

> **Use case:** When not using an ORM, you’ll often manually alter tables.

1. **Open MySQL Workbench**, connect to `fastapi_ecom`.
2. **Alter an existing table**. For example, add a `stock` column to `products`:

   ```sql
   USE fastapi_ecom;

   ALTER TABLE products
     ADD COLUMN stock INT NOT NULL DEFAULT 0;
   ```
3. **Verify**:

   ```sql
   DESCRIBE products;
   SELECT id, name, price, stock FROM products LIMIT 5;
   ```

   * You should see the new `stock` column with default `0`.
4. **Teaching Tip:**

   * Emphasize using `ALTER TABLE … ADD COLUMN IF NOT EXISTS` for safety in scripts.
   * Show the Visual SQL Editor in Workbench—drag-and-drop columns for non-scripted changes.

---

### 2. Introducing Alembic (Optional, for ORM Phase)

> **Why Alembic?** When you adopt SQLAlchemy ORM, Alembic automates schema versioning through migration scripts.

#### 2.1 Install & Initialize

```bash
# Inside your virtualenv
pip install alembic
alembic init alembic
```

* Creates an `alembic/` folder and `alembic.ini`.

#### 2.2 Configure `alembic.ini` & `env.py`

1. **alembic.ini**:

   ```ini
   [alembic]
   script_location = alembic

   [alembic:env]
   sqlalchemy.url = mysql+mysqlconnector://<USER>:<PASS>@localhost:3306/fastapi_ecom
   ```
2. **alembic/env.py**:

   ```python
   from logging.config import fileConfig
   from sqlalchemy import engine_from_config
   from sqlalchemy import pool
   from alembic import context
   from app.db.base import Base   # your SQLAlchemy metadata
   # …

   config = context.config
   fileConfig(config.config_file_name)
   target_metadata = Base.metadata
   ```

#### 2.3 Generate & Apply a Migration

```bash
# Auto-detect changes (requires your models to be defined in SQLAlchemy)
alembic revision --autogenerate -m "Add stock to products"

# Review the generated script in alembic/versions/
# Then apply:
alembic upgrade head
```

* **Expected output**:

  ```
  INFO  [alembic.runtime.migration] Context impl MySQLImpl.
  INFO  [alembic.runtime.migration] Will assume transactional DDL.
  INFO  [alembic.runtime.migration] Running upgrade  -> <revision_id>, Add stock to products
  ```

> **Teaching Tip:**
>
> * Always review autogenerated scripts before applying.
> * Version-control the `alembic/versions/` directory.

---

### 3. Teaching Notes & Common Pitfalls

* **Manual edits vs migrations**: Manual Workbench changes can drift from code; migrations codify your schema history.
* **Autogenerate limitations**: Alembic needs access to your SQLAlchemy `Base.metadata`—you must import all models.
* **Idempotency**: Wrap `ALTER TABLE` in `IF NOT EXISTS` in scripts for safe re-runs.
* **Environment vars**: Avoid hard-coding DB URLs; read from `.env` in `env.py`.

---

### 4. Mini Assignment

1. **Manual change**: In Workbench, add a `discount` column (`DECIMAL(5,2) DEFAULT 0.00`) to `products`. Verify with `DESCRIBE`.
2. **Alembic practice** (optional):

   * Define a simple SQLAlchemy `Product` model with the new `discount` field in `app/db/base.py`.
   * Run `alembic revision --autogenerate -m "Add discount to products"`.
   * Inspect & apply the migration.
3. **Verification**: Use `SELECT discount FROM products;` in Workbench and test CRUD endpoints to ensure no breakage.

---

### 5. Best Practices

* **Version control** ALL migration scripts.
* **Keep manual and automated migrations in sync**: If you manually change, generate a corresponding Alembic revision.
* **Backup** before major schema changes in production.

---

✅ **Module 8 complete.**
*When you’re ready, say “Continue to next module.”*

---

## Module 9: JWT Authentication

*Objective:*
Introduce user registration/login with password hashing and JWTs, and protect selected endpoints (e.g., `/orders`) via FastAPI dependencies. By the end of this module, students will be able to:

* Create `users` table and Pydantic schemas
* Hash passwords with `bcrypt`
* Generate and validate JWT access tokens with PyJWT
* Protect routes using `OAuth2PasswordBearer` and `Depends`

---

### 📁 Project Structure Updates

```
ecom-fastapi/
└── app/
    ├── auth/
    │   ├── jwt.py                 # JWT helpers
    │   └── deps.py                # auth dependencies
    ├── schemas/
    │   ├── user.py                # User & Token schemas
    │   └── …                      
    ├── crud/
    │   ├── user.py                # User CRUD + auth logic
    │   └── …                      
    ├── routes/
    │   ├── auth.py                # Register/Login routes
    │   ├── order.py               # Orders router (now protected)
    │   └── …                      
    └── main.py                    # include auth router, update order router
```

---

### 1. Create `users` Table

```sql
USE fastapi_ecom;

CREATE TABLE IF NOT EXISTS users (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  role          ENUM('admin','customer') NOT NULL DEFAULT 'customer',
  created       DATETIME DEFAULT NOW()
);
```

> **Teaching Tip:** Explain why we store only hashed passwords, never plaintext.

---

### 2. Define Schemas: `app/schemas/user.py`

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    role: str
    created: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None
```

---

### 3. JWT Helpers: `app/auth/jwt.py`

```python
# app/auth/jwt.py
import os
from datetime import datetime, timedelta
import jwt

# Load from .env
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM  = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError as e:
        raise
```

---

### 4. Auth Dependencies: `app/auth/deps.py`

```python
# app/auth/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from app.auth.jwt import verify_access_token
from app.schemas.user import TokenData
from app.crud.user import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        user_id: int = payload.get("user_id")
        role:    str = payload.get("role")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        token_data = TokenData(user_id=user_id, role=role)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )
    user = get_user_by_id(token_data.user_id)
    return user

def get_current_active_user(current_user=Depends(get_current_user)):
    # Here you could check `current_user.is_active` if you track that
    return current_user

def get_current_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
```

---

### 5. User CRUD & Auth Logic: `app/crud/user.py`

```python
# app/crud/user.py
import bcrypt
from fastapi import HTTPException, status
from app.db.connection import get_db_connection
from app.schemas.user import UserCreate, User
from app.auth.jwt import create_access_token

def get_user_by_email(email: str) -> User | None:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email=%s;", (email,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return User(**row) if row else None

def get_user_by_id(user_id: int) -> User:
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s;", (user_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**row)

def create_user(user_in: UserCreate) -> User:
    if get_user_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = bcrypt.hashpw(user_in.password.encode(), bcrypt.gensalt()).decode()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, hashed_password, role) VALUES (%s,%s,%s)",
        (user_in.email, hashed, "customer")
    )
    conn.commit()
    user_id = cur.lastrowid
    cur.close(); conn.close()
    return get_user_by_id(user_id)

def authenticate_user(email: str, password: str) -> User:
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    return user

def create_user_token(user: User) -> str:
    token_data = {"user_id": user.id, "role": user.role}
    return create_access_token(token_data)
```

---

### 6. Auth Routes: `app/routes/auth.py`

```python
# app/routes/auth.py
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, User, Token
from app.crud.user import create_user, authenticate_user, create_user_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def register(user_in: UserCreate):
    return create_user(user_in)

@router.post(
    "/login",
    response_model=Token
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
```

---

### 7. Protecting Endpoints

1. **Include the auth router** in `app/main.py`:

   ```python
   # app/main.py
   from app.routes.auth    import router as auth_router
   from app.auth.deps     import get_current_active_user
   from app.routes.order   import router as order_router
   # …
   app.include_router(auth_router)
   # Protect orders
   app.include_router(order_router, dependencies=[Depends(get_current_active_user)])
   ```
2. **Alternatively**, add `Depends(get_current_active_user)` to specific routes in `app/routes/order.py`.

> **Teaching Tip:** Demonstrate both global (router-level) and route-level protection.

---

### 8. Live Coding & Testing

1. **Register a new user**

   ```
   POST /auth/register
   {
     "email":"alice@example.com",
     "password":"supersecret"
   }
   ```

   **Response 201**

   ```json
   {
     "id": 1,
     "email": "alice@example.com",
     "role": "customer",
     "created": "2025-07-21T17:00:00"
   }
   ```

2. **Login to get token**

   ```
   POST /auth/login
   Content-Type: application/x-www-form-urlencoded

   username=alice@example.com&password=supersecret
   ```

   **Response 200**

   ```json
   {
     "access_token": "<JWT_TOKEN>",
     "token_type": "bearer"
   }
   ```

3. **Access protected `/orders`** without token

   ```
   GET /orders
   ```

   **Response 401**

   ```json
   { "detail":"Not authenticated" }
   ```

4. **With token**

   ```
   GET /orders
   Authorization: Bearer <JWT_TOKEN>
   ```

   **Response 200**

---

### 9. Mini Assignment

1. **Admin-only route:** Add `DELETE /users/{user_id}` protected by `get_current_admin`.
2. **Password change:** Create `PATCH /auth/change-password` that requires old & new password.
3. **Token expiry:** Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env` to 60, regenerate tokens, and show expiry behavior.

---

### 10. Best Practices

* Store `SECRET_KEY` and token settings securely (never commit to VCS).
* Use HTTPS in production to protect tokens in transit.
* Implement refresh tokens for long-lived sessions.

---

✅ **Module 9 complete.**
*When you’re ready, say “Continue to next module.”*

---

## Module 10: Deployment Tips

*Objective:*
Prepare your E-Com API for production: manage secrets, enable CORS, connect to a hosted MySQL instance, and containerize or deploy to cloud platforms.

---

### 1. Prepare Your `.env` for Production

1. **Create a production `.env.prod`** (do **not** commit to VCS):

   ```env
   # Database
   DB_HOST=prod-mysql.example.com
   DB_PORT=3306
   DB_USER=prod_user
   DB_PASSWORD=super-secret-password
   DB_NAME=fastapi_ecom_prod

   # JWT settings
   JWT_SECRET_KEY=replace_with_a_strong_random_value
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60

   # App settings
   APP_HOST=0.0.0.0
   APP_PORT=8000

   # CORS
   CORS_ORIGINS=https://your-frontend.com,https://admin.your-frontend.com
   ```
2. **Load in code** (you’ve already got `python-dotenv`):

   ```python
   from dotenv import load_dotenv
   import os
   load_dotenv(".env.prod")

   # Later...
   origins = os.getenv("CORS_ORIGINS", "").split(",")
   ```

> **Teaching Tip:** Emphasize never shipping secrets in source; use a secrets manager (e.g., AWS Secrets Manager) for production.

---

### 2. Set Up CORS

In **`app/main.py`**, register the middleware:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="E-Com API")

# 1. Load allowed origins
origins = os.getenv("CORS_ORIGINS", "").split(",")

# 2. Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"],
    allow_headers=["*"],
)
```

> **Teaching Tip:** In development you can use `allow_origins=["*"]`, but lock it down in production to your actual frontends.

---

### 3. Use MySQL in Production

1. **Managed MySQL** on platforms like Render, AWS RDS, or Azure Database for MySQL.
2. **Connection string** looks the same—just point `DB_HOST` and credentials to the cloud instance.
3. **TLS/SSL**: For RDS, enable SSL by passing certificate options to `mysql-connector-python`:

   ```python
   conn = mysql.connector.connect(
       host=os.getenv("DB_HOST"),
       port=os.getenv("DB_PORT"),
       user=os.getenv("DB_USER"),
       password=os.getenv("DB_PASSWORD"),
       database=os.getenv("DB_NAME"),
       ssl_ca="/path/to/rds-combined-ca-bundle.pem"
   )
   ```

> **Teaching Tip:** Show students how to download the RDS CA bundle and configure the connector to enforce SSL.

---

### 4. Deployment Options

#### A. Docker

1. **`Dockerfile`**:

   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .
   CMD ["uvicorn", "app.main:app", 
        "--host", "0.0.0.0", "--port", "8000"]
   ```
2. **`docker-compose.yml`** (optional local dev):

   ```yaml
   version: "3.8"
   services:
     db:
       image: mysql:8
       environment:
         MYSQL_DATABASE: fastapi_ecom
         MYSQL_USER: dev
         MYSQL_PASSWORD: devpass
         MYSQL_ROOT_PASSWORD: rootpass
       ports:
         - "3306:3306"
     web:
       build: .
       env_file: .env
       ports:
         - "8000:8000"
       depends_on:
         - db
   ```
3. **Build & Run**:

   ```bash
   docker-compose up --build
   ```

#### B. Railway / Render

1. **Push** your Docker image to GitHub or DockerHub.
2. **Link** your repo/image in Railway/Render’s dashboard.
3. **Set environment variables** via their UI (DB\_HOST, etc.).
4. **Deploy**—the platform will build and run the container.

#### C. Deta (Serverless)

1. Install Deta CLI: `pip install deta` and `deta login`.
2. Create `main.py` entrypoint with a `lambda_handler` wrapper (Deta Micro).
3. Deploy: `deta deploy`.

> **Teaching Tip:** Compare “always-on” (Docker/Railway) vs. serverless (Deta) pros & cons.

---

### 5. Live Coding & Testing

1. **Local Docker**:

   * `docker-compose up --build`
   * Verify `http://localhost:8000/ping` → `{ "message":"pong" }`
2. **Render**:

   * After linking repo, check the service’s health endpoint (`/ping`) on the provided URL.
3. **Deta**:

   * `deta deploy` prints a URL; test `/ping` there.

---

### 6. Teaching Tips & Common Pitfalls

* **Database readiness**: Containers may spin up faster than MySQL—use a retry loop in your startup code.
* **Environment mismatch**: Ensure you’re loading `.env.prod` in production, not `.env` from local.
* **Exposed ports**: Don’t expose MySQL port publicly—limit to internal network.
* **CORS headaches**: If frontends still get CORS errors, inspect response headers in the browser DevTools.

---

### 7. Mini Assignment

1. **Containerize** your entire app with the above `Dockerfile` & `docker-compose.yml`.
2. **Deploy** to a free Railway project: link your GitHub, set env vars, and run.
3. **Verify** all endpoints (`/ping`, `/products`, `/orders`) in Postman against the live URL.

---

### 8. Best Practices

* **CI/CD**: Automate build & deployment with GitHub Actions or GitLab CI.
* **Secrets Management**: Use a vault (e.g., Vault, AWS Secrets Manager) instead of flat `.env` in production.
* **Health Checks & Metrics**: Add `/health` endpoint and integrate with Prometheus/Grafana for monitoring.
* **Scaling**: Use multiple replicas and a load balancer; consider stateless design (sessions in DB).

---



```

Below is a **module-wise Streamlit frontend** for your FastAPI E-Commerce API. It uses Streamlit’s multipage support — each page consumes the corresponding API endpoints. You’ll get:

* **`utils.py`**: shared functions (auth, requests, config)
* **`requirements.txt`**
* **`.env`** for your API root URL
* **Pages** under a `pages/` folder:

  1. **Auth** (login & signup)
  2. **Products** (list, create, edit, delete)
  3. **Categories** (list & create)
  4. **Cart** (view, add, remove)
  5. **Orders** (place order & history)

---

## Project Structure

```
streamlit_app/
├── .env
├── requirements.txt
├── utils.py
└── pages/
    ├── 1_Auth.py
    ├── 2_Products.py
    ├── 3_Categories.py
    ├── 4_Cart.py
    └── 5_Orders.py
```

---

### `requirements.txt`

```text
streamlit
requests
python-dotenv
```

---

### `.env`

```env
API_URL=http://localhost:8000
```

---

## `utils.py`

```python
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

def login(email: str, password: str) -> bool:
    resp = requests.post(f"{API_URL}/auth/login",
                         data={"username": email, "password": password})
    if resp.status_code == 200:
        st.session_state.token = resp.json()["access_token"]
        return True
    st.error("❌ Login failed: " + resp.json().get("detail", ""))
    return False

def signup(email: str, password: str) -> bool:
    resp = requests.post(f"{API_URL}/auth/register",
                         json={"email": email, "password": password})
    if resp.status_code == 201:
        st.success("✅ Registration successful! Please log in.")
        return True
    st.error("❌ Registration failed: " + resp.json().get("detail", ""))
    return False

def get_headers() -> dict:
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}
```

---

## pages/1\_Auth.py

```python
import streamlit as st
from utils import login, signup

st.title("🔐 E-Com App: Authentication")

mode = st.sidebar.radio("Mode", ["Login", "Sign Up"])
email = st.text_input("Email", key="auth_email")
password = st.text_input("Password", type="password", key="auth_password")

if mode == "Login":
    if st.button("Login"):
        if login(email, password):
            st.success("Logged in successfully!")
            st.experimental_rerun()
else:
    if st.button("Register"):
        signup(email, password)
```

---

## pages/2\_Products.py

```python
import streamlit as st
import requests
from utils import API_URL, get_headers

st.title("📦 Products")

if "token" not in st.session_state:
    st.warning("Please log in first in the Auth page.")
    st.stop()

headers = get_headers()

# 1) List products
st.subheader("All Products")
resp = requests.get(f"{API_URL}/products", headers=headers)
if resp.status_code == 200:
    products = resp.json().get("data", resp.json())
    for p in products:
        st.markdown(f"**{p['name']}** (ID {p['id']}) — ${p['price']:.2f}")
        st.write(p["description"] or "_No description_")
        col1, col2 = st.columns(2)
        if col1.button("Edit", key=f"edit_{p['id']}"):
            st.session_state.edit_id = p["id"]
            st.session_state.name = p["name"]
            st.session_state.desc = p["description"]
            st.session_state.price = p["price"]
            st.experimental_rerun()
        if col2.button("Delete", key=f"del_{p['id']}"):
            requests.delete(f"{API_URL}/products/{p['id']}", headers=headers)
            st.success("Deleted!")
            st.experimental_rerun()
else:
    st.error("Failed to fetch products")

# 2) Add / Update form
st.subheader("➕ Add / Update Product")
name = st.text_input("Name", key="name")
desc = st.text_area("Description", key="desc")
price = st.number_input("Price", min_value=0.0, format="%.2f", key="price")

if "edit_id" in st.session_state:
    if st.button("Update Product"):
        pid = st.session_state.pop("edit_id")
        data = {"name": name, "description": desc, "price": price}
        requests.put(f"{API_URL}/products/{pid}", json=data, headers=headers)
        st.success("Updated!")
        st.experimental_rerun()
else:
    if st.button("Add Product"):
        data = {"name": name, "description": desc, "price": price}
        requests.post(f"{API_URL}/products", json=data, headers=headers)
        st.success("Created!")
        st.experimental_rerun()
```

---

## pages/3\_Categories.py

```python
import streamlit as st
import requests
from utils import API_URL, get_headers

st.title("🏷️ Categories")

if "token" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

headers = get_headers()

# List
st.subheader("All Categories")
resp = requests.get(f"{API_URL}/categories", headers=headers)
if resp.status_code == 200:
    cats = resp.json().get("data", resp.json())
    for c in cats:
        st.write(f"- {c['id']}: {c['name']}")
else:
    st.error("Failed to fetch categories")

# Add
st.subheader("➕ Add Category")
name = st.text_input("New category name", key="cat_name")
if st.button("Add Category"):
    r = requests.post(f"{API_URL}/categories", json={"name": name}, headers=headers)
    if r.status_code == 201:
        st.success("Category added!")
        st.experimental_rerun()
    else:
        st.error("Error: " + r.text)
```

---

## pages/4\_Cart.py

```python
import streamlit as st
import requests
from utils import API_URL, get_headers

st.title("🛒 Your Cart")

if "token" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

headers = get_headers()

# View
st.subheader("Current Cart")
r = requests.get(f"{API_URL}/cart", headers=headers)
if r.status_code == 200:
    cart = r.json().get("data", r.json())
    if cart["items"]:
        for item in cart["items"]:
            st.write(f"• Item {item['id']}: Prod {item['product_id']} × {item['quantity']}")
            if st.button("Remove", key=f"rm_{item['id']}"):
                requests.delete(f"{API_URL}/cart/items/{item['id']}", headers=headers)
                st.experimental_rerun()
    else:
        st.info("Cart is empty")
else:
    st.error("Failed to fetch cart")

# Add
st.subheader("➕ Add to Cart")
pid = st.number_input("Product ID", step=1, key="cart_pid")
qty = st.number_input("Quantity", step=1, min_value=1, key="cart_qty")
if st.button("Add to Cart"):
    resp = requests.post(f"{API_URL}/cart/items",
                         json={"product_id": pid, "quantity": qty},
                         headers=headers)
    if resp.status_code == 201:
        st.success("Added!")
        st.experimental_rerun()
    else:
        st.error("Error: " + resp.text)
```

---

## pages/5\_Orders.py

```python
import streamlit as st
import requests
from utils import API_URL, get_headers

st.title("🧾 Orders")

if "token" not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

headers = get_headers()

# Place Order
if st.button("🛍️ Place Order (from Cart)"):
    r = requests.post(f"{API_URL}/orders", headers=headers, json={})
    if r.status_code == 201:
        st.success("Order placed!")
    else:
        st.error("Error: " + r.text)

# History
st.subheader("Order History")
r = requests.get(f"{API_URL}/orders", headers=headers)
if r.status_code == 200:
    orders = r.json().get("data", r.json())
    for o in orders:
        st.markdown(f"**Order {o['id']}** — Total: ${o['total_amount']:.2f} on {o['created']}")
        with st.expander("Show Items"):
            for itm in o["items"]:
                st.write(f"- Prod {itm['product_id']} ×{itm['quantity']} @ ${itm['price_at_purchase']:.2f}")
else:
    st.error("Failed to fetch orders")
```

---

### 🎓 Teaching Tips & Best Practices

* **Session State:** Store JWT in `st.session_state.token` for persistence across pages.
* **Error Handling:** Always check `resp.status_code` and show `st.error(...)`.
* **Layout:** Use `st.columns` and `st.expander` for a clean look.
* **Styling:** You can customize colors in `.streamlit/config.toml`.
* **Pagination/Search (Bonus):** Add inputs on the Products page and pass `?page=&search=&sort=` to the GET `/products` URL.

---

🚀 **Run the app**

```bash
pip install -r requirements.txt
streamlit run pages/1_Auth.py
```

Then use the sidebar to navigate between pages. Enjoy building an **amazing** Streamlit frontend for your FastAPI E-Commerce API!

```
