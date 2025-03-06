import mysql.connector


global cnx
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="30062005",
    database="pandeyji_eatery"
)
def insert_order_item(food_item: str, quantity: int, order_id: int):
    """Inserts an order item into the database"""
    try:
        cursor = cnx.cursor()

        cursor.callproc("insert_order_item", [food_item, quantity, order_id])

        cnx.commit()

        cursor.close()

        print("Successfully inserted the order item")

        return 1

    except mysql.connector.Error as err:
        print(f"An error occurred inserting item: {err}")
        cnx.rollback()
        return -1

    except Exception as err:
        print(f"An error occurred inserting item: {err}")
        cnx.rollback()
        return -1

def insert_order_tracking(order_id: int, status: str):
    """Inserts an order tracking entry into the database"""
    try:
        cursor = cnx.cursor()

        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))

        cnx.commit()

        cursor.close()

        print("Successfully inserted the order tracking entry")

        return 1

    except mysql.connector.Error as err:
        print(f"An error occurred inserting order tracking entry: {err}")
        cnx.rollback()
        return -1

    except Exception as err:
        print(f"An error occurred inserting order tracking entry: {err}")
        cnx.rollback()
        return -1

def get_next_order_id():
    """Returns the next order id"""
    cursor = cnx.cursor()

    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()

    if result is None:
        return 1
    else:
        return result + 1

def get_order_total_price(order_id: int):
    """Returns the total price of an order"""
    cursor = cnx.cursor()

    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()

    return result

def get_order_status(order_id: int):
    """Returns the status of an order"""
    # Create a cursor object
    cursor = cnx.cursor()

    # Write the SQL query
    query = ("SELECT status FROM order_tracking WHERE order_id = %s")

    # execute the query
    cursor.execute(query, (order_id,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()

    if result is not None:
        return result[0]
    else:
        return None