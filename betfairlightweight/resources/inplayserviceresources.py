from .baseresource import BaseResource


class InningOne(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'inning_one'
        attributes = {
            'overs': 'overs',
            'runs': 'runs',
            'wickets': 'wickets'
        }


class Home(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'home'
        attributes = {
            'bookingPoints': 'booking_points',
            'fullTimeScore': 'full_time_score',
            'games': 'games',
            'halfTimeScore': 'half_time_score',
            'name': 'name',
            'numberOfCards': 'number_of_cards',
            'numberOfCorners': 'number_of_corners',
            'numberOfCornersFirstHalf': 'number_of_corners_first_half',
            'numberOfCornersSecondHalf': 'number_of_corners_second_half',
            'numberOfRedCards': 'number_of_red_cards',
            'numberOfYellowCards': 'number_of_yellow_cards',
            'penaltiesScore': 'penalties_score',
            'penaltiesSequence': 'penalties_sequence',
            'score': 'score',
            'sets': 'sets',
            'highlight': 'highlight',
            'aces': 'aces',
            'doubleFaults': 'double_faults',
            'gameSequence': 'game_sequence',
            'isServing': 'is_serving',
            'playerSeed': 'player_seed',
            'serviceBreaks': 'service_breaks',
        }
        sub_resources = {
            'inning1': InningOne
        }


class Away(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'away'
        attributes = {
            'bookingPoints': 'booking_points',
            'fullTimeScore': 'full_time_score',
            'games': 'games',
            'halfTimeScore': 'half_time_score',
            'name': 'name',
            'numberOfCards': 'number_of_cards',
            'numberOfCorners': 'number_of_corners',
            'numberOfCornersFirstHalf': 'number_of_corners_first_half',
            'numberOfCornersSecondHalf': 'number_of_corners_second_half',
            'numberOfRedCards': 'number_of_red_cards',
            'numberOfYellowCards': 'number_of_yellow_cards',
            'penaltiesScore': 'penalties_score',
            'penaltiesSequence': 'penalties_sequence',
            'score': 'score',
            'sets': 'sets',
            'highlight': 'highlight',
            'aces': 'aces',
            'doubleFaults': 'double_faults',
            'gameSequence': 'game_sequence',
            'isServing': 'is_serving',
            'playerSeed': 'player_seed',
            'serviceBreaks': 'service_breaks',
        }
        sub_resources = {
            'inning1': InningOne
        }


class Score(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'score'
        attributes = {
            'bookingPoints': 'booking_points',
            'numberOfCards': 'number_of_cards',
            'numberOfCorners': 'number_of_corners',
            'numberOfCornersFirstHalf': 'number_of_corners_first_half',
            'numberOfCornersSecondHalf': 'number_of_corners_second_half',
            'numberOfRedCards': 'number_of_red_cards',
            'numberOfYellowCards': 'number_of_yellow_cards'

        }
        sub_resources = {
            'away': Away,
            'home': Home,
        }


class UpdateDetail(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'update_detail'
        attributes = {
            'elapsedRegularTime': 'elapsed_regular_time',
            'matchTime': 'match_time',
            'type': 'type',
            'updateId': 'update_id',
            'updateTime': 'update_time',
            'updateType': 'update_type',
            'team': 'team',
            'teamName': 'team_name',
        }
        datetime_attributes = (
            'updateTime'
        )


class EventTimeline(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'event_timeline'
        attributes = {
            'eventId': 'event_id',
            'elapsedRegularTime': 'elapsed_regular_time',
            'eventTypeId': 'event_type_id',
            'inPlayMatchStatus': 'in_play_match_status',
            'status': 'status',
            'timeElapsed': 'time_elapsed'

        }
        sub_resources = {
            'score': Score,
            'updateDetails': UpdateDetail,
        }


class FullTimeElapsed(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'full_time_elapsed'
        attributes = {
            'hour': 'hour',
            'min': 'min',
            'sec': 'sec'
        }


class StateOfBall(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'state_of_ball'
        attributes = {
            'appealId': 'appeal_id',
            'appealTypeName': 'appeal_type_name',
            'batsmanName': 'batsman_name',
            'batsmanRuns': 'batsman_runs',
            'bowlerName': 'bowler_name',
            'bye': 'bye',
            'dismissalTypeName': 'dismissal_type_name',
            'legBye': 'leg_bye',
            'noBall': 'no_ball',
            'outcomeId': 'outcome_id',
            'overBallNumber': 'over_ball_number',
            'overNumber': 'over_number',
            'referralOutcome': 'referral_outcome',
            'wide': 'wide'
        }


class Scores(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'scores'
        attributes = {
            'eventId': 'event_id',
            'elapsedRegularTime': 'elapsed_regular_time',
            'elapsedAddedTime': 'elapsed_added_time',
            'eventTypeId': 'event_type_id',
            'matchStatus': 'match_status',
            'timeElapsed': 'time_elapsed',
            'timeElapsedSeconds': 'time_elapsed_seconds',
            'status': 'status',
            'currentDay': 'current_day',
            'currentSet': 'current_set',
            'description': 'description',
            'matchType': 'match_type',
            'currentGame': 'current_game',
            'currentPoint': 'current_point'
        }
        sub_resources = {
            'fullTimeElapsed': FullTimeElapsed,
            'score': Score,
            'stateOfBall': StateOfBall
        }
