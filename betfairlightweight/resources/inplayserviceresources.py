from .baseresource import BaseResource


class Innings:
    def __init__(self, overs, runs, wickets):
        self.overs = overs
        self.runs = runs
        self.wickets = wickets


class HomeAwayBase:
    def __init__(
        self,
        penaltiesScore,
        penaltiesSequence,
        halfTimeScore,
        fullTimeScore,
        name=None,
        score=None,
        sets=None,
        games=None,
        numberOfCards=None,
        numberOfCorners=None,
        numberOfCornersFirstHalf=None,
        numberOfCornersSecondHalf=None,
        numberOfRedCards=None,
        numberOfYellowCards=None,
        highlight=None,
        aces=None,
        doubleFaults=None,
        gameSequence=None,
        bookingPoints=None,
        isServing=None,
        playerSeed=None,
        serviceBreaks=None,
        inning1=None,
        inning2=None,
        quarterByQuarter=None,
    ):
        self.booking_points = bookingPoints
        self.full_time_score = fullTimeScore
        self.games = games
        self.half_time_score = halfTimeScore
        self.name = name
        self.number_of_cards = numberOfCards
        self.number_of_corners = numberOfCorners
        self.number_of_corners_first_half = numberOfCornersFirstHalf
        self.number_of_corners_second_half = numberOfCornersSecondHalf
        self.number_of_red_cards = numberOfRedCards
        self.number_of_yellow_cards = numberOfYellowCards
        self.penalties_score = penaltiesScore
        self.penalties_sequence = penaltiesSequence
        self.score = score
        self.sets = sets
        self.highlight = highlight
        self.aces = aces
        self.double_faults = doubleFaults
        self.game_sequence = gameSequence
        self.is_serving = isServing
        self.player_seed = playerSeed
        self.service_breaks = serviceBreaks
        self.inning1 = Innings(**inning1) if inning1 else None
        self.inning2 = Innings(**inning2) if inning2 else None
        self.quarter_by_quarter = quarterByQuarter


class Score:
    def __init__(
        self,
        home,
        away,
        bookingPoints=None,
        numberOfCards=None,
        numberOfCorners=None,
        numberOfCornersFirstHalf=None,
        numberOfCornersSecondHalf=None,
        numberOfRedCards=None,
        numberOfYellowCards=None,
    ):
        self.booking_points = bookingPoints
        self.number_of_cards = numberOfCards
        self.number_of_corners = numberOfCorners
        self.number_of_corners_first_half = numberOfCornersFirstHalf
        self.number_of_corners_second_half = numberOfCornersSecondHalf
        self.number_of_red_cards = numberOfRedCards
        self.number_of_yellow_cards = numberOfYellowCards
        self.home = HomeAwayBase(**home)
        self.away = HomeAwayBase(**away)


class UpdateDetail:
    def __init__(
        self,
        matchTime,
        type,
        updateTime,
        updateType,
        team=None,
        teamName=None,
        elapsedAddedTime=None,
        updateId=None,
        elapsedRegularTime=None,
        player=None,
    ):
        self.elapsed_regular_time = elapsedRegularTime
        self.match_time = matchTime
        self.type = type
        self.update_id = updateId
        self.update_time = BaseResource.strip_datetime(updateTime)
        self.update_type = updateType
        self.team = team
        self.team_name = teamName
        self.elapsed_added_time = elapsedAddedTime
        self.player = player


class EventTimeline(BaseResource):
    def __init__(self, **kwargs):
        super(EventTimeline, self).__init__(**kwargs)
        self.event_id = kwargs.get("eventId")
        self.elapsed_regular_time = kwargs.get("elapsedRegularTime")
        self.event_type_id = kwargs.get("eventTypeId")
        self.in_play_match_status = kwargs.get("inPlayMatchStatus")
        self.status = kwargs.get("status")
        self.time_elapsed = kwargs.get("timeElapsed")
        self.score = Score(**kwargs.get("score")) if kwargs.get("score") else None
        self.update_detail = (
            [UpdateDetail(**i) for i in kwargs.get("updateDetails")]
            if kwargs.get("updateDetails")
            else []
        )


class FullTimeElapsed:
    def __init__(self, hour, min, sec):
        self.hour = hour
        self.min = min
        self.sec = sec


