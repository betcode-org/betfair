import datetime

from ..parse.models import BetfairModel
from ..parse.enums import RaceStatusEnum
from ..utils import strp_betfair_time


class RaceStatus(BetfairModel):

    def __init__(self, date_time_sent, raw_response, result):
        super(RaceStatus, self).__init__(date_time_sent, raw_response)
        self.response_code = result.get('responseCode')
        self.race_id = result.get('raceId')
        self.meeting_id = result.get('meetingId')
        self.race_status = result.get('raceStatus')
        self.last_updated = result.get('lastUpdated')

    @property
    def race_status_description(self):
        return RaceStatusEnum[self.race_status].value


class Score(BetfairModel):

    def __init__(self, date_time_sent, raw_response, result):
        super(Score, self).__init__(date_time_sent, raw_response)
        self.result = result

        self.event_id = result.get('eventId')
        self.start_time = strp_betfair_time(result.get('startTime'))
        self.broadcast = Broadcast(result.get('broadcasts'))

        state = result.get('state')
        if state:
            event_type_id = state.get('eventTypeId')
            if event_type_id == 1:
                self.state = SoccerState(state)
            elif event_type_id == 2:
                self.state = TennisState(state)
            elif event_type_id == 4:
                self.state = CricketState(state)

    def difference(self, cls):
        if self.event_id != cls.event_id:
            raise TypeError('EventIds do not match')
        if not self.state or not cls.state:
            raise TypeError('state missing')
        if self.state.event_type_id == 1:
            for value in self.__dict__:
                if (isinstance(self.__dict__[value], (str, int, float, datetime.datetime)) and
                        self.__dict__[value] != cls.__dict__[value]):
                    print('Difference', value, self.__dict__[value], cls.__dict__[value])

            for value in self.state.__dict__:
                if (isinstance(self.state.__dict__[value], (str, int, float, datetime.datetime)) and
                        self.state.__dict__[value] != cls.state.__dict__[value]):
                    print('Difference', value, self.state.__dict__[value], cls.state.__dict__[value])


class Broadcast:

    def __init__(self, broadcast):
        self.is_data_visualization_available = broadcast.get('isDataVisualizationAvailable')
        self.is_live_video_available = broadcast.get('isDataVisualizationAvailable')
        self.radio = Radio(broadcast.get('radio'))
        self.bf_live_video = TV(broadcast.get('bfLiveVideo'))
        self.tv = [TV(tv) for tv in broadcast.get('tv')]


class Radio:

    def __init__(self, radio):
        self.url = radio.get('url')


class TV:

    def __init__(self, tv):
        self.channel = tv.get('channel')
        self.start_time = tv.get('startTime')
        self.end_time = tv.get('endTime')


class State:

    def __init__(self, state):
        self.event_id = state.get('eventId')
        self.event_type_id = state.get('eventTypeId')
        self.match_status = state.get('matchStatus')
        self.full_time_elapsed = TimeElapsed(state.get('fullTimeElapsed'))


class Scores:

    def __init__(self, score):
        self.name = score.get('name')
        self.full_time_score = score.get('fullTimeScore')
        self.half_time_score = score.get('halfTimeScore')
        self.highlight = score.get('highlight')
        self.penalties_score = score.get('penaltiesScore')
        self.penalties_sequence = score.get('penaltiesSequence')


class TimeElapsed:

    def __init__(self, time_elapsed):
        self.hour = time_elapsed.get('hour')
        self.min = time_elapsed.get('min')
        self.sec = time_elapsed.get('sec')

    @property
    def time_elapsed_seconds(self):
        return self.sec + (60 * self.min) + (60 * 60 * self.hour)


# Cricket

class CricketState(State):

    def __init__(self, state):
        super(CricketState, self).__init__(state)
        self.match_type = state.get('matchType')
        self.match_status = state.get('matchStatus')
        self.match_type = state.get('matchType')
        self.current_day = state.get('currentDay')
        self.current_set = state.get('currentSet')
        self.description = state.get('description')
        self.state_of_ball = BallState(state.get('stateOfBall'))
        self.score = CricketScore(state.get('score'))


