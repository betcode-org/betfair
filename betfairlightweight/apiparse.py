

class EventTypes:

    def __init__(self, event_type):
        self.event_type_id = event_type['eventType']['id']
        self.event_type_name = event_type['eventType']['name']
        self.market_count = event_type['marketCount']
