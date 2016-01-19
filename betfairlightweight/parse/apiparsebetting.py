from utils import key_check, strp_betfair_time


class PlaceOrder:

    def __init__(self, market_id, place_response):
        self.market_id = market_id
        self.bet_id = place_response['betId']
        self.status = place_response['status']
        self.customer_ref = key_check(place_response, 'customerRef')
        self.average_price_matched = place_response['averagePriceMatched']
        self.size_matched = place_response['sizeMatched']
        self.placed_date = strp_betfair_time(place_response['placedDate'])
        self.instruction = PlaceOrderInstruction(place_response['instruction'])


class PlaceOrderInstruction:

    def __init__(self, instruction):
        self.selection_id = instruction['selectionId']
        self.side = instruction['side']
        self.order_type = instruction['orderType']
        self.handicap = key_check(instruction, 'handicap')
        if 'limitOrder' in instruction:
            self.order = PlaceOrderLimit(instruction['limitOrder'])


class PlaceOrderLimit:

    def __init__(self, limit_order):
        self.persistence_type = limit_order['persistenceType']
        self.price = limit_order['price']
        self.size = limit_order['size']


class CancelOrder:

    def __init__(self, market_id, cancel_response):
        self.market_id = market_id
        self.status = cancel_response['status']
        self.customer_ref = key_check(cancel_response, 'customerRef')
        self.size_cancelled = cancel_response['sizeCancelled']
        self.cancelled_date = strp_betfair_time(cancel_response['cancelledDate'])
        self.instruction = CancelOrderInstruction(cancel_response['instruction'])


class CancelOrderInstruction:

    def __init__(self, instruction):
        self.bet_id = instruction['betId']
        self.size_reduction = key_check(instruction, 'sizeReduction')


class UpdateOrder:

    def __init__(self, market_id, update_response):
        self.market_id = market_id
        self.status = update_response['status']
        self.customer_ref = key_check(update_response, 'customerRef')
        self.instruction = UpdateOrderInstruction(update_response['instruction'])


class UpdateOrderInstruction:

    def __init__(self, instruction):
        self.bet_id = instruction['betId']
        self.new_persistence_type = instruction['newPersistenceType']


class ReplaceOrder:

    def __init__(self, market_id, replace_response):
        self.market_id = market_id
        self.status = replace_response['status']
        self.customer_ref = key_check(replace_response, 'customerRef')
        self.cancel_instruction = CancelOrder(market_id, replace_response['cancelInstructionReport'])
        self.place_instruction = PlaceOrder(market_id, replace_response['placeInstructionReport'])