class BallState:

    def __init__(self, ball_state):
        self.appeal_id = ball_state.get('appealId')
        self.appeal_type_name = ball_state.get('appealTypeName')
        self.batsman_name = ball_state.get('batsmanName')
        self.batsman_runs = ball_state.get('batsmanRuns')
        self.bowler_name = ball_state.get('bowlerName')
        self.bye = ball_state.get('bye')
        self.dismissal_type_name = ball_state.get('dismissalTypeName')
        self.leg_bye = ball_state.get('legBye')
        self.no_ball = ball_state.get('noBall')
        self.outcome_id = ball_state.get('outcomeId')
        self.over_ball_number = ball_state.get('overBallNumber')
        self.over_number = ball_state.get('overNumber')
        self.referral_outcome = ball_state.get('referralOutcome')
        self.wide = ball_state.get('wide')


class CricketScore:

    def __init__(self, score):
        self.home = CricketScoreScores(score.get('home'))
        self.away = CricketScoreScores(score.get('away'))


class CricketScoreScores(Scores):

    def __init__(self, score):
        super(CricketScoreScores, self).__init__(score)
        self.inning_one = Innings(score.get('inning1'))
        self.inning_two = Innings(score.get('inning2'))


class Innings:

    def __init__(self, inning):
        if inning:
            self.overs = inning.get('overs')
            self.runs = inning.get('runs')
            self.wickets = inning.get('wickets')


# Tennis

class TennisState(State):

    def __init__(self, state):
        super(TennisState, self).__init__(state)
        self.current_game = state.get('currentGame')
        self.current_point = state.get('currentPoint')
        self.current_set = state.get('currentSet')
        self.has_sets = state.get('hasSets')
        self.score = TennisScore(state.get('score'))


class TennisScore:

    def __init__(self, score):
        self.home = TennisScoreScores(score.get('home'))
        self.away = TennisScoreScores(score.get('away'))


class TennisScoreScores(Scores):

    def __init__(self, score):
        super(TennisScoreScores, self).__init__(score)
        self.aces = score.get('aces')
        self.double_faults = score.get('doubleFaults')
        self.game_sequence = score.get('gameSequence')
        self.games = score.get('games')
        self.is_serving = score.get('isServing')
        self.score = score.get('score')
        self.service_breaks = score.get('serviceBreaks')
        self.sets = score.get('sets')
        self.player_seed = score.get('playerSeed')


# Soccer

class SoccerState(State):

    def __init__(self, state):
        super(SoccerState, self).__init__(state)
        self.time_elapsed = state.get('timeElapsed')
        self.time_elapsed_seconds = state.get('timeElapsedSeconds')
        self.elapsed_regular_time = state.get('elapsedRegularTime')
        self.status = state.get('status')
        self.score = SoccerScore(state.get('score'))


class SoccerBase:

    def __init__(self, score):
        self.booking_points = score.get('bookingPoints')
        self.number_of_cards = score.get('numberOfCards')
        self.number_of_corners = score.get('numberOfCorners')
        self.number_of_corners_first_half = score.get('numberOfCornersFirstHalf')
        self.number_of_corners_second_half = score.get('numberOfCornersSecondHalf')
        self.number_of_red_cards = score.get('numberOfRedCards')
        self.number_of_yellow_cards = score.get('numberOfYellowCards')


class SoccerScore(SoccerBase):

    def __init__(self, score):
        super(SoccerScore, self).__init__(score)
        self.home = SoccerScoreScores(score.get('home'))
        self.away = SoccerScoreScores(score.get('away'))


class SoccerScoreScores(Scores, SoccerBase):

    def __init__(self, score):
        super(SoccerScoreScores, self).__init__(score)
        super(SoccerScoreScores, self).__init__(score)
        self.score = score.get('score')
        self.games = score.get('games')
        self.sets = score.get('sets')
