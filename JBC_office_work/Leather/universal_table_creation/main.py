import pandas as pd
import pymysql

# --- Database connection details ---
db_config = {
    'host': 'localhost',      # change this if needed
    'user': 'root',
    'password': '',
    'database': 'Leather_repair_db',
    'port': 3306              # default MySQL port
}

# --- SQL query ---
query = """
SELECT 
  orders.id AS order_id_or_management_number, 
  order_items.description AS expert_description,
  order_items.id AS order_items_id,
  template_insert_histories.description_template_id
FROM 
  orders 
JOIN 
  order_items ON orders.id = order_items.order_id
JOIN 
  template_insert_histories ON order_items.id = template_insert_histories.order_item_id
GROUP BY 
  template_insert_histories.description_template_id
"""

# --- Connect to the database and fetch data ---
try:
    connection = pymysql.connect(**db_config)
    df = pd.read_sql(query, connection)
    connection.close()

    # --- Save to Excel ---
    output_file = "output.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Excel file saved successfully as '{output_file}'.")

except Exception as e:
    print("Error:", e)
