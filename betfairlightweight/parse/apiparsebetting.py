from betfairlightweight.utils import key_check, strp_betfair_time


class Order:

    def __init__(self, date_time_sent, raw_response, result, date_time_received):
        self.date_time_received = date_time_received
        self.date_time_sent = date_time_sent
        self.raw_response = raw_response
        self.market_id = result['marketId']
        self.status = result['status']
        self.customer_ref = key_check(result, 'customerRef')
        if self.status != 'SUCCESS':
            self.error_code = result['errorCode']


class PlaceOrder(Order):

    def __init__(self, date_time_sent, raw_response, result, date_time_placed):
        super(PlaceOrder, self).__init__(date_time_sent, raw_response, result, date_time_placed)
        self.instruction_reports = [PlaceOrderInstructionReports(order) for order in result['instructionReports']]


class PlaceOrderInstructionReports:

    def __init__(self, instruction_report):
        self.status = instruction_report['status']
        if self.status == 'SUCCESS':
            self.bet_id = instruction_report['betId']
            self.average_price_matched = instruction_report['averagePriceMatched']
            self.size_matched = instruction_report['sizeMatched']
            self.placed_date = strp_betfair_time(instruction_report['placedDate'])
        else:
            self.error_code = instruction_report['errorCode']
        self.instruction = PlaceOrderInstruction(instruction_report['instruction'])


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


class CancelAllOrders:

    def __init__(self, date_time_sent, raw_response, result, date_time_placed):
        self.date_time_received = date_time_placed
        self.date_time_sent = date_time_sent
        self.raw_response = raw_response
        self.status = result['status']
        self.instruction_report = result['instructionReports']


class CancelOrder(Order):  # todo cancel all orders has no response?

    def __init__(self, date_time_sent, raw_response, result, date_time_placed):
        super(CancelOrder, self).__init__(date_time_sent, raw_response, result, date_time_placed)
        self.instruction_reports = [CancelOrderInstructionReports(order) for order in result['instructionReports']]


class CancelOrderInstructionReports:

    def __init__(self, instruction_report):
        self.status = instruction_report['status']
        if self.status == 'SUCCESS':
            self.size_cancelled = instruction_report['sizeCancelled']
            self.cancelled_date = strp_betfair_time(instruction_report['cancelledDate'])
        else:
            self.error_code = instruction_report['errorCode']
        self.instruction = CancelOrderInstruction(instruction_report['instruction'])


class CancelOrderInstruction:

    def __init__(self, instruction):
        self.bet_id = instruction['betId']
        self.size_reduction = key_check(instruction, 'sizeReduction')


class UpdateOrder(Order):

    def __init__(self, date_time_sent, raw_response, result, date_time_placed):
        super(UpdateOrder, self).__init__(date_time_sent, raw_response, result, date_time_placed)
        self.instruction_reports = [UpdateOrderInstructionReports(order) for order in result['instructionReports']]


class UpdateOrderInstructionReports:

    def __init__(self, instruction_report):
        self.status = instruction_report['status']
        if self.status != 'SUCCESS':
            self.error_code = instruction_report['errorCode']
        self.instruction = UpdateOrderInstruction(instruction_report['instruction'])


class UpdateOrderInstruction:

    def __init__(self, instruction):
        self.bet_id = instruction['betId']
        self.new_persistence_type = instruction['newPersistenceType']


class ReplaceOrder(Order):

    def __init__(self, date_time_sent, raw_response, result, date_time_placed):
        super(ReplaceOrder, self).__init__(date_time_sent, raw_response, result, date_time_placed)
        self.instruction_reports = [ReplaceOrderInstructionReports(order) for order in result['instructionReports']]


class ReplaceOrderInstructionReports:

    def __init__(self, instruction_report):
        self.status = instruction_report['status']
        if self.status != 'SUCCESS':
            self.error_code = instruction_report['errorCode']
        self.cancel_instruction = CancelOrderInstructionReports(instruction_report['cancelInstructionReport'])
        if self.status == 'SUCCESS':
            self.place_instruction = PlaceOrderInstructionReports(instruction_report['placeInstructionReport'])
        else:
            self.place_instruction = ReplaceOrderPlace(instruction_report['placeInstructionReport'])


class ReplaceOrderPlace:

    def __init__(self, place_response):
        self.status = place_response['status']
        self.error_code = place_response['errorCode']
