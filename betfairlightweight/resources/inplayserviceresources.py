from .baseresource import BaseResource


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
            'sets': 'sets'
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
            'sets': 'sets'
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
            'updateType': 'update_type'
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
