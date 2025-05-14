
# Arlington Organic Market Web Interface (Phase 3)

This is a Flask web application to manage inventory, vendors, pricing, and sales analytics for the Arlington Organic Market.

---

## 1. Project Overview

- Built using **Flask + MySQL**
- Covers operations like: add product, update price, delete item, and view inventory
- Includes a dashboard to view view-based results

---

## 2. Setup Instructions

1. Clone or download the project
2. Start your MySQL/XAMPP server and create the `arlington` database


---

## 3. Folder Structure

```
├── app.py                  # Main Flask app
├── templates/              # All HTML templates
│   ├── home.html
│   ├── add_product.html
│   ├── update_price.html
│   ├── delete_product.html
│   ├── view_products.html
│   └── report.html
├
└── README.md
```

---

## 4. Key Features

### Q1: Add a New Product to Inventory
```sql

INSERT INTO VENDOR (vId, Vname, Street, City, StateAb, Zipcode)
VALUES (201, 'Organic Farms', '123 Greenway Blvd', 'Dallas', 'TX', '75001');


INSERT INTO ITEM (iId, Iname, Sprice, Category)
VALUES (101, 'Almond Nuts', 12.99, 'Nuts');


INSERT INTO VENDOR_STORE (vId, sId)
VALUES (201, 1);


INSERT INTO STORE_ITEM (sId, iId, Scount)
VALUES (1, 101, 50);
```

- Adds a vendor and new item
- Links the vendor to store 1
- Initializes stock count for the item


- Created the route `/add_product` using `GET` to show the form and `POST` to handle submission.
- Collected form data using `request.form`.
- Ran 4 SQL queries: vendor insert, item insert, vendor-store link, and inventory update.
- Used `conn.commit()` to save and `conn.rollback()` for errors.
- Displayed feedback on the same form using `render_template()`.

### Q2: View Products Available at Store 1
```sql
SELECT i.Iname, i.Sprice, s.Scount
FROM ITEM i
JOIN STORE_ITEM s ON i.iId = s.iId
WHERE s.sId = 1;
```

- Retrieves all products for store ID 1
- Shows product name, price, and stock count


- Created `/view_products` route using `GET` only.
- Executed a JOIN query to fetch item and inventory data.
- Rendered results in an HTML table using `view_products.html`.

### Q3: Update Price of Almond Nuts
```sql
UPDATE ITEM
SET Sprice = 10.99
WHERE iId = 101;
```

- Reduces the price of Almond Nuts from 12.99 to 10.99


- Created the route `/update_price` with `GET` and `POST` methods.
- On form submission, executed `UPDATE` SQL query.
- Displayed success message in `update_price.html`.

### Q4: Delete Almond Nuts and Related Data
```sql
DELETE FROM STORE_ITEM WHERE iId = 101;
DELETE FROM VENDOR_STORE WHERE vId = 201 AND sId = 1;
DELETE FROM ITEM WHERE iId = 101;
DELETE FROM VENDOR
WHERE vId = 201 AND vId NOT IN (SELECT vId FROM VENDOR_STORE);
```

- Removes item from inventory and item table
- Deletes vendor-item relation
- Deletes vendor only if not linked to other items


- Created `/delete_product` route with `GET` and `POST` methods.
- Handled deletion in correct order to avoid constraint errors.
- Showed confirmation message in `delete_product.html`.

### View-based
- **Views Created in DB:** `ItemSalesSummary`, `TopLoyalCustomers`
- **Queries performed in Flask:**

```sql
-- QV1: Top 3 items by revenue
SELECT Iname, TotalRevenue FROM ItemSalesSummary ORDER BY TotalRevenue DESC LIMIT 3;

-- QV2: Items sold > 50
SELECT Iname, TotalQuantitySold FROM ItemSalesSummary WHERE TotalQuantitySold > 50;

-- QV3: Top loyal customer
SELECT Cname, LoyaltyScore FROM TopLoyalCustomers ORDER BY LoyaltyScore DESC LIMIT 1;

-- QV4: Loyalty score between 4 and 5
SELECT Cname, LoyaltyScore FROM TopLoyalCustomers WHERE LoyaltyScore BETWEEN 4 AND 5;

-- QV5: Total revenue
SELECT SUM(TotalRevenue) AS TotalMarketRevenue FROM ItemSalesSummary;
```


#### 
- Created `/analytics` route to run multiple SELECT queries.
- Pulled data from the views and passed it into `report.html`.
- Displayed each result in its own section (tables or text).