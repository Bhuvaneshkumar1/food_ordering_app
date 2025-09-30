import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from typing import List, Dict, Optional

USERS_FILE = 'users.csv'
MENU_FILE = 'menu.csv'
ORDERS_FILE = 'orders.csv'
ORDER_ITEMS_FILE = 'order_items.csv'

logged_in_user: Optional[Dict] = None

# ---------------- CSV Helpers ----------------
def read_csv(file: str) -> List[Dict]:
    rows = []
    if not os.path.exists(file):
        return rows
    try:
        with open(file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"❌ Error reading {file}: {e}")
    return rows

def append_csv(file: str, data: Dict, fieldnames: List[str]):
    try:
        file_exists = os.path.exists(file)
        with open(file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        print(f"❌ Error writing to {file}: {e}")

def get_next_id(file: str) -> int:
    rows = read_csv(file)
    if not rows:
        return 1
    try:
        return max(int(r.get('id','0')) for r in rows if str(r.get('id','0')).isdigit()) + 1
    except Exception:
        return 1

# ---------------- Admin Auto Setup ----------------
def ensure_admin_exists():
    users = read_csv(USERS_FILE)
    if not any(u.get('role','') == 'ADMIN' for u in users):
        admin = {'id':'1','name':'admin','email':'admin@food.com','password':'admin123','role':'ADMIN'}
        append_csv(USERS_FILE, admin, ['id','name','email','password','role'])
        print("Admin account created: admin@food.com / admin123")

# ---------------- Authentication ----------------
def register_user():
    try:
        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip()
        password = input("Enter Password: ").strip()
        user_id = get_next_id(USERS_FILE)
        user = {'id':str(user_id),'name':name,'email':email,'password':password,'role':'USER'}
        append_csv(USERS_FILE, user, ['id','name','email','password','role'])
        print("✅ User registered successfully!")
    except Exception as e:
        print("❌ Registration error:", e)

def login_user():
    global logged_in_user
    try:
        email = input("Enter Email: ").strip()
        password = input("Enter Password: ").strip()
        users = read_csv(USERS_FILE)
        logged_in_user = next((u for u in users if u.get('email')==email and u.get('password')==password), None)
        if logged_in_user:
            print(f"✅ Login successful! Logged in as {logged_in_user.get('role','USER')}")
        else:
            print("❌ Invalid credentials!")
    except Exception as e:
        print("❌ Login error:", e)

# ---------------- Menu ----------------
def view_menu():
    try:
        menu = read_csv(MENU_FILE)
        if not menu:
            print("Menu is empty!")
            return
        menu.sort(key=lambda x: x.get('item_name','').lower())
        print("\n┌───────┬─────────────────────┬───────────┐")
        print("│ ID    │ Item Name           │ Price (Rs)│")
        print("├───────┼─────────────────────┼───────────┤")
        for m in menu:
            print(f"│ {m.get('id',''):<5} │ {m.get('item_name',''):<19} │ {m.get('price',''):<9} │")
        print("└───────┴─────────────────────┴───────────┘")
    except Exception as e:
        print("❌ Error displaying menu:", e)

def add_menu_item():
    try:
        item_name = input("Enter Item Name: ").strip()
        price = input("Enter Price: ").strip()
        item_id = get_next_id(MENU_FILE)
        append_csv(MENU_FILE, {'id':str(item_id),'item_name':item_name,'price':price}, ['id','item_name','price'])
        print("✅ Menu item added!")
    except Exception as e:
        print("❌ Error adding menu item:", e)

def remove_menu_item():
    try:
        view_menu()
        item_id = input("Enter Menu ID to remove: ").strip()
        menu = read_csv(MENU_FILE)
        menu = [m for m in menu if m.get('id','') != item_id]
        with open(MENU_FILE,'w',newline='',encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id','item_name','price'])
            writer.writeheader()
            writer.writerows(menu)
        print("✅ Menu item removed!")
    except Exception as e:
        print("❌ Error removing menu item:", e)

# ---------------- Orders ----------------
def generate_pdf(order_id: str, cart: List[Dict], total: float):
    try:
        filename = f"Order_{order_id}_Invoice.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(300, 800, "🧾 Food Delivery Invoice")
        c.setFont("Helvetica", 12)
        c.drawString(50, 770, f"Order ID: {order_id}")
        c.drawString(50, 750, f"Customer: {logged_in_user.get('name','')}")
        c.drawString(50, 730, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, 700, "Items:")

        y = 680
        for item in cart:
            line = f"{item['item_name']} x {item['qty']} = Rs.{item['price']*item['qty']:.2f}"
            c.drawString(60, y, line)
            y -= 20

        c.drawString(50, y-10, f"TOTAL: Rs.{total:.2f}")
        c.save()
        print(f"📄 PDF generated: {filename}")
    except Exception as e:
        print("❌ PDF generation error:", e)

def place_order():
    try:
        cart: List[Dict] = []
        while True:
            view_menu()
            item_id = input("Enter Item ID (0 to finish): ").strip()
            if item_id == '0':
                break
            quantity = input("Enter Quantity: ").strip()
            menu = read_csv(MENU_FILE)
            item = next((i for i in menu if i.get('id','') == item_id), None)
            if not item:
                print("❌ Invalid Item ID!")
                continue
            cart.append({
                'item_id': item_id,
                'item_name': item.get('item_name',''),
                'price': float(item.get('price','0')),
                'qty': int(quantity)
            })
            print(f"✅ Added {item.get('item_name','')} x {quantity} to cart!")

        if not cart:
            print("Cart is empty. Order cancelled.")
            return

        total = sum(c['price']*c['qty'] for c in cart)

        # Save order
        order_id = str(get_next_id(ORDERS_FILE))
        append_csv(ORDERS_FILE, {'id':order_id,'user_id':logged_in_user['id'],'date':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, ['id','user_id','date'])
        for c in cart:
            append_csv(ORDER_ITEMS_FILE, {'order_id':order_id,'item_id':c['item_id'],'qty':str(c['qty'])}, ['order_id','item_id','qty'])
        print("\n🛒 Order Summary:")
        for c in cart:
            print(f"{c['item_name']} x {c['qty']} = Rs.{c['price']*c['qty']:.2f}")
        print(f"✅ Order placed successfully! Order ID: {order_id}")

        # Generate PDF
        generate_pdf(order_id, cart, total)
    except Exception as e:
        print("❌ Error placing order:", e)

def view_my_orders():
    try:
        orders = read_csv(ORDERS_FILE)
        order_items = read_csv(ORDER_ITEMS_FILE)
        menu = read_csv(MENU_FILE)
        print("\n===== My Orders =====")
        for o in orders:
            if o.get('user_id','') != logged_in_user.get('id',''):
                continue
            print(f"Order ID: {o.get('id','')} Date: {o.get('date','')}")
            items = [oi for oi in order_items if oi.get('order_id','') == o.get('id','')]
            for i in items:
                m = next((m for m in menu if m.get('id','')==i.get('item_id','')), None)
                if m:
                    subtotal = float(m.get('price','0'))*int(i.get('qty','0'))
                    print(f" - {m.get('item_name','')} x {i.get('qty','0')} = Rs.{subtotal:.2f}")
            print("---------------------------")
    except Exception as e:
        print("❌ Error viewing orders:", e)

# ---------------- Menus ----------------
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View Menu\n2. Add Menu Item\n3. Remove Menu Item\n4. Logout")
        choice = input("Choice: ").strip()
        if choice=='1': view_menu()
        elif choice=='2': add_menu_item()
        elif choice=='3': remove_menu_item()
        elif choice=='4':
            print("👋 Logged out!")
            return
        else:
            print("❌ Invalid choice!")

def user_menu():
    while True:
        print("\n--- User Menu ---")
        print("1. View Menu\n2. Place Order\n3. View My Orders\n4. Logout")
        choice = input("Choice: ").strip()
        if choice=='1': view_menu()
        elif choice=='2': place_order()
        elif choice=='3': view_my_orders()
        elif choice=='4':
            print("👋 Logged out!")
            return
        else:
            print("❌ Invalid choice!")

# ---------------- Main ----------------
def main():
    ensure_admin_exists()
    while True:
        print("\n=== Welcome to CLI Food Delivery ===")
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Choice: ").strip()
        if choice=='1': register_user()
        elif choice=='2':
            login_user()
            if logged_in_user:
                if logged_in_user.get('role','')=='ADMIN': admin_menu()
                else: user_menu()
        elif choice=='3':
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
