import re

def extract_session_id(session_str: str):
    """Extracts the session id from the given string"""
    match = re.search(r"/sessions/(.*)/contexts", session_str)

    if match:
        extracted_str = match.group(1)
        return extracted_str
    warning_message = "Could not extract session id from the given string"

    return warning_message

def get_str_from_food_dict(food_dict: dict):
    """Returns a string representation of the food dictionary"""
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])

if __name__ == "__main__":
    print(extract_session_id("projects/chatty-chatbot-qfqn/locations/global/agent/sessions/dcd8cbe1-fa23-57d0-d393-ea73964c10cc/contexts/ongoing-order"))
    print(get_str_from_food_dict({"Pizza": 2, "Burger": 3}))