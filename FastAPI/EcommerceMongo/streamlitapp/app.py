import streamlit as st
import requests
import os
from dotenv import load_dotenv

# ─── Setup ─────────────────────────────────────────────────────────────────────
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="E-Com Demo", layout="wide")

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None  # will hold {"id":..., "email":...}

headers = {"Content-Type": "application/json"}


# ─── Authentication ─────────────────────────────────────────────────────────────
def register():
    st.subheader("📋 Register")
    email = st.text_input("Email", key="reg_email")
    pwd   = st.text_input("Password", type="password", key="reg_pwd")
    if st.button("Sign Up"):
        resp = requests.post(f"{API_URL}/auth/register",
                             json={"email": email, "password": pwd})
        if resp.status_code == 201:
            st.success("Registered! Please log in.")
        else:
            st.error(resp.json().get("detail", resp.text))


def login():
    st.subheader("🔑 Login")
    email = st.text_input("Email", key="log_email")
    pwd   = st.text_input("Password", type="password", key="log_pwd")
    if st.button("Log In"):
        resp = requests.post(f"{API_URL}/auth/login",
                             json={"email": email, "password": pwd})
        if resp.status_code == 200:
            st.session_state.user = resp.json()
            st.experimental_rerun()
        else:
            st.error(resp.json().get("detail", resp.text))


# ─── PRODUCTS ──────────────────────────────────────────────────────────────────
def products_page():
    st.header("📦 Products")
    # List
    with st.expander("All Products"):
        resp = requests.get(f"{API_URL}/products")
        if resp.ok:
            prods = resp.json().get("data", resp.json())
            for p in prods:
                cols = st.columns([4,1,1])
                cols[0].markdown(f"**{p['name']}** — ${p['price']:.2f}\n\n{p.get('description','')}")
                if cols[1].button("Edit", key=f"edit_prod_{p['id']}"):
                    st.session_state.edit_prod = p
                    st.experimental_rerun()
                if cols[2].button("Delete", key=f"del_prod_{p['id']}"):
                    requests.delete(f"{API_URL}/products/{p['id']}")
                    st.success("Deleted")
                    st.experimental_rerun()
        else:
            st.error("Could not fetch products")

    # Create / Update
    st.subheader("➕ Add / Update Product")
    p = st.session_state.get("edit_prod", {})
    name = st.text_input("Name", value=p.get("name",""), key="prod_name")
    desc = st.text_area("Description", value=p.get("description",""), key="prod_desc")
    price= st.number_input("Price", value=p.get("price",0.0), format="%.2f", key="prod_price")
    stock= st.number_input("Stock", min_value=0, value=p.get("stock",0), key="prod_stock")

    if "edit_prod" in st.session_state:
        if st.button("Update Product"):
            pid = p["id"]
            payload = {"name":name,"description":desc,"price":price,"stock":stock}
            requests.put(f"{API_URL}/products/{pid}", json=payload)
            st.success("Updated")
            del st.session_state.edit_prod
            st.experimental_rerun()
    else:
        if st.button("Add Product"):
            payload = {"name":name,"description":desc,"price":price,"stock":stock}
            requests.post(f"{API_URL}/products", json=payload)
            st.success("Created")
            st.experimental_rerun()


