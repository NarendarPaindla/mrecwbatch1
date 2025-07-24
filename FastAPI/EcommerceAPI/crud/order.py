# app/crud/order.py
from db.connection import get_db_connection
from schemas.order import OrderCreate, Order
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