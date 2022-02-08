from .baseresource import BaseResource
from .bettingresources import PriceLadderDescription


class MarketDefinitionRunner:
    """
    :type adjustment_factor: float
    :type id: int
    :type removal_date: datetime.datetime
    :type sort_priority: int
    :type status: unicode
    """

    def __init__(
        self,
        id: int,
        sortPriority: int,
        status: str,
        hc: float = 0,
        bsp: float = None,
        adjustmentFactor: float = None,
        removalDate: str = None,
        name: str = None,
    ):
        self.selection_id = id
        self.sort_priority = sortPriority
        self.status = status
        self.handicap = hc
        self.bsp = bsp
        self.adjustment_factor = adjustmentFactor
        self.removal_date = BaseResource.strip_datetime(removalDate)
        self.name = name  # historic data only

    def __str__(self):
        return "MarketDefinitionRunner: %s" % self.selection_id

    def __repr__(self):
        return "<MarketDefinitionRunner>"


class MarketDefinitionKeyLineSelection:
    """
    :type selectionId: int
    :type handicap: float
    """

    def __init__(self, **kwargs):
        self.selection_id = kwargs.get("id")
        self.handicap = kwargs.get("hc")


class MarketDefinitionKeyLine:
    def __init__(self, kl):
        self.key_line = [MarketDefinitionKeyLineSelection(**i) for i in kl]


class MarketDefinition:
    """
    :type bet_delay: int
    :type betting_type: unicode
    :type bsp_market: bool
    :type bsp_reconciled: bool
    :type complete: bool
    :type country_code: unicode
    :type cross_matching: bool
    :type discount_allowed: bool
    :type event_id: unicode
    :type event_type_id: unicode
    :type in_play: bool
    :type market_base_rate: float
    :type market_time: datetime.datetime
    :type market_type: unicode
    :type number_of_active_runners: int
    :type number_of_winners: int
    :type open_date: datetime.datetime
    :type persistence_enabled: bool
    :type regulators: unicode
    :type runners: list[MarketDefinitionRunner]
    :type runners_voidable: bool
    :type settled_time: datetime.datetime
    :type status: unicode
    :type suspend_time: datetime.datetime
    :type timezone: unicode
    :type turn_in_play_enabled: bool
    :type venue: unicode
    :type version: int
    """

    def __init__(
        self,
        betDelay: int,
        bettingType: str,
        bspMarket: bool,
        bspReconciled: bool,
        complete: bool,
        crossMatching: bool,
        discountAllowed: bool,
        eventId: str,
        eventTypeId: str,
        inPlay: bool,
        marketBaseRate: float,
        marketTime: str,
        numberOfActiveRunners: int,
        numberOfWinners: int,
        persistenceEnabled: bool,
        regulators: str,
        runnersVoidable: bool,
        status: str,
        timezone: str,
        turnInPlayEnabled: bool,
        version: int,
        runners: list,
        openDate: str = None,
        countryCode: str = None,
        eachWayDivisor: float = None,
        venue: str = None,
        settledTime: str = None,
        suspendTime: str = None,
        marketType: str = None,
        lineMaxUnit: float = None,
        lineMinUnit: float = None,
        lineInterval: float = None,
        name: str = None,
        eventName: str = None,
        priceLadderDefinition: dict = None,
        keyLineDefinition: dict = None,
        raceType: str = None,
    ):
        self.bet_delay = betDelay
        self.betting_type = bettingType
        self.bsp_market = bspMarket
        self.bsp_reconciled = bspReconciled
        self.complete = complete
        self.country_code = countryCode
        self.cross_matching = crossMatching
        self.discount_allowed = discountAllowed
        self.event_id = eventId
        self.event_type_id = eventTypeId
        self.in_play = inPlay
        self.market_base_rate = marketBaseRate
        self.market_time = BaseResource.strip_datetime(marketTime)
        self.market_type = marketType
        self.number_of_active_runners = numberOfActiveRunners
        self.number_of_winners = numberOfWinners
        self.open_date = BaseResource.strip_datetime(openDate) if openDate else None
        self.persistence_enabled = persistenceEnabled
        self.regulators = regulators
        self.runners_voidable = runnersVoidable
        self.settled_time = BaseResource.strip_datetime(settledTime)
        self.status = status
        self.each_way_divisor = eachWayDivisor
        self.suspend_time = BaseResource.strip_datetime(suspendTime)
        self.timezone = timezone
        self.turn_in_play_enabled = turnInPlayEnabled
        self.venue = venue
        self.version = version
        self.line_max_unit = lineMaxUnit
        self.line_min_unit = lineMinUnit
        self.line_interval = lineInterval
        self.runners = [MarketDefinitionRunner(**i) for i in runners]
        self.price_ladder_definition = (
            PriceLadderDescription(**priceLadderDefinition)
            if priceLadderDefinition
            else None
        )
        self.key_line_definitions = (
            MarketDefinitionKeyLine(**keyLineDefinition) if keyLineDefinition else None
        )
        self.race_type = raceType

        self.name = name  # historic data only
        self.event_name = eventName  # historic data only


