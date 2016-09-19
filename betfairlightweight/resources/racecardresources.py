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


class DaysSinceLastRun(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'days_since_last_run'
        attributes = {
            'days': 'days',
            'type': 'type'
        }


class Jockey(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'jockey'
        attributes = {
            'jockeyId': 'jockey_id',
            'name': 'name'
        }


class Selection(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'selection'
        attributes = {
            'marketId': 'market_id',
            'marketType': 'market_type',
            'selectionId': 'selection_id'
        }


class Trainer(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'trainer'
        attributes = {
            'location': 'location',
            'name': 'name',
            'trainerId': 'trainer_id'
        }


class Runner(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'runners'
        attributes = {
            'age': 'age',
            'comment': 'comment',
            'gender': 'gender',
            'horseId': 'horse_id',
            'isNonRunner': 'is_non_runner',
            'longHandicap': 'long_handicap',
            'name': 'name',
            'ownerColours': 'owner_colours',
            'recentForm': 'recent_form',
            'saddleCloth': 'saddle_cloth',
            'starRating': 'star_rating',
            'timeform123Place': 'timeform_123_place',
            'weight': 'weight',
            'winsAtCourse': 'wins_at_course',
            'winsAtCourseAndDistance': 'wins_at_course_and_distance',
            'winsAtDistance': 'wins_at_distance'
        }
        sub_resources = {
            'daysSinceLastRun': DaysSinceLastRun,
            'jockey': Jockey,
            'selections': Selection,
            'trainer': Trainer
        }


class RaceCard(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'race_card'
        attributes = {
            'bettingForecastText': 'betting_forecast_text',
            'comment': 'comment',
            'minimumWeight': 'minimum_weight',
            'numberOfNonRunners': 'number_of_non_runners',
            'numberOfRunners': 'number_of_runners',
            'prize': 'prize',
            'timeform123Text': 'timeform_123_text'
        }
        sub_resources = {
            'inPlayHints': InPlayHint,
            'race': Race,
            'runners': Runner
        }
