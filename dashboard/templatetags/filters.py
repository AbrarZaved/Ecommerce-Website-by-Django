from django import template
import ast

register = template.Library()


@register.filter
def details(dict):
    # Convert string representation of list to actual list
    data_list = ast.literal_eval(dict)

    # Convert list of dictionaries to a single dictionary
    product_details = {key: value for d in data_list for key, value in d.items()}

    # Define the keys you want to keep
    allowed_keys = [
        "Color",
        "Pattern",
        "Ideal For",
        "Fabric",
        "Type",
        "Fabric Care",
        "Style Code",
    ]

    # Filter the dictionary to only include allowed keys
    filtered_details = {
        key: value for key, value in product_details.items() if key in allowed_keys
    }

    # If filtered details don't have 7 items, add the first available ones
    if len(filtered_details) < 7:
        missing_keys = [key for key in allowed_keys if key not in filtered_details]
        for key in missing_keys[: 7 - len(filtered_details)]:
            # Add the missing key with a placeholder value if not present
            filtered_details[key] = "Not Available"

    # Truncate values to 25 characters
    result = "<br>".join(
        f"{key}: {value if value != 'India' else 'Bangladesh'}"
        for key, value in filtered_details.items()
    )

    # Return result with HTML <br> for new lines
    return result