class Race(BaseResource):
    """
    :type market_id: unicode
    :type race_id: unicode
    :type rpm: dict
    :type rcm: dict
    """

    def __init__(self, **kwargs):
        self.streaming_unique_id = kwargs.pop("streaming_unique_id", None)
        self.streaming_update = kwargs.pop("streaming_update", None)
        self.streaming_snap = kwargs.pop("streaming_snap", False)
        self.publish_time_epoch = kwargs.get("pt")
        self.publish_time = self.strip_datetime(kwargs.get("pt"))
        super(Race, self).__init__(**kwargs)
        self.market_id = kwargs.get("mid")
        self.race_id = kwargs.get("id")
        self.race_progress = (
            RaceProgress(**kwargs["rpc"]) if kwargs.get("rpc") else None
        )
        self.race_runners = [RaceChange(**runner) for runner in kwargs.get("rrc") or []]


class RaceProgress:
    """
    :type publish_time: int
    :type feed_time: int
    :type race_id: unicode
    :type gate: unicode
    :type sectional_time: float
    :type running_time: float
    :type speed: float
    :type progress: float
    :type order: list
    """

    def __init__(self, **kwargs):
        self.feed_time_epoch = kwargs.get("ft")
        self.feed_time = BaseResource.strip_datetime(kwargs.get("ft"))
        self.gate_name = kwargs.get("g")
        self.sectional_time = kwargs.get("st")
        self.running_time = kwargs.get("rt")
        self.speed = kwargs.get("spd")
        self.progress = kwargs.get("prg")
        self.order = kwargs.get("ord")
        self.jumps = kwargs.get("J")


class RaceChange:
    """
    :type publish_time: int
    :type feed_time: int
    :type race_id: unicode
    :type selection_id: int
    :type lat: float
    :type long: float
    :type speed: float
    :type progress: float
    :type stride_frequency: float
    """

    def __init__(self, **kwargs):
        self.feed_time_epoch = kwargs.get("ft")
        self.feed_time = BaseResource.strip_datetime(kwargs.get("ft"))
        self.selection_id = kwargs.get("id")
        self.lat = kwargs.get("lat")
        self.long = kwargs.get("long")
        self.speed = kwargs.get("spd")
        self.progress = kwargs.get("prg")
        self.stride_frequency = kwargs.get("sfq")  # in Hz


class CricketFixtureInfo:
    """
    :type home_team: unicode
    :type away_team: unicode
    :type expected_start_time: unicode
    :type fixture_status: unicode
    :type event_description: unicode
    :type max_overs: int
    :type event_status: unicode
    """

    def __init__(self, **kwargs):
        self.home_team = kwargs.get("homeTeam")
        self.away_team = kwargs.get("awayTeam")
        self.expected_start_time = kwargs.get("expectedStartTime")
        self.fixture_status = kwargs.get("fixtureStatus")
        self.event_description = kwargs.get("eventDescription")
        self.max_overs = kwargs.get("maxOvers")
        self.event_status = kwargs.get("eventStatus")


class CricketTeamInfo:
    """
    :type name: unicode
    :type players: list[CricketPlayerInfo]
    :type selection_id: int
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.players = [
            CricketPlayerInfo(**player) for player in kwargs.get("players") or []
        ]
        self.selection_id = kwargs.get("selectionId")


class CricketPlayerInfo:
    """
    :type name: unicode
    :type is_captain: bool
    :type is_wicket_keeper: bool
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.is_captain = kwargs.get("isCaptain")
        self.is_wicket_keeper = kwargs.get("isWicketKeeper")


class CricketMatchStats:
    """
    :type current_innings: int
    :type toss_result: unicode
    :type innings_stats: list[CricketInningsStats]
    :type batting_team_stats: CricketBattingTeamStats
    :type bowling_team_stats: CricketBowlingTeamStats
    """

    def __init__(self, **kwargs):
        self.current_innings = kwargs.get("currentInnings")
        self.toss_result = kwargs.get("tossResult")
        self.innings_stats = [
            CricketInningsStats(**innings)
            for innings in kwargs.get("inningsStats") or []
        ]
        self.batting_team_stats = (
            CricketBattingTeamStats(**kwargs["battingTeamStats"])
            if kwargs.get("battingTeamStats")
            else None
        )
        self.bowling_team_stats = (
            CricketBowlingTeamStats(**kwargs["bowlingTeamStats"])
            if kwargs.get("bowlingTeamStats")
            else None
        )


class CricketInningsStats:
    """
    :type innings_num: int
    :type batting_team: unicode
    :type bowling_team: unicode
    :type innings_runs: int
    :type innings_overs: unicode
    :type innings_wickets: int
    """

    def __init__(self, **kwargs):
        self.innings_num = kwargs.get("inningsNum")
        self.batting_team = kwargs.get("battingTeam")
        self.bowling_team = kwargs.get("bowlingTeam")
        self.inningsRuns = kwargs.get("inningsRuns")
        self.inningsOvers = kwargs.get("inningsOvers")
        self.inningsWickets = kwargs.get("inningsWickets")


