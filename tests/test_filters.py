import datetime
import unittest

from betfairlightweight.filters import (
    market_filter,
    time_range,
    price_data,
    ex_best_offers_overrides,
    price_projection,
    place_instruction,
    limit_on_close_order,
    limit_order,
    cancel_instruction,
    market_on_close_order,
    replace_instruction,
    update_instruction,
    streaming_market_data_filter,
    streaming_market_filter,
    streaming_order_filter,
)


class FilterTest(unittest.TestCase):
    def test_streaming_market_filter(self):
        response = streaming_market_filter()
        assert response == {}

        response = streaming_market_filter(market_ids=[1, 2])
        assert response == {"marketIds": [1, 2]}

    def test_streaming_market_data_filter(self):
        response = streaming_market_data_filter()
        assert response == {}

        response = streaming_market_data_filter(ladder_levels=3)
        assert response == {"ladderLevels": 3}

    def test_streaming_order_filter(self):
        response = streaming_order_filter()
        assert response == {}

        response = streaming_order_filter(include_overall_position=True)
        assert response == {"includeOverallPosition": True}

    def test_time_range(self):
        dt1 = datetime.datetime.now()
        dt2 = datetime.datetime.now() + datetime.timedelta(days=1)

        cases = ((dt1.date(), None), (None, dt1.date()), (123, None), (None, 456))

        for case in cases:
            from_ = case[0]
            to = case[1]
            with self.assertRaises(TypeError):
                time_range(from_=from_, to=to)

        response = time_range()
        assert response == {"from": None, "to": None}

        response = time_range(from_=dt1, to=dt2)
        assert response == {"from": dt1.isoformat(), "to": dt2.isoformat()}

        response = time_range(from_="123", to="456")
        assert response == {"from": "123", "to": "456"}

    def test_market_filter(self):
        response = market_filter()
        assert response == {}

        response = market_filter(market_ids=["1.123"])
        assert response == {"marketIds": ["1.123"]}

    def test_price_data(self):
        response = price_data()
        assert response == []

        response = price_data(ex_best_offers=True)
        assert response == ["EX_BEST_OFFERS"]

    def test_ex_best_offers_overrides(self):
        response = ex_best_offers_overrides()
        assert response == {}

    def test_price_projection(self):
        response = price_projection()
        assert response == {
            "rolloverStakes": False,
            "priceData": [],
            "exBestOffersOverrides": {},
            "virtualise": True,
        }
        response = price_projection(price_data=price_data(sp_available=True))
        assert response == {
            "rolloverStakes": False,
            "priceData": ["SP_AVAILABLE"],
            "exBestOffersOverrides": {},
            "virtualise": True,
        }
        response = price_projection()
        assert response == {
            "rolloverStakes": False,
            "priceData": [],
            "exBestOffersOverrides": {},
            "virtualise": True,
        }

    def test_place_instruction(self):
        response = place_instruction("LIMIT", 123, "LAY")
        assert response == {"orderType": "LIMIT", "selectionId": 123, "side": "LAY"}

    def test_limit_order(self):
        response = limit_order(size=1.1, price=123, persistence_type="LAPSE")
        assert response == {"size": 1.1, "price": 123, "persistenceType": "LAPSE"}

    def test_limit_on_close_order(self):
        response = limit_on_close_order(1.1, 2.2)
        assert response == {"liability": 1.1, "price": 2.2}

    def test_market_on_close_order(self):
        response = market_on_close_order(1.1)
        assert response == {"liability": 1.1}

    def test_cancel_instruction(self):
        response = cancel_instruction("1.123")
        assert response == {"betId": "1.123"}

    def test_replace_instruction(self):
        response = replace_instruction("1.123", 12)
        assert response == {"betId": "1.123", "newPrice": 12}

    def test_update_instruction(self):
        response = update_instruction("1.123", "LAPSE")
        assert response == {"betId": "1.123", "newPersistenceType": "LAPSE"}
