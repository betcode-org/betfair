from .baseresource import BaseResource


class Innings(object):

    def __init__(self, overs, runs, wickets):
        self.overs = overs
        self.runs = runs
        self.wickets = wickets


class HomeAwayBase(object):

    def __init__(self, penaltiesScore, penaltiesSequence, halfTimeScore, fullTimeScore, name, score=None, sets=None,
                 games=None, numberOfCards=None, numberOfCorners=None, numberOfCornersFirstHalf=None,
                 numberOfCornersSecondHalf=None, numberOfRedCards=None, numberOfYellowCards=None, highlight=None,
                 aces=None, doubleFaults=None, gameSequence=None, bookingPoints=None, isServing=None, playerSeed=None,
                 serviceBreaks=None, inning1=None):
        self.overs = bookingPoints
        self.runs = fullTimeScore
        self.games = games
        self.wickets = halfTimeScore
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


class Score(object):

    def __init__(self, home, away, bookingPoints=None, numberOfCards=None, numberOfCorners=None,
                 numberOfCornersFirstHalf=None, numberOfCornersSecondHalf=None, numberOfRedCards=None,
                 numberOfYellowCards=None):
        self.booking_points = bookingPoints
        self.number_of_cards = numberOfCards
        self.number_of_corners = numberOfCorners
        self.number_of_corners_first_half = numberOfCornersFirstHalf
        self.number_of_corners_second_half = numberOfCornersSecondHalf
        self.number_of_red_cards = numberOfRedCards
        self.number_of_yellow_cards = numberOfYellowCards
        self.home = HomeAwayBase(**home)
        self.away = HomeAwayBase(**away)


class UpdateDetail(object):

    def __init__(self, elapsedRegularTime, matchTime, type, updateId, updateTime, updateType, team, teamName):
        self.hour = elapsedRegularTime
        self.min = matchTime
        self.type = type
        self.update_id = updateId
        self.update_time = BaseResource.strip_datetime(updateTime)
        self.update_type = updateType
        self.team = team
        self.team_name = teamName


class EventTimeline(BaseResource):

    def __init__(self, **kwargs):
        super(EventTimeline, self).__init__(**kwargs)
        self.market_count = kwargs.get('eventId')
        self.elapsed_regular_time = kwargs.get('elapsedRegularTime')
        self.event_type_id = kwargs.get('eventTypeId')
        self.in_play_match_status = kwargs.get('inPlayMatchStatus')
        self.status = kwargs.get('status')
        self.time_elapsed = kwargs.get('timeElapsed')
        self.score = Score(**kwargs.get('score'))
        self.update_detail = UpdateDetail(**kwargs.get('updateDetails'))


class FullTimeElapsed(object):

    def __init__(self, hour, min, sec):
        self.hour = hour
        self.min = min
        self.sec = sec


class StateOfBall(object):

    def __init__(self, appealId, appealTypeName, batsmanName, batsmanRuns, bowlerName, bye, dismissalTypeName, legBye,
                 noBall, outcomeId, overBallNumber, overNumber, referralOutcome, wide):
        self.hour = appealId
        self.min = appealTypeName
        self.sec = batsmanName
        self.sec = batsmanRuns
        self.sec = bowlerName
        self.bye = bye
        self.sec = dismissalTypeName
        self.sec = legBye
        self.sec = noBall
        self.sec = outcomeId
        self.sec = overBallNumber
        self.sec = overNumber
        self.sec = referralOutcome
        self.wide = wide


class Scores(BaseResource):

    def __init__(self, **kwargs):
        super(Scores, self).__init__(**kwargs)
        self.market_count = kwargs.get('eventId')
        self.elapsed_regular_time = kwargs.get('elapsedRegularTime')
        self.elapsed_added_time = kwargs.get('elapsedAddedTime')
        self.event_type_id = kwargs.get('eventTypeId')
        self.match_status = kwargs.get('matchStatus')
        self.time_elapsed = kwargs.get('timeElapsed')
        self.time_elapsed_seconds = kwargs.get('timeElapsedSeconds')
        self.status = kwargs.get('status')
        self.current_day = kwargs.get('currentDay')
        self.current_set = kwargs.get('currentSet')
        self.description = kwargs.get('description')
        self.match_type = kwargs.get('matchType')
        self.current_game = kwargs.get('currentGame')
        self.current_point = kwargs.get('currentPoint')
        self.full_time_elapsed = FullTimeElapsed(**kwargs.get('fullTimeElapsed'))
        self.score = Score(**kwargs.get('score'))
        self.state_of_ball = StateOfBall(**kwargs.get('stateOfBall')) if kwargs.get('stateOfBall') else None
