from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()
inprogress_orders = {}

@app.post("/")
async def handle_request(request: Request):
    """Handles the incoming Webhook request from Dialogflow"""
    # Get the Json data from the request
    data = await request.json()

    # Extract the info based on the structure of
    # the WebhookRequest from Dialogflow
    intent = data['queryResult']['intent']['displayName']
    parameters = data['queryResult']['parameters']
    output_contexts = data['queryResult']['outputContexts']

    session_id = generic_helper.extract_session_id((output_contexts[0]['name']))

    intent_handler_dict = {
        "order.add - context: ongoing-order": add_to_order,
        "order.remove - context: ongoing-order": remove_from_order,
        "order.complete - context: ongoing-order": complete_order,
        "track.order - context: ongoing-tracking": track_order
    }

    if intent in intent_handler_dict:
        return intent_handler_dict[intent](parameters, session_id)
    else:
        return JSONResponse(
            content={
                "fulfillmentText": "Sorry, I could not understand your request"
            }
        )

def remove_from_order(parameters: dict, session_id: str):
    """Removes the food items from the order"""
    if session_id not in inprogress_orders:
        fulfillment_text = "I am having a trouble finding your order. Sorry! Can you place a new order again?"
        return JSONResponse(
            content={
                "fulfillmentText": fulfillment_text
            }
        )

    current_order = inprogress_orders[session_id]
    food_items = parameters['food-item']

    removed_items = []
    no_such_items = []
    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f"Successfully removed {', '.join(removed_items)} from your order."

    if len(no_such_items) > 0:
        fulfillment_text = f"Sorry, I could not find {', '.join(no_such_items)} in your order."

    if len(current_order) == 0:
        fulfillment_text += "Your order is empty. Would you like to add something?"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Your current order is {order_str}. Would you like to add something?"

    return JSONResponse(
        content={
            "fulfillmentText": fulfillment_text
        }
    )

def add_to_order(parameters: dict, session_id: str):
    """Adds the food items to the order"""
    food_item = parameters['food-item']
    quantities = parameters['number']

    if len(food_item) != len(quantities):
        fulfillment_text = "Sorry, I could not understand the quantities of the items you mentioned."
    else:
        new_food_dict = dict(zip(food_item, quantities))

        if session_id in inprogress_orders:
            # Update the existing dictionary
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            # Create a new entry in the inprogress_orders dictionary
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])

        fulfillment_text = f"So far you have ordered {order_str}. Anything else you would like to add?"

    return JSONResponse(
        content={
            "fulfillmentText": fulfillment_text
        }
    )

def complete_order(parameters: dict, session_id: str):
    """Completes the order and places it in the database"""
    if session_id not in inprogress_orders:
        fulfillment_text = "I am having a trouble finding your order. Sorry! Can you place a new order again?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_database(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I could not place your order. Please try again."
        else:
            order_total = db_helper.get_order_total_price(order_id)
            fulfillment_text = f"Your order with id {order_id} has been placed successfully." \
            f"Here is your order id #{order_id}. You can track your order using this id."\
            f"Your order total is {order_total}, which will be delivered to you soon."

        del inprogress_orders[session_id]

    return JSONResponse(
        content={
            "fulfillmentText": fulfillment_text
        }
    )

def save_to_database(order: dict):
    """Saves the order to the database"""
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

def track_order(parameters: dict, session_id: str):
    """Tracks the order based on the order id"""
    order_id = int(parameters['number'])

    # Get the order status from the database
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"Your order with id {order_id} is {order_status}"
    else:
        fulfillment_text = f"Sorry, we could not find any order with id {order_id}"

    return JSONResponse(
        content={
            "fulfillmentText": fulfillment_text
        }
    )