class StateOfBall:
    def __init__(
        self,
        appealId,
        appealTypeName,
        batsmanName,
        batsmanRuns,
        bowlerName,
        bye,
        dismissalTypeName,
        legBye,
        noBall,
        outcomeId,
        overBallNumber,
        overNumber,
        referralOutcome,
        wide,
    ):
        self.appeal_id = appealId
        self.appeal_type_name = appealTypeName
        self.batsman_name = batsmanName
        self.batsman_runs = batsmanRuns
        self.bowler_name = bowlerName
        self.bye = bye
        self.dismissal_type_name = dismissalTypeName
        self.leg_bye = legBye
        self.no_ball = noBall
        self.outcome_id = outcomeId
        self.over_ball_number = overBallNumber
        self.over_number = overNumber
        self.referral_outcome = referralOutcome
        self.wide = wide


class Scores(BaseResource):
    def __init__(self, **kwargs):
        super(Scores, self).__init__(**kwargs)
        self.event_id = kwargs.get("eventId")
        self.elapsed_regular_time = kwargs.get("elapsedRegularTime")
        self.elapsed_added_time = kwargs.get("elapsedAddedTime")
        self.event_type_id = kwargs.get("eventTypeId")
        self.match_status = kwargs.get("matchStatus")
        self.time_elapsed = kwargs.get("timeElapsed")
        self.time_elapsed_seconds = kwargs.get("timeElapsedSeconds")
        self.status = kwargs.get("status")
        self.current_day = kwargs.get("currentDay")
        self.current_set = kwargs.get("currentSet")
        self.description = kwargs.get("description")
        self.match_type = kwargs.get("matchType")
        self.current_game = kwargs.get("currentGame")
        self.current_point = kwargs.get("currentPoint")
        self.full_time_elapsed = FullTimeElapsed(**kwargs.get("fullTimeElapsed"))
        self.score = Score(**kwargs.get("score"))
        self.state_of_ball = (
            StateOfBall(**kwargs.get("stateOfBall"))
            if kwargs.get("stateOfBall")
            else None
        )


class Broadcast:
    def __init__(self, **kwargs):
        self.event_id = kwargs.get("eventId")
        self.has_live_streaming = kwargs.get("hasLiveStreaming")
        self.has_live_streaming_info = kwargs.get("hasLiveStreamingInfo")
        self.img_url = kwargs.get("imgUrl")
        self.overview_url = kwargs.get("overviewUrl")
        self.provider = kwargs.get("provider")
        self.provider_name = kwargs.get("providerName")
        self.provider_display_name = kwargs.get("providerDisplayName")
        self.channels = kwargs.get("channels")


class MatchInfo:
    def __init__(self, **kwargs):
        self.event_id = kwargs.get("eventId")
        self.match_id = kwargs.get("matchId")
        self.home_team = kwargs.get("homeTeam")
        self.away_team = kwargs.get("awayTeam")
        self.competition = kwargs.get("competition")
        self.event_type_id = kwargs.get("eventTypeId")
        self.start_time = BaseResource.strip_datetime(kwargs.get("startTime")) if kwargs.get("startTime") else None
        self.venue = kwargs.get("venue")
        self.in_play = kwargs.get("inPlay")


class ScoresAndBroadcast(BaseResource):
    def __init__(self, **kwargs):
        super(ScoresAndBroadcast, self).__init__(**kwargs)
        self.event_id = kwargs.get("eventId")
        self.elapsed_regular_time = kwargs.get("elapsedRegularTime")
        self.elapsed_added_time = kwargs.get("elapsedAddedTime")
        self.event_type_id = kwargs.get("eventTypeId")
        self.match_status = kwargs.get("matchStatus")
        self.time_elapsed = kwargs.get("timeElapsed")
        self.time_elapsed_seconds = kwargs.get("timeElapsedSeconds")
        self.status = kwargs.get("status")
        self.current_day = kwargs.get("currentDay")
        self.current_set = kwargs.get("currentSet")
        self.description = kwargs.get("description")
        self.match_type = kwargs.get("matchType")
        self.current_game = kwargs.get("currentGame")
        self.current_point = kwargs.get("currentPoint")
        self.full_time_elapsed = (
            FullTimeElapsed(**kwargs.get("fullTimeElapsed"))
            if kwargs.get("fullTimeElapsed")
            else None
        )
        self.score = Score(**kwargs.get("score")) if kwargs.get("score") else None
        self.state_of_ball = (
            StateOfBall(**kwargs.get("stateOfBall"))
            if kwargs.get("stateOfBall")
            else None
        )
        self.broadcasts = (
            [Broadcast(**b) for b in kwargs.get("broadcasts")]
            if kwargs.get("broadcasts")
            else []
        )
        self.match_info = (
            MatchInfo(**kwargs.get("matchInfo"))
            if kwargs.get("matchInfo")
            else None
        )
