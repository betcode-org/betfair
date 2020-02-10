import betfairlightweight
from betfairlightweight import filters


# create trading instance
trading = betfairlightweight.APIClient("username", "password", app_key="appKey")

# login
trading.login()

# make event type request to find horse racing event type
horse_racing_event_type_id = trading.betting.list_event_types(
    filter=filters.market_filter(text_query="Horse Racing")
)

# returns one result
print(horse_racing_event_type_id)

for event_type in horse_racing_event_type_id:
    # prints id, name and market count
    print(event_type.event_type.id, event_type.event_type.name, event_type.market_count)
    horse_racing_id = event_type.event_type.id

    # list all horse racing market catalogues
    market_catalogues = trading.betting.list_market_catalogue(
        filter=filters.market_filter(
            event_type_ids=[horse_racing_id],  # filter on just horse racing
            market_countries=["GB"],  # filter on just GB countries
            market_type_codes=["WIN"],  # filter on just WIN market types
        ),
        market_projection=[
            "MARKET_START_TIME",
            "RUNNER_DESCRIPTION",
        ],  # runner description required
        max_results=1,
    )

    print("%s market catalogues returned" % len(market_catalogues))

    for market_catalogue in market_catalogues:
        # prints market id, market name and market start time
        print(
            market_catalogue.market_id,
            market_catalogue.market_name,
            market_catalogue.market_start_time,
        )

        for runner in market_catalogue.runners:
            # prints runner id, runner name and handicap
            print(runner.selection_id, runner.runner_name, runner.handicap)

        # market book request
        market_books = trading.betting.list_market_book(
            market_ids=[market_catalogue.market_id],
            price_projection=filters.price_projection(
                price_data=filters.price_data(ex_all_offers=True)
            ),
        )

        for market_book in market_books:
            # prints market id, inplay?, status and total matched
            print(
                market_book.market_id,
                market_book.inplay,
                market_book.status,
                market_book.total_matched,
            )

            for runner in market_book.runners:
                # prints selection id, status and total matched
                print(runner.selection_id, runner.status, runner.total_matched)

                available_to_back = runner.ex.available_to_back
                available_to_lay = runner.ex.available_to_lay
                print(available_to_back, available_to_lay)


# logout
trading.logout()
