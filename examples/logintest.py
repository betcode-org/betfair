import logging
import betfairlightweight


logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO,)


trading = betfairlightweight.APIClient('username', 'password')
betfairlightweight.login(trading)

# event_types = betfairlightweight.list_event_types(trading)
# competitions = betfairlightweight.list_competitions(trading)
# time_ranges = betfairlightweight.list_time_ranges(trading)
# events = betfairlightweight.list_events(trading)
# market_types = betfairlightweight.list_market_types(trading)
# country_codes = betfairlightweight.list_countries(trading)
# venues = betfairlightweight.list_venues(trading)
# params = {"filter": {"eventTypeIds": ["7"]},"maxResults": "1000","marketProjection": ["COMPETITION", "EVENT", "EVENT_TYPE", "RUNNER_DESCRIPTION", "MARKET_START_TIME"]}
# market_catalogue = betfairlightweight.list_market_catalogue(trading, params=params)
# market_book = betfairlightweight.list_market_book(trading, {'marketIds': ['1.124168894'], 'priceProjection': {'priceData': ['EX_TRADED']}})
# current_orders = betfairlightweight.list_current_orders(trading, {'marketIds': ['1.124168864']})
# cleared_orders = betfairlightweight.list_cleared_orders(trading)
# pandl = betfairlightweight.list_market_profit_and_loss(trading, {'marketIds': ['1.124168864']})
# race_status = betfairlightweight.list_race_status(trading, {'marketIds': ['1.124168864']})

# account_funds = betfairlightweight.get_account_funds(trading)
# account_details = betfairlightweight.get_account_details(trading)
# account_statement = betfairlightweight.get_account_statement(trading)
# currency_rates = betfairlightweight.list_currency_rates(trading)
# transfer_funds = betfairlightweight.transfer_funds(trading)

# params = {"marketId":"1.124181266", "instructions":[{"selectionId":"9365984","handicap":"0","side":"LAY","orderType":"LIMIT","limitOrder":{"size":'2.00',"price":'1.01',"persistenceType":"LAPSE"}}]}
# place_order = betfairlightweight.place_orders(trading, params)
# params = {"marketId":"1.124181266","instructions":[{"betId":place_order.instruction_reports[0].bet_id,"sizeReduction":None}]}
# cancel_order = betfairlightweight.cancel_orders(trading, params)
# params = {"marketId":"1.124181266","instructions":[{"betId": place_order.instruction_reports[0].bet_id,"newPrice":"1.10"}]}
# replace_order = betfairlightweight.replace_orders(trading, params)
# params = {"marketId":"1.124181266","instructions":[{"betId":place_order.instruction_reports[0].bet_id,"newPersistenceType":"PERSIST"}]}
# update_order = betfairlightweight.update_orders(trading, params)


betfairlightweight.logout(trading)