class CricketBattingTeamStats:
    """
    :type team_name: unicode
    :type bat_1_name: int
    :type bat_1_runs: int
    :type bat_1_balls: int
    :type bat_1_fours: int
    :type bat_1_sixes: int
    :type bat_1_strike: int
    :type bat_2_name: int
    :type bat_2_runs: int
    :type bat_2_balls: int
    :type bat_2_fours: int
    :type bat_2_sixes: int
    :type bat_2_strike: int
    """

    def __init__(self, **kwargs):
        self.team_name = kwargs.get("teamName")
        self.bat_1_name = kwargs.get("bat1Name")
        self.bat_1_runs = kwargs.get("bat1Runs")
        self.bat_1_balls = kwargs.get("bat1Balls")
        self.bat_1_fours = kwargs.get("bat1Fours")
        self.bat_1_sixes = kwargs.get("bat1Sixes")
        self.bat_1_strike = kwargs.get("bat1Strike")
        self.bat_2_name = kwargs.get("bat2Name")
        self.bat_2_runs = kwargs.get("bat2Runs")
        self.bat_2_balls = kwargs.get("bat2Balls")
        self.bat_2_fours = kwargs.get("bat2Fours")
        self.bat_2_sixes = kwargs.get("bat2Sixes")
        self.bat_2_strike = kwargs.get("bat2Strike")


class CricketBowlingTeamStats:
    """
    :type team_name
    :type bowl_1_name: unicode
    :type bowl_1_overs: unicode
    :type bowl_1_runs: int
    :type bowl_1_maidens: int
    :type bowl_1_wickets: int
    :type bowl_2_name: unicode
    :type bowl_2_overs: unicode
    :type bowl_2_runs: int
    :type bowl_2_maidens: int
    :type bowl_2_wickets: int
    """

    def __init__(self, **kwargs):
        self.team_name = kwargs.get("teamName")
        self.bowl_1_name = kwargs.get("bowl1Name")
        self.bowl_1_overs = kwargs.get("bowl1Overs")
        self.bowl_1_runs = kwargs.get("bowl1Runs")
        self.bowl_1_maidens = kwargs.get("bowl1Maidens")
        self.bowl_1_wickets = kwargs.get("bowl1Wickets")
        self.bowl_2_name = kwargs.get("bowl2Name")
        self.bowl_2_overs = kwargs.get("bowl2Overs")
        self.bowl_2_runs = kwargs.get("bowl2Runs")
        self.bowl_2_maidens = kwargs.get("bowl2Maidens")
        self.bowl_2_wickets = kwargs.get("bowl2Wickets")


class IncidentListWrapper:
    """
    :type incident_list: list[CricketIncident]
    """

    def __init__(self, **kwargs):
        self.incident_list = [
            CricketIncident(**incident) for incident in kwargs.get("incidentList") or []
        ]


class CricketIncident:
    """
    :type participant_ref: unicode
    :type incident_type: unicode
    :type value: unicode
    :type innings: int
    :type overs: unicode
    :type actual_time: int
    """

    def __init__(self, **kwargs):
        self.participant_ref = kwargs.get("participantRef")
        self.incident_type = kwargs.get("incidentType")
        self.value = kwargs.get("value")
        self.innings = kwargs.get("innings")
        self.overs = kwargs.get("overs")
        self.actual_time = kwargs.get("actualTime")


class CricketMatch(BaseResource):
    """
    :type event_id: unicode
    :type market_id: unicode
    :type fixture_info: CricketFixtureInfo
    :type home_team: CricketTeamInfo
    :type away_team: CricketTeamInfo
    :type match_stats: CricketMatchStats
    :type incident_list_wrapper: IncidentListWrapper
    """

    def __init__(self, **kwargs):
        self.streaming_unique_id = kwargs.pop("streaming_unique_id", None)
        self.streaming_update = kwargs.pop("streaming_update", None)
        self.streaming_snap = kwargs.pop("streaming_snap", False)
        self.publish_time_epoch = kwargs.get("pt")
        self.publish_time = self.strip_datetime(kwargs.get("pt"))
        super(CricketMatch, self).__init__(**kwargs)
        self.event_id = kwargs.get("eventId")
        self.market_id = kwargs.get("marketId")
        self.fixture_info = (
            CricketFixtureInfo(**kwargs["fixtureInfo"])
            if kwargs.get("fixtureInfo")
            else None
        )
        self.home_team = (
            CricketTeamInfo(**kwargs["homeTeam"]) if kwargs.get("homeTeam") else None
        )
        self.away_team = (
            CricketTeamInfo(**kwargs["awayTeam"]) if kwargs.get("awayTeam") else None
        )
        self.match_stats = (
            CricketMatchStats(**kwargs["matchStats"])
            if kwargs.get("matchStats")
            else None
        )
        self.incident_list_wrapper = (
            IncidentListWrapper(**kwargs["incidentListWrapper"])
            if kwargs.get("incidentListWrapper")
            else None
        )
