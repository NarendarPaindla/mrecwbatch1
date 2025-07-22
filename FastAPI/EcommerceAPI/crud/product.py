from fastapi import HTTPException
from schemas.product import ProductCreate,Product
from db.connection import get_db_connection

def create_product(payload: ProductCreate)-> Product:
    conn=get_db_connection()
    cursor=conn.cursor()
    sql="INSERT INTO products (name,description,price) VALUES (%s,%s,%s)"
    cursor.execute(sql,(payload.name,payload.description,payload.price))
    conn.commit()
    new_id=cursor.lastrowid
    cursor.close()
    conn.close()
    return Product(id=new_id,**payload.dict())

def list_products()->list[Product]:
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products;")
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return [Product(**r) for r in rows]

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