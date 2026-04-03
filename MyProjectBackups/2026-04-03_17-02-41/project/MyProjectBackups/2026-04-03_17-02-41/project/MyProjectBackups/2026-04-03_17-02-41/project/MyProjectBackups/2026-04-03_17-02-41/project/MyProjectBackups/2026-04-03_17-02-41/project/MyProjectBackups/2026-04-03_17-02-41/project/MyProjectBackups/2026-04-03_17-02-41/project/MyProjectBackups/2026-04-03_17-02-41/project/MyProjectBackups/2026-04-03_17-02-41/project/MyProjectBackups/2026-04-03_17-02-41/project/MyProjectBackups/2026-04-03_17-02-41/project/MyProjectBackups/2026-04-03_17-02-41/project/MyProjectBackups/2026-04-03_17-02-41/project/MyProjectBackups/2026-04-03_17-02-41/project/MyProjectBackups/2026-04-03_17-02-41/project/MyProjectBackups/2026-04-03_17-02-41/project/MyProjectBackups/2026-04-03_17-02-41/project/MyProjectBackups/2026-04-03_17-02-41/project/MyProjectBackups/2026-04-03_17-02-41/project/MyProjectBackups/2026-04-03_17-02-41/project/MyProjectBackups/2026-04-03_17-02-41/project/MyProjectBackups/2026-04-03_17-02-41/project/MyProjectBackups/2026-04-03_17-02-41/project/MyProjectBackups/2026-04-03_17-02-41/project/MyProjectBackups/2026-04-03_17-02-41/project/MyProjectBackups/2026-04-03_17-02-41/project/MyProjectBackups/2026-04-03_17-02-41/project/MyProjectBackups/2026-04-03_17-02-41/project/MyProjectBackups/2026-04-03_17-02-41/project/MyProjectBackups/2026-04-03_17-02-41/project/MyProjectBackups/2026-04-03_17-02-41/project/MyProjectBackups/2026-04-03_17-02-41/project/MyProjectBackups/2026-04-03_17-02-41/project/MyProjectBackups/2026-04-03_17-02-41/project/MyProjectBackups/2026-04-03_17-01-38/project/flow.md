🏗 Variant → InventoryItem → InventoryLevel Diagram
ProductVariant (commerce layer)
+-------------------------+
| SKU: TS-M-BLK           |  <- canonical SKU, used in orders, API, frontend
| option1: Medium         |
| option2: Black          |
| price: 1500             |
+-------------------------+
           |
           v
InventoryItem (stock identity)
+-------------------------+
| variant: TS-M-BLK       |  <- links to ProductVariant
| SKU: TS-M-BLK           |  <- warehouse-friendly SKU, usually same as variant
| tracked: True           |
| barcode: optional       |
+-------------------------+
           |
           v
InventoryLevel (per warehouse/location)
+-------------------------+
| InventoryItem: TS-M-BLK |
| Location: WH1           |
| Available: 10           |
| Incoming: 5             |
+-------------------------+
| InventoryItem: TS-M-BLK |
| Location: WH2           |
| Available: 5            |
| Incoming: 0             |
+-------------------------+
           |
           v
OMS / Fulfillment
+-------------------------+
| Order references SKU     |
| Check InventoryLevel     |
| Reserve stock / ship     |
+-------------------------+
           |
           v
Frontend / Customer
+-------------------------+
| Customer sees variant    |
| Selected options → SKU   |
| Price, availability      |
+-------------------------+



ProductVariant (SKU: TS-M-BLK)
        |
        v
InventoryItem (variant link)
        |
        v
InventoryLevel (per Warehouse)
  -------------------------------
  | WH1 | Available: 10        |
  | WH2 | Available: 5         |
  -------------------------------
        |
        v
Order Placement
        |
        v
Check Stock → Deduct from Warehouse(s)
        |
        v
Fulfillment / Shipping


🏗 Complete Product & Inventory Flow Diagram

1️⃣ Product Layer (Marketing)
+-------------------------+
| Product                 |
|-------------------------|
| title, description      |
| handle, status          |
+-------------------------+
           |
           v
2️⃣ Options Layer (Structure)
+-------------------------+
| ProductOption           |
|-------------------------|
| Name: Size, Color       |
| Position: order         |
+-------------------------+
           |
           v
3️⃣ Option Values
+-------------------------+
| ProductOptionValue      |
|-------------------------|
| Value: Small, Medium    |
| Value: Black, White     |
| Position: order         |
+-------------------------+
           |
           v
4️⃣ Variant Generation (Commerce Layer)
+-------------------------+
| ProductVariant          |
|-------------------------|
| SKU: TS-M-BLK           |
| Option1: Medium         |
| Option2: Black          |
| Price, compare_at_price |
| Weight, is_active       |
+-------------------------+
           |
           v
5️⃣ Inventory Identity
+-------------------------+
| InventoryItem           |
|-------------------------|
| Links to ProductVariant |
| SKU (mirrors variant)   |
| Barcode, tracked, cost  |
+-------------------------+
           |
           v
6️⃣ Multi-Location Stock
+-------------------------+
| InventoryLevel          |
|-------------------------|
| Warehouse1: Available=10|
| Warehouse2: Available=5 |
| Incoming stock tracked  |
+-------------------------+
           |
           v
7️⃣ Order Fulfillment
+-------------------------+
| OMS / Fulfillment       |
|-------------------------|
| Order references SKU    |
| Check InventoryLevel    |
| Reserve stock per wh    |
| Ship items              |
+-------------------------+
           |
           v
8️⃣ Frontend / Customer
+-------------------------+
| Customer sees options   |
| Dropdowns: Size, Color  |
| Selected variant → SKU  |
| Shows price & stock     |
+-------------------------+

🏗 Inventory Tracking Flow: Tracked vs Non-Tracked


                 ProductVariant
                 +-------------------+
                 | SKU: TS-M-BLK     |
                 | Price: 1500       |
                 +-------------------+
                           |
                           v
                 InventoryItem
                 +-------------------+
Tracked=True  --> | tracked: True      | --> OMS checks InventoryLevel before fulfilling
                 | SKU: TS-M-BLK     |
                 +-------------------+
                           |
                           v
                 InventoryLevel (per warehouse)
                 +-------------------+
                 | WH1: Available=10 |
                 | WH2: Available=5  |
                 +-------------------+
                           |
                           v
                 OMS / Fulfillment
                 +-------------------+
                 | Reserve stock     |
                 | Deduct available  |
                 | Ship items        |
                 +-------------------+

Tracked=False --> InventoryItem
                 +-------------------+
                 | tracked: False     | --> OMS ignores stock
                 | SKU: EBOOK-001    |
                 +-------------------+
                           |
                           v
                 InventoryLevel ignored
                           |
                           v
                 OMS / Fulfillment
                 +-------------------+
                 | Always available  |
                 | No stock check    |
                 | Ship / deliver    |
                 +-------------------+