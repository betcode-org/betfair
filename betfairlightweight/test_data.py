from betfairlightweight.resources.streamingresources import MarketDefinitionRunner


def create_market_definition_data():
    return {
        "bspMarket": True,
        "turnInPlayEnabled": True,
        "persistenceEnabled": True,
        "marketBaseRate": 5,
        "eventId": "29988339",
        "eventTypeId": "7",
        "numberOfWinners": 1,
        "bettingType": "ODDS",
        "marketType": "WIN",
        "marketTime": "2020-09-01T15:50:00.000Z",
        "suspendTime": "2020-09-01T15:50:00.000Z",
        "bspReconciled": False,
        "complete": True,
        "inPlay": False,
        "crossMatching": False,
        "runnersVoidable": False,
        "numberOfActiveRunners": 13,
        "betDelay": 0,
        "status": "OPEN",
        "runners": [
            {
                "adjustmentFactor": 13.103,
                "status": "ACTIVE",
                "sortPriority": 1,
                "id": 722234
            },
            {
                "adjustmentFactor": 22.954,
                "status": "ACTIVE",
                "sortPriority": 2,
                "id": 10860103
            },
            {
                "adjustmentFactor": 9.708,
                "status": "ACTIVE",
                "sortPriority": 3,
                "id": 3730295
            },
            {
                "adjustmentFactor": 9.708,
                "status": "ACTIVE",
                "sortPriority": 4,
                "id": 13356116
            },
            {
                "adjustmentFactor": 13.103,
                "status": "ACTIVE",
                "sortPriority": 5,
                "id": 22922469
            },
            {
                "adjustmentFactor": 7.347,
                "status": "ACTIVE",
                "sortPriority": 6,
                "id": 20838057
            },
            {
                "adjustmentFactor": 4.852,
                "status": "ACTIVE",
                "sortPriority": 7,
                "id": 28569319},
            {
                "adjustmentFactor": 2.99,
                "status": "ACTIVE",
                "sortPriority": 8,
                "id": 258127},
            {
                "adjustmentFactor": 6.294,
                "status": "ACTIVE",
                "sortPriority": 9,
                "id": 25092605},
            {
                "adjustmentFactor": 4.852,
                "status": "ACTIVE",
                "sortPriority": 10,
                "id": 24434008},
            {
                "adjustmentFactor": 3.911,
                "status": "ACTIVE",
                "sortPriority": 11,
                "id": 26588871},
            {
                "adjustmentFactor": 0.589,
                "status": "ACTIVE",
                "sortPriority": 12,
                "id": 20730420},
            {
                "adjustmentFactor": 0.589,
                "status": "ACTIVE",
                "sortPriority": 13,
                "id": 15287874}],
        "regulators": ["MR_INT"],
        "venue": "Kempton",
        "countryCode": "GB",
        "discountAllowed": True,
        "timezone": "Europe/London",
        "openDate": "2020-09-01T12:15:00.000Z",
        "version": 3341870393,
        "raceType": "Flat",
        "priceLadderDefinition": {"type": "CLASSIC"}
    }


def create_market_definition_runner():
    return MarketDefinitionRunner(
        id=1,
        sortPriority=1,
        status="ACTIVE",
        hc=0,
        bsp=None,
        adjustmentFactor=None,
        removalDate=None,
        name=None,
    )
