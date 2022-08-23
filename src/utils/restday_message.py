import random
import json
import os

resources_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), 
        "..", "..", "resources"
        )
    )

# Responses JSON
with open(f"{resources_path}/responses.json") as json_file:
    responses = json.load(json_file)


def get_restday_message(ctx, day, input_type):
    # Get message
    message = random.choice(responses["on_restday"][input_type])
    message = message.replace("__user__", f"<@{ctx.author.id}>")
    message = message.replace("__day__", day)

    # Return message
    return message
