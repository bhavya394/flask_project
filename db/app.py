
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder='templates')

# Database connection config
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Bhavya@08',
    'database': 'arlington'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    msg = ""
    conn = cursor = None

    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Grabbing form data
            vendor_id = request.form['vendor_id']
            vendor_name = request.form['vendor_name']
            street = request.form['street']
            city = request.form['city']
            state = request.form['state']
            zipcode = request.form['zipcode']

            item_id = request.form['item_id']
            item_name = request.form['item_name']
            price = request.form['price']
            category = request.form['category']

            store_id = request.form['store_id']
            stock = request.form['stock']

            # Insert vendor
            cursor.execute("""
                insert into VENDOR (vId, Vname, Street, City, StateAb, Zipcode)
                values (%s, %s, %s, %s, %s, %s)
            """, (vendor_id, vendor_name, street, city, state, zipcode))

            # Insert item
            cursor.execute("""
                insert into ITEM (iId, Iname, Sprice, Category)
                values (%s, %s, %s, %s)
            """, (item_id, item_name, price, category))

            # Vendor and store link
            cursor.execute("""
                insert into VENDOR_STORE (vId, sId)
                values (%s, %s)
            """, (vendor_id, store_id))

            # Inventory insert
            cursor.execute("""
                insert into STORE_ITEM (sId, iId, Scount)
                values (%s, %s, %s)
            """, (store_id, item_id, stock))

            conn.commit()
            msg = "Product added successfully."
        except Exception as e:
            if conn: conn.rollback()
            msg = f"Error: {str(e)}"
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    return render_template('add_product.html', message=msg)

@app.route('/update_price', methods=['GET', 'POST'])
def update_price():
    msg = ""
    conn = cursor = None
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                update ITEM set Sprice = 10.99 where iId = 101
            """)
            conn.commit()
            msg = "Price updated to $10.99."
        except Exception as e:
            if conn: conn.rollback()
            msg = f"Error: {str(e)}"
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    return render_template('update_price.html', message=msg)

@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    msg = ""
    conn = cursor = None
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("delete from STORE_ITEM where iId = 101")
            cursor.execute("delete from VENDOR_STORE where vId = 201 and sId = 1")
            cursor.execute("delete from ITEM where iId = 101")
            cursor.execute("""
                delete from VENDOR
                where vId = 201 and vId not in (select vId from VENDOR_STORE)
            """)

            conn.commit()
            msg = "Almond Nuts and its vendor removed."
        except Exception as e:
            if conn: conn.rollback()
            msg = f"Error: {str(e)}"
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    return render_template('delete_product.html', message=msg)

@app.route('/view_products')
def view_products():
    items = []
    conn = cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            select i.Iname, i.Sprice, s.Scount
            from ITEM i
            join STORE_ITEM s on i.iId = s.iId
            where s.sId = 1;
        """)
        items = cursor.fetchall()
    except Exception as e:
        print("Error:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return render_template('view_products.html', products=items)


@app.route('/report')
def analytics():
    results = {}
    conn = cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("select Iname, TotalRevenue from ItemSalesSummary order by TotalRevenue desc limit 3")
        results['q1'] = cursor.fetchall()

        cursor.execute("select Iname, TotalQuantitySold from ItemSalesSummary where TotalQuantitySold > 50")
        results['q2'] = cursor.fetchall()

        cursor.execute("select Cname, LoyaltyScore from TopLoyalCustomers order by LoyaltyScore desc limit 1")
        results['q3'] = cursor.fetchone()

        cursor.execute("select Cname, LoyaltyScore from TopLoyalCustomers where LoyaltyScore between 4 and 5")
        results['q4'] = cursor.fetchall()

        cursor.execute("select sum(TotalRevenue) from ItemSalesSummary")
        results['q5'] = cursor.fetchone()

    except Exception as e:
        print("Analytics error:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return render_template('report.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
