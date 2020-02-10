import betfairlightweight
from betfairlightweight import filters


# create trading instance
trading = betfairlightweight.APIClient("username", "password", app_key="appKey")

# login
trading.login()

# update for test
market_id = "1.131347484"
selection_id = 12029579


def place_order():
    # placing an order
    limit_order = filters.limit_order(size=2.00, price=1.01, persistence_type="LAPSE")
    instruction = filters.place_instruction(
        order_type="LIMIT",
        selection_id=selection_id,
        side="LAY",
        limit_order=limit_order,
    )
    place_orders = trading.betting.place_orders(
        market_id=market_id, instructions=[instruction]  # list
    )

    print(place_orders.status)
    for order in place_orders.place_instruction_reports:
        print(
            "Status: %s, BetId: %s, Average Price Matched: %s "
            % (order.status, order.bet_id, order.average_price_matched)
        )


def update_order(bet_id):
    # updating an order
    instruction = filters.update_instruction(
        bet_id=bet_id, new_persistence_type="PERSIST"
    )
    update_order = trading.betting.update_orders(
        market_id=market_id, instructions=[instruction]
    )

    print(update_order.status)
    for order in update_order.update_instruction_reports:
        print("Status: %s" % order.status)


def replace_order(bet_id):
    # replacing an order
    instruction = filters.replace_instruction(bet_id=bet_id, new_price=1.10)
    replace_order = trading.betting.replace_orders(
        market_id=market_id, instructions=[instruction]
    )

    print(replace_order.status)
    for order in replace_order.replace_instruction_reports:
        place_report = order.place_instruction_reports
        cancel_report = order.cancel_instruction_reports
        print(
            "Status: %s, New BetId: %s, Average Price Matched: %s "
            % (order.status, place_report.bet_id, place_report.average_price_matched)
        )


def cancel_order(bet_id):
    # cancelling an order
    instruction = filters.cancel_instruction(bet_id=bet_id, size_reduction=2.00)
    cancel_order = trading.betting.cancel_orders(
        market_id=market_id, instructions=[instruction]
    )

    print(cancel_order.status)
    for cancel in cancel_order.cancel_instruction_reports:
        print(
            "Status: %s, Size Cancelled: %s, Cancelled Date: %s"
            % (cancel.status, cancel.size_cancelled, cancel.cancelled_date)
        )
