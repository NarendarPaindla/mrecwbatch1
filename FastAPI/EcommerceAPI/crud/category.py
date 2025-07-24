# app/crud/category.py
from db.connection import get_db_connection
from schemas.category import Category, CategoryCreate
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