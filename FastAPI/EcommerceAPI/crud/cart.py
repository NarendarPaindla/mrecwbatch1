# app/crud/cart.py
from db.connection import get_db_connection
from schemas.cart import CartCreate, Cart, CartItemCreate, CartItem
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