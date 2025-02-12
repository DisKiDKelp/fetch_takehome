from datetime import date, datetime
from math import ceil, floor

from receipt_processor.models import Item, Receipt


def calculate_points(reciept: Receipt) -> int:
    """Calculate points helper function."""

    # One point for every alphanumeric character in the retailer name.
    retailer_name_points = sum([i.isalnum() for i in reciept.retailer])

    receipt_total_points = calc_receipt_total_points(reciept.total)

    items_points = calc_item_points(items=reciept.items)

    timeframe_points = calc_timeframe_points(
        purchase_date=reciept.purchase_date,
        purchase_time=reciept.purchase_time,
    )

    return retailer_name_points + receipt_total_points + items_points + timeframe_points


def calc_receipt_total_points(reciept_total: int) -> int:
    """Calculate Points based on the total amount."""

    # 50 points if the total is a round dollar amount with no cents.
    if reciept_total % 100 == 0:
        # A whole dollar is a multiple of .25, add points for both
        return 75

    # 25 points if the total is a multiple of 0.25.
    if reciept_total % 25 == 0:
        return 25

    return 0


def calc_item_points(items: list[Item]) -> int:
    """Calculate points based on items, both total number and description."""

    # 5 points for every two items on the receipt.
    number_of_items_points = (len(items) // 2) * 5

    # If the trimmed length of the item description is a multiple of 3
    # multiply the price by 0.2 and round up to the nearest integer
    description_points = 0
    for item in items:
        description_len = len(item.short_description.strip())
        if description_len % 3 == 0:
            # Convert to cents
            item_price_cents = item.price / 100
            description_points += ceil(item_price_cents * 0.2)

    return number_of_items_points + description_points


def calc_timeframe_points(purchase_date: date, purchase_time: datetime) -> int:
    """Calculate points based on the time the order was seen."""

    # 6 points if the day in the purchase date is odd.
    date_points = 6
    if purchase_date.day % 2 == 0:
        # It's an even day so set added points to 0
        date_points = 0

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    time_of_day_points = 0

    # Define time range
    start_time = datetime.strptime("14:00", "%H:%M").time()
    end_time = datetime.strptime("16:00", "%H:%M").time()

    # Check if purchase time is within range
    if start_time <= purchase_time <= end_time:
        time_of_day_points = 10

    return date_points + time_of_day_points
