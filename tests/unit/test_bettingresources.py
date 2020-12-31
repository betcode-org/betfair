import datetime
import unittest

from betfairlightweight import resources
from betfairlightweight.resources.bettingresources import (
    LimitOrder,
    LimitOnCloseOrder,
    MarketOnCloseOrder,
    PriceSize,
)
from betfairlightweight.compat import BETFAIR_DATE_FORMAT
from tests.unit.tools import create_mock_json


class BettingResourcesTest(unittest.TestCase):

    ELAPSED_TIME = 1.2

    def test_event_type_result(self):
        mock_response = create_mock_json("tests/resources/list_event_types.json")
        event_types = mock_response.json().get("result")

        for event_type in event_types:
            resource = resources.EventTypeResult(
                elapsed_time=self.ELAPSED_TIME, **event_type
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_count == event_type["marketCount"]
            assert resource.event_type.id == event_type["eventType"]["id"]
            assert resource.event_type.name == event_type["eventType"]["name"]

    def test_competition_result(self):
        mock_response = create_mock_json("tests/resources/list_competitions.json")
        competitions = mock_response.json().get("result")

        for competition in competitions:
            resource = resources.CompetitionResult(
                elapsed_time=self.ELAPSED_TIME, **competition
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_count == competition["marketCount"]
            assert resource.competition_region == competition["competitionRegion"]
            assert resource.competition.id == competition["competition"]["id"]
            assert resource.competition.name == competition["competition"]["name"]

    def test_time_range_result(self):
        mock_response = create_mock_json("tests/resources/list_time_ranges.json")
        time_ranges = mock_response.json().get("result")

        for time_range in time_ranges:
            resource = resources.TimeRangeResult(
                elapsed_time=self.ELAPSED_TIME, **time_range
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_count == time_range["marketCount"]
            assert resource.time_range._from == datetime.datetime.strptime(
                time_range["timeRange"]["from"], BETFAIR_DATE_FORMAT
            )
            assert resource.time_range.to == datetime.datetime.strptime(
                time_range["timeRange"]["to"], BETFAIR_DATE_FORMAT
            )

    def test_event_result(self):
        mock_response = create_mock_json("tests/resources/list_events.json")
        event_results = mock_response.json().get("result")

        for event_result in event_results:
            resource = resources.EventResult(
                elapsed_time=self.ELAPSED_TIME, **event_result
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_count == event_result["marketCount"]
            assert resource.event.id == event_result["event"]["id"]
            assert resource.event.open_date == datetime.datetime.strptime(
                event_result["event"]["openDate"], BETFAIR_DATE_FORMAT
            )
            assert resource.event.time_zone == event_result["event"]["timezone"]
            assert resource.event.country_code == event_result["event"]["countryCode"]
            assert resource.event.name == event_result["event"]["name"]
            assert resource.event.venue == event_result["event"]["venue"]

    def test_market_type_result(self):
        mock_response = create_mock_json("tests/resources/list_market_types.json")
        market_type_results = mock_response.json().get("result")

        for market_type_result in market_type_results:
            resource = resources.MarketTypeResult(
                elapsed_time=self.ELAPSED_TIME, **market_type_result
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_count == market_type_result["marketCount"]
            assert resource.market_type == market_type_result["marketType"]

    def test_country_result(self):
        mock_response = create_mock_json("tests/resources/list_countries.json")
        countries_results = mock_response.json().get("result")

        for countries_result in countries_results:
            resource = resources.CountryResult(
                elapsed_time=self.ELAPSED_TIME, **countries_result
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_count == countries_result["marketCount"]
            assert resource.country_code == countries_result["countryCode"]

    def test_venue_result(self):
        mock_response = create_mock_json("tests/resources/list_venues.json")
        venue_results = mock_response.json().get("result")

        for venue_result in venue_results:
            resource = resources.VenueResult(
                elapsed_time=self.ELAPSED_TIME, **venue_result
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_count == venue_result["marketCount"]
            assert resource.venue == venue_result["venue"]

    def test_market_catalogue(self):
        mock_response = create_mock_json("tests/resources/list_market_catalogue.json")
        market_catalogues = mock_response.json().get("result")

        for market_catalogue in market_catalogues:
            resource = resources.MarketCatalogue(
                elapsed_time=self.ELAPSED_TIME, **market_catalogue
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_id == market_catalogue["marketId"]
            assert resource.market_name == market_catalogue["marketName"]
            assert resource.total_matched == market_catalogue["totalMatched"]
            assert resource.market_start_time == datetime.datetime.strptime(
                market_catalogue["marketStartTime"], BETFAIR_DATE_FORMAT
            )

            assert resource.competition.id == market_catalogue["competition"]["id"]
            assert resource.competition.name == market_catalogue["competition"]["name"]

            assert resource.event.id == market_catalogue["event"]["id"]
            assert resource.event.open_date == datetime.datetime.strptime(
                market_catalogue["event"]["openDate"], BETFAIR_DATE_FORMAT
            )
            assert resource.event.time_zone == market_catalogue["event"]["timezone"]
            assert (
                resource.event.country_code == market_catalogue["event"]["countryCode"]
            )
            assert resource.event.name == market_catalogue["event"]["name"]
            assert resource.event.venue == market_catalogue["event"].get("venue")

            assert resource.event_type.id == market_catalogue["eventType"]["id"]
            assert resource.event_type.name == market_catalogue["eventType"]["name"]

            assert (
                resource.description.betting_type
                == market_catalogue["description"]["bettingType"]
            )
            assert (
                resource.description.bsp_market
                == market_catalogue["description"]["bspMarket"]
            )
            assert (
                resource.description.discount_allowed
                == market_catalogue["description"]["discountAllowed"]
            )
            assert (
                resource.description.market_base_rate
                == market_catalogue["description"]["marketBaseRate"]
            )
            assert resource.description.market_time == datetime.datetime.strptime(
                market_catalogue["description"]["marketTime"], BETFAIR_DATE_FORMAT
            )
            assert (
                resource.description.market_type
                == market_catalogue["description"]["marketType"]
            )
            assert (
                resource.description.persistence_enabled
                == market_catalogue["description"]["persistenceEnabled"]
            )
            assert (
                resource.description.regulator
                == market_catalogue["description"]["regulator"]
            )
            assert (
                resource.description.rules == market_catalogue["description"]["rules"]
            )
            assert (
                resource.description.rules_has_date
                == market_catalogue["description"]["rulesHasDate"]
            )
            assert resource.description.suspend_time == datetime.datetime.strptime(
                market_catalogue["description"]["suspendTime"], BETFAIR_DATE_FORMAT
            )
            assert (
                resource.description.turn_in_play_enabled
                == market_catalogue["description"]["turnInPlayEnabled"]
            )
            assert (
                resource.description.wallet == market_catalogue["description"]["wallet"]
            )
            assert resource.description.each_way_divisor == market_catalogue[
                "description"
            ].get("eachWayDivisor")
            assert resource.description.clarifications == market_catalogue[
                "description"
            ].get("clarifications")
            assert resource.description.line_range_info.interval == market_catalogue[
                "description"
            ]["lineRangeInfo"].get("interval")
            assert resource.description.line_range_info.market_unit == market_catalogue[
                "description"
            ]["lineRangeInfo"].get("marketUnit")
            assert (
                resource.description.line_range_info.min_unit_value
                == market_catalogue["description"]["lineRangeInfo"].get("minUnitValue")
            )
            assert (
                resource.description.line_range_info.max_unit_value
                == market_catalogue["description"]["lineRangeInfo"].get("maxUnitValue")
            )
            assert (
                resource.description.price_ladder_description.type
                == market_catalogue["description"]["priceLadderDescription"].get("type")
            )

            assert len(resource.runners) == 10
            assert resource.runners[6].handicap == 0.0
            assert resource.runners[6].runner_name == "SCR Altach"
            assert resource.runners[6].selection_id == 872710
            assert resource.runners[6].sort_priority == 7
            assert resource.runners[6].metadata == {"runnerId": "872710"}

    def test_market_catalogue_no_ero_data(self):
        mock_response = create_mock_json(
            "tests/resources/list_market_catalogue_no_ero.json"
        )
        market_catalogues = mock_response.json().get("result")

        for market_catalogue in market_catalogues:
            resources.MarketCatalogue(
                elapsed_time=self.ELAPSED_TIME, **market_catalogue
            )

    def test_market_book(self):
        mock_response = create_mock_json("tests/resources/list_market_book.json")
        market_books = mock_response.json().get("result")

        for market_book in market_books:
            resource = resources.MarketBook(
                elapsed_time=self.ELAPSED_TIME, **market_book
            )
            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_id == market_book["marketId"]
            assert resource.bet_delay == market_book["betDelay"]
            assert resource.bsp_reconciled == market_book["bspReconciled"]
            assert resource.complete == market_book["complete"]
            assert resource.cross_matching == market_book["crossMatching"]
            assert resource.inplay == market_book["inplay"]
            assert resource.is_market_data_delayed == market_book["isMarketDataDelayed"]
            assert resource.last_match_time == datetime.datetime.strptime(
                market_book["lastMatchTime"], BETFAIR_DATE_FORMAT
            )
            assert (
                resource.number_of_active_runners
                == market_book["numberOfActiveRunners"]
            )
            assert resource.number_of_runners == market_book["numberOfRunners"]
            assert resource.number_of_winners == market_book["numberOfWinners"]
            assert resource.runners_voidable == market_book["runnersVoidable"]
            assert resource.status == market_book["status"]
            assert resource.total_available == market_book["totalAvailable"]
            assert resource.total_matched == market_book["totalMatched"]
            assert resource.version == market_book["version"]

            assert len(resource.runners) == len(market_book["runners"])

            for i, key_line in enumerate(
                market_book["keyLineDescription"].get("keyLine", [])
            ):
                assert (
                    key_line["handicap"]
                    == resource.key_line_description.key_line[i].handicap
                )
                assert (
                    key_line["selectionId"]
                    == resource.key_line_description.key_line[i].selection_id
                )

            for i, runner in enumerate(market_book["runners"]):
                resource_runner = resource.runners[i]
                assert resource_runner.selection_id == runner["selectionId"]
                assert resource_runner.status == runner["status"]
                assert resource_runner.total_matched == runner.get("totalMatched")
                assert resource_runner.adjustment_factor == runner.get(
                    "adjustmentFactor"
                )
                assert resource_runner.handicap == runner["handicap"]
                assert resource_runner.last_price_traded == runner.get(
                    "lastPriceTraded"
                )

                if runner.get("removalDate"):
                    assert resource_runner.removal_date == datetime.datetime.strptime(
                        runner["removalDate"], BETFAIR_DATE_FORMAT
                    )
                # else:
                #     assert resource_runner.sp.near_price == runner['sp']['nearPrice']
                #     assert resource_runner.sp.far_price == runner['sp']['farPrice']
                #     assert resource_runner.sp.actual_sp == runner['sp']['actualSP']

                # assert resource_runner.sp.back_stake_taken == runner['sp']['backStakeTaken']
                # assert resource_runner.sp.lay_liability_taken == runner['sp']['layLiabilityTaken']
                #
                # assert resource_runner.ex.available_to_back == runner['ex'].get('availableToBack')
                # assert resource_runner.ex.available_to_lay == runner['ex'].get('availableToLay')
                # assert resource_runner.ex.traded_volume == runner['ex'].get('tradedVolume')

                # # print(resource_runner.orders)
                # # print(resource_runner.matches)
                # # todo complete

    def test_price_size(self):
        price_size = PriceSize(**{"price": 1.01, "size": 2048})
        self.assertEqual(price_size.price, 1.01)
        self.assertEqual(price_size.size, 2048)
        self.assertEqual(str(price_size), "Price: 1.01 Size: 2048")

    def test_match(self):
        match = {
            "selectionId": 123,
            "matchedLays": [{"price": 1.01, "size": 2.00}],
            "matchedBacks": [],
        }
        resource = resources.Match(**match)
        self.assertEqual(resource.selection_id, 123)
        self.assertEqual(resource.matched_backs, [])
        self.assertEqual(resource.matched_lays[0].price, 1.01)
        self.assertEqual(resource.matched_lays[0].size, 2.00)

    def test_current_orders(self):
        mock_response = create_mock_json("tests/resources/list_current_orders.json")
        current_orders = mock_response.json().get("result")
        resource = resources.CurrentOrders(
            elapsed_time=self.ELAPSED_TIME, **current_orders
        )
        assert resource.elapsed_time == self.ELAPSED_TIME
        assert len(resource.orders) == len(current_orders.get("currentOrders"))

        for current_order in current_orders.get("currentOrders"):
            assert resource.orders[0].bet_id == current_order["betId"]
            # todo complete

    def test_cleared_orders(self):
        mock_response = create_mock_json("tests/resources/list_cleared_orders.json")
        cleared_orders = mock_response.json().get("result")
        resource = resources.ClearedOrders(
            elapsed_time=self.ELAPSED_TIME, **cleared_orders
        )
        assert resource.elapsed_time == self.ELAPSED_TIME
        assert len(resource.orders) == len(cleared_orders.get("clearedOrders"))

        for cleared_order in cleared_orders.get("clearedOrders"):
            assert resource.orders[0].bet_id == cleared_order["betId"]
            # todo complete

    def test_market_profit_loss(self):
        mock_response = create_mock_json(
            "tests/resources/list_market_profit_and_loss.json"
        )
        market_profits = mock_response.json().get("result")

        for market_profit in market_profits:
            resource = resources.MarketProfitLoss(
                elapsed_time=self.ELAPSED_TIME, **market_profit
            )

            assert resource.elapsed_time == self.ELAPSED_TIME
            assert resource.market_id == market_profit["marketId"]
            assert resource.commission_applied == market_profit.get("commissionApplied")

            assert len(resource.profit_and_losses) == len(
                market_profit["profitAndLosses"]
            )
            # todo complete

    def test_limit_order(self):
        limit_order = LimitOrder(
            1.01,
            12,
            persistenceType="LIMIT",
            timeInForce=True,
            minFillSize=2,
            betTargetType="BACKERS_PROFIT",
            betTargetSize=3,
        )
        assert limit_order.price == 1.01
        assert limit_order.size == 12
        assert limit_order.persistence_type == "LIMIT"
        assert limit_order.time_in_force is True
        assert limit_order.min_fill_size == 2
        assert limit_order.bet_target_type == "BACKERS_PROFIT"
        assert limit_order.bet_target_size == 3

    def test_limit_on_close_order(self):
        limit_on_close_order = LimitOnCloseOrder(liability=12, price=100)
        assert limit_on_close_order.liability == 12
        assert limit_on_close_order.price == 100

    def test_market_on_close_order(self):
        market_on_close_order = MarketOnCloseOrder(liability=12)
        assert market_on_close_order.liability == 12

    def test_place_orders(self):
        mock_response = create_mock_json("tests/resources/place_orders.json")
        place_orders = mock_response.json().get("result")
        resource = resources.PlaceOrders(elapsed_time=self.ELAPSED_TIME, **place_orders)
        assert resource.elapsed_time == self.ELAPSED_TIME
        assert resource.market_id == place_orders["marketId"]
        assert resource.status == place_orders["status"]
        assert resource.customer_ref == place_orders.get("customerRef")
        assert resource.error_code == place_orders.get("errorCode")
        assert len(resource.place_instruction_reports) == len(
            place_orders.get("instructionReports")
        )

        for order in place_orders.get("instructionReports"):
            assert (
                resource.place_instruction_reports[0].size_matched
                == order["sizeMatched"]
            )
            assert resource.place_instruction_reports[0].status == order["status"]
            assert resource.place_instruction_reports[0].bet_id == order["betId"]
            assert (
                resource.place_instruction_reports[0].average_price_matched
                == order["averagePriceMatched"]
            )
            assert resource.place_instruction_reports[
                0
            ].placed_date == datetime.datetime.strptime(
                order["placedDate"], BETFAIR_DATE_FORMAT
            )
            assert resource.place_instruction_reports[0].error_code == order.get(
                "errorCode"
            )

            assert (
                resource.place_instruction_reports[0].instruction.selection_id
                == order["instruction"]["selectionId"]
            )
            assert (
                resource.place_instruction_reports[0].instruction.side
                == order["instruction"]["side"]
            )
            assert (
                resource.place_instruction_reports[0].instruction.order_type
                == order["instruction"]["orderType"]
            )
            assert (
                resource.place_instruction_reports[0].instruction.handicap
                == order["instruction"]["handicap"]
            )

            assert (
                resource.place_instruction_reports[
                    0
                ].instruction.limit_order.persistence_type
                == order["instruction"]["limitOrder"]["persistenceType"]
            )
            assert (
                resource.place_instruction_reports[0].instruction.limit_order.price
                == order["instruction"]["limitOrder"]["price"]
            )
            assert (
                resource.place_instruction_reports[0].instruction.limit_order.size
                == order["instruction"]["limitOrder"]["size"]
            )

    def test_cancel_orders(self):
        mock_response = create_mock_json("tests/resources/cancel_orders.json")
        cancel_orders = mock_response.json().get("result")
        resource = resources.CancelOrders(
            elapsed_time=self.ELAPSED_TIME, **cancel_orders
        )
        assert resource.elapsed_time == self.ELAPSED_TIME
        assert resource.market_id == cancel_orders["marketId"]
        assert resource.status == cancel_orders["status"]
        assert resource.customer_ref == cancel_orders.get("customerRef")
        assert resource.error_code == cancel_orders.get("errorCode")
        assert len(resource.cancel_instruction_reports) == len(
            cancel_orders.get("instructionReports")
        )

        for order in cancel_orders.get("instructionReports"):
            assert (
                resource.cancel_instruction_reports[0].size_cancelled
                == order["sizeCancelled"]
            )
            assert resource.cancel_instruction_reports[0].status == order["status"]
            assert resource.cancel_instruction_reports[
                0
            ].cancelled_date == datetime.datetime.strptime(
                order["cancelledDate"], BETFAIR_DATE_FORMAT
            )

            assert (
                resource.cancel_instruction_reports[0].instruction.bet_id
                == order["instruction"]["betId"]
            )
            assert resource.cancel_instruction_reports[
                0
            ].instruction.size_reduction == order["instruction"].get("sizeReduction")

    def test_update_orders(self):
        mock_response = create_mock_json("tests/resources/update_orders.json")
        update_orders = mock_response.json().get("result")
        resource = resources.UpdateOrders(
            elapsed_time=self.ELAPSED_TIME, **update_orders
        )
        assert resource.elapsed_time == self.ELAPSED_TIME
        assert resource.market_id == update_orders["marketId"]
        assert resource.status == update_orders["status"]
        assert resource.customer_ref == update_orders.get("customerRef")
        assert resource.error_code == update_orders.get("errorCode")
        assert len(resource.update_instruction_reports) == len(
            update_orders.get("instructionReports")
        )

        for order in update_orders.get("instructionReports"):
            pass

    def test_replace_orders(self):
        mock_response = create_mock_json("tests/resources/replace_orders.json")
        replace_orders = mock_response.json().get("result")
        resource = resources.ReplaceOrders(
            elapsed_time=self.ELAPSED_TIME, **replace_orders
        )
        assert resource.elapsed_time == self.ELAPSED_TIME
        assert resource.market_id == replace_orders["marketId"]
        assert resource.status == replace_orders["status"]
        assert resource.customer_ref == replace_orders.get("customerRef")
        assert resource.error_code == replace_orders.get("errorCode")
        # assert len(resource.instruction_reports) == len(replace_orders.get('instructionReports'))