# ─── CATEGORIES ─────────────────────────────────────────────────────────────────
def categories_page():
    st.header("🏷️ Categories")
    # List
    with st.expander("All Categories"):
        resp = requests.get(f"{API_URL}/categories")
        if resp.ok:
            cats = resp.json().get("data", resp.json())
            for c in cats:
                cols = st.columns([4,1,1])
                cols[0].write(f"{c['name']}")
                if cols[1].button("Edit", key=f"edit_cat_{c['id']}"):
                    st.session_state.edit_cat = c
                    st.experimental_rerun()
                if cols[2].button("Delete", key=f"del_cat_{c['id']}"):
                    requests.delete(f"{API_URL}/categories/{c['id']}")
                    st.success("Deleted")
                    st.experimental_rerun()
        else:
            st.error("Could not fetch categories")

    # Create / Update
    st.subheader("➕ Add / Update Category")
    c = st.session_state.get("edit_cat", {})
    name = st.text_input("Name", value=c.get("name",""), key="cat_name")
    if "edit_cat" in st.session_state:
        if st.button("Update Category"):
            cid = c["id"]
            requests.put(f"{API_URL}/categories/{cid}", json={"name":name})
            st.success("Updated")
            del st.session_state.edit_cat
            st.experimental_rerun()
    else:
        if st.button("Add Category"):
            requests.post(f"{API_URL}/categories", json={"name":name})
            st.success("Created")
            st.experimental_rerun()


# ─── CART ───────────────────────────────────────────────────────────────────────
def cart_page():
    st.header("🛒 Your Cart")
    uid = st.session_state.user["email"]

    # View
    with st.expander("Current Cart"):
        resp = requests.get(f"{API_URL}/carts/{uid}")
        if resp.ok:
            cart = resp.json().get("data", resp.json())
            if cart["items"]:
                for it in cart["items"]:
                    cols = st.columns([4,1])
                    cols[0].write(f"Product {it['product_id']} × {it['quantity']}")
                    if cols[1].button("Remove", key=f"rm_{it['id']}"):
                        requests.delete(f"{API_URL}/carts/{uid}/items/{it['id']}")
                        st.experimental_rerun()
            else:
                st.info("Your cart is empty")
        else:
            st.error("Could not fetch cart")

    # Add
    st.subheader("➕ Add to Cart")
    pid = st.text_input("Product ID", key="cart_pid")
    qty = st.number_input("Quantity", min_value=1, value=1, key="cart_qty")
    if st.button("Add to Cart"):
        resp = requests.post(f"{API_URL}/carts/{uid}/items",
                             json={"product_id": pid, "quantity": qty})
        if resp.status_code == 201:
            st.success("Added!")
            st.experimental_rerun()
        else:
            st.error(resp.text)


# ─── ORDERS ─────────────────────────────────────────────────────────────────────
def orders_page():
    st.header("🧾 Orders")
    uid = st.session_state.user["email"]

    # Place Order
    if st.button("🛍️ Place Order from Cart"):
        # fetch cart
        cart = requests.get(f"{API_URL}/carts/{uid}").json().get("items",[])
        items_payload = [{"product_id":it["product_id"], "quantity":it["quantity"]} for it in cart]
        resp = requests.post(f"{API_URL}/orders", json={"user_id":uid, "items":items_payload})
        if resp.status_code == 201:
            st.success("Order placed!")
        else:
            st.error(resp.text)

    # History
    st.subheader("Your Order History")
    resp = requests.get(f"{API_URL}/orders/{uid}")
    if resp.ok:
        orders = resp.json().get("data", resp.json())
        for o in orders:
            with st.expander(f"Order {o['id']} — ${o['total_amount']:.2f}"):
                st.write(f"Created: {o['created']}")
                for it in o["items"]:
                    st.write(f"- Product {it['product_id']} ×{it['quantity']} @ ${it['price_at_purchase']:.2f}")
    else:
        st.error("Could not fetch orders")


# ─── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    st.sidebar.title("E-Com Demo")
    if st.session_state.user is None:
        page = st.sidebar.radio("Go to", ["Login", "Register"])
        if page == "Login":
            login()
        else:
            register()
        return

    # After login
    st.sidebar.write(f"👤 {st.session_state.user['email']}")
    page = st.sidebar.selectbox("Navigate", [
        "Products", "Categories", "Cart", "Orders", "Logout"
    ])

    if page == "Products":
        products_page()
    elif page == "Categories":
        categories_page()
    elif page == "Cart":
        cart_page()
    elif page == "Orders":
        orders_page()
    else:
        if st.sidebar.button("Log Out"):
            st.session_state.user = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()
