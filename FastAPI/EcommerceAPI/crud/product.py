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