from .baseresource import BaseResource


class RaceType(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'race_type'
        attributes = {
            'abbr': 'abbr',
            'full': 'full',
            'key': 'key'
        }


class RaceClassification(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'race_classification'
        attributes = {
            'classification': 'classification',
            'classificationAbbr': 'classification_abbr',
            'code': 'code',
            'displayName': 'display_name',
            'displayNameAbbr': 'display_name_abbr'
        }


class Market(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'markets'
        attributes = {
            'marketId': 'market_id',
            'marketType': 'market_type',
            'numberOfWinners': 'number_of_winners'
        }


class Going(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'going'
        attributes = {
            'abbr': 'abbr',
            'full': 'full',
            'key': 'key'
        }


class Course(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'course'
        attributes = {
            'country': 'country',
            'countryCode': 'country_code',
            'courseId': 'course_id',
            'courseType': 'course_type',
            'name': 'name',
            'surfaceType': 'surface_type',
            'timeformCourseCode': 'timeform_course_code',
            'timezone': 'timezone'
        }


class Race(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'race'
        attributes = {
            'betfairMeetingId': 'betfair_meeting_id',
            'distance': 'distance',
            'eligibility': 'eligibility',
            'isResultAvailable': 'is_results_available',
            'meetingGoing': 'meeting_going',
            'meetingId': 'meeting_id',
            'numberOfRunners': 'number_of_runners',
            'raceClass': 'race_class',
            'raceId': 'race_id',
            'raceTitle': 'race_title',
            'startDate': 'start_date',
        }
        sub_resources = {
            'course': Course,
            'going': Going,
            'markets': Market,
            'raceClassification': RaceClassification,
            'raceType': RaceType,
        }
        datetime_attributes = (
            'startDate',
        )


class InPlayHint(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'in_play_hints'
        attributes = {
            'hintName': 'hint_name',
            'hintValue': 'hint_value',
        }


class RaceCard(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'race_card'
        attributes = {
            'minimumWeight': 'minimum_weight',
            'prize': 'prize',
        }
        sub_resources = {
            'inPlayHints': InPlayHint,
            'race': Race,
        }
