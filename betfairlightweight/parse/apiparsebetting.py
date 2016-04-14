from ..parse.models import BetfairModel
from ..utils import strp_betfair_time


class Order(BetfairModel):

    def __init__(self, date_time_sent, raw_response, result):
        super(Order, self).__init__(date_time_sent, raw_response)
        self.market_id = result.get('marketId')
        self.status = result.get('status')
        self.customer_ref = result.get('customerRef')
        self.error_code = result.get('errorCode')


class PlaceOrder(Order):

    def __init__(self, date_time_sent, raw_response, result):
        super(PlaceOrder, self).__init__(date_time_sent, raw_response, result)
        self.instruction_reports = [PlaceOrderInstructionReports(order) for order in result.get('instructionReports')]


class PlaceOrderInstructionReports:

    def __init__(self, instruction_report):
        self.status = instruction_report.get('status')
        if self.status == 'SUCCESS':
            self.bet_id = instruction_report.get('betId')
            self.average_price_matched = instruction_report.get('averagePriceMatched')
            self.size_matched = instruction_report.get('sizeMatched')
            self.placed_date = strp_betfair_time(instruction_report.get('placedDate'))
        self.error_code = instruction_report.get('errorCode')
        self.instruction = PlaceOrderInstruction(instruction_report.get('instruction'))


class PlaceOrderInstruction:

    def __init__(self, instruction):
        self.selection_id = instruction.get('selectionId')
        self.side = instruction.get('side')
        self.order_type = instruction.get('orderType')
        self.handicap = instruction.get('handicap')
        if 'limitOrder' in instruction:
            self.order = PlaceOrderLimit(instruction.get('limitOrder'))


class PlaceOrderLimit:

    def __init__(self, limit_order):
        self.persistence_type = limit_order.get('persistenceType')
        self.price = limit_order.get('price')
        self.size = limit_order.get('size')


class CancelAllOrders(BetfairModel):

    def __init__(self, date_time_sent, raw_response, result):
        super(CancelAllOrders, self).__init__(date_time_sent, raw_response)
        self.status = result.get('status')
        self.instruction_report = result.get('instructionReports')


class CancelOrder(Order):  # todo cancel all orders has no response?

    def __init__(self, date_time_sent, raw_response, result):
        super(CancelOrder, self).__init__(date_time_sent, raw_response, result)
        self.instruction_reports = [CancelOrderInstructionReports(order) for order in result.get('instructionReports')]


class CancelOrderInstructionReports:

    def __init__(self, instruction_report):
        self.status = instruction_report.get('status')
        if self.status == 'SUCCESS':
            self.size_cancelled = instruction_report.get('sizeCancelled')
            self.cancelled_date = strp_betfair_time(instruction_report.get('cancelledDate'))
        self.error_code = instruction_report.get('errorCode')
        self.instruction = CancelOrderInstruction(instruction_report.get('instruction'))


class CancelOrderInstruction:

    def __init__(self, instruction):
        self.bet_id = instruction.get('betId')
        self.size_reduction = instruction.get('sizeReduction')


class UpdateOrder(Order):

    def __init__(self, date_time_sent, raw_response, result):
        super(UpdateOrder, self).__init__(date_time_sent, raw_response, result)
        self.instruction_reports = [UpdateOrderInstructionReports(order) for order in result.get('instructionReports')]


class UpdateOrderInstructionReports:

    def __init__(self, instruction_report):
        self.status = instruction_report.get('status')
        self.error_code = instruction_report.get('errorCode')
        self.instruction = UpdateOrderInstruction(instruction_report.get('instruction'))


class UpdateOrderInstruction:

    def __init__(self, instruction):
        self.bet_id = instruction.get('betId')
        self.new_persistence_type = instruction.get('newPersistenceType')


class ReplaceOrder(Order):

    def __init__(self, date_time_sent, raw_response, result):
        super(ReplaceOrder, self).__init__(date_time_sent, raw_response, result)
        self.instruction_reports = [ReplaceOrderInstructionReports(order) for order in result.get('instructionReports')]


class ReplaceOrderInstructionReports:

    def __init__(self, instruction_report):
        self.status = instruction_report.get('status')
        self.error_code = instruction_report.get('errorCode')
        self.cancel_instruction = CancelOrderInstructionReports(instruction_report.get('cancelInstructionReport'))
        if self.status == 'SUCCESS':
            self.place_instruction = PlaceOrderInstructionReports(instruction_report.get('placeInstructionReport'))
        else:
            self.place_instruction = ReplaceOrderPlace(instruction_report.get('placeInstructionReport'))


class ReplaceOrderPlace:

    def __init__(self, place_response):
        self.status = place_response.get('status')
        self.error_code = place_response.get('errorCode')
