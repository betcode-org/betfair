from .baseresource import BaseResource


class RaceType(BaseResource):
    """
    :type abbr: unicode
    :type full: unicode
    :type key: unicode
    """
    abbr = None
    full = None
    key = None

    class Meta(BaseResource.Meta):
        identifier = 'race_type'
        attributes = {
            'abbr': 'abbr',
            'full': 'full',
            'key': 'key'
        }


class RaceClassification(BaseResource):
    """
    :type classification: unicode
    :type classification_abbr: unicode
    :type code: unicode
    :type display_name: unicode
    :type display_name_abbr: unicode
    """
    classification = None
    classification_abbr = None
    code = None
    display_name = None
    display_name_abbr = None

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
    """
    :type market_id: unicode
    :type market_type: unicode
    :type number_of_winners: int
    """
    market_id = None
    market_type = None
    number_of_winners = None

    class Meta(BaseResource.Meta):
        identifier = 'markets'
        attributes = {
            'marketId': 'market_id',
            'marketType': 'market_type',
            'numberOfWinners': 'number_of_winners'
        }


class Going(BaseResource):
    """
    :type abbr: unicode
    :type full: unicode
    :type key: unicode
    """
    abbr = None
    full = None
    key = None

    class Meta(BaseResource.Meta):
        identifier = 'going'
        attributes = {
            'abbr': 'abbr',
            'full': 'full',
            'key': 'key'
        }


class Course(BaseResource):
    """
    :type country: unicode
    :type country_code: unicode
    :type course_id: unicode
    :type course_type: unicode
    :type name: unicode
    :type surface_type: unicode
    :type timeform_course_code: unicode
    :type timezone: unicode
    """
    country = None
    country_code = None
    course_id = None
    course_type = None
    name = None
    surface_type = None
    timeform_course_code = None
    timezone = None

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
    """
    :type betfair_meeting_id: unicode
    :type course: Course
    :type distance: int
    :type eligibility: unicode
    :type going: Going
    :type is_results_available: bool
    :type markets: list[Market]
    :type meeting_going: unicode
    :type meeting_id: unicode
    :type number_of_runners: int
    :type race_class: int
    :type race_classification: RaceClassification
    :type race_id: unicode
    :type race_title: unicode
    :type race_type: RaceType
    :type start_date: datetime.datetime
    """
    betfair_meeting_id = None
    course = None
    distance = None
    eligibility = None
    going = None
    is_results_available = None
    markets = None
    meeting_going = None
    meeting_id = None
    number_of_runners = None
    race_class = None
    race_classification = None
    race_id = None
    race_title = None
    race_type = None
    start_date = None

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
    """
    :type hint_name: unicode
    :type hint_value: unicode
    """
    hint_name = None
    hint_value = None

    class Meta(BaseResource.Meta):
        identifier = 'in_play_hints'
        attributes = {
            'hintName': 'hint_name',
            'hintValue': 'hint_value',
        }


class DaysSinceLastRun(BaseResource):
    """
    :type days: int
    :type type: unicode
    """
    days = None
    type = None

    class Meta(BaseResource.Meta):
        identifier = 'days_since_last_run'
        attributes = {
            'days': 'days',
            'type': 'type'
        }


class Jockey(BaseResource):
    """
    :type jockey_id: unicode
    :type name: unicode
    """
    jockey_id = None
    name = None

    class Meta(BaseResource.Meta):
        identifier = 'jockey'
        attributes = {
            'jockeyId': 'jockey_id',
            'name': 'name'
        }


class Selection(BaseResource):
    """
    :type market_id: unicode
    :type market_type: unicode
    :type selection_id: unicode
    """
    market_id = None
    market_type = None
    selection_id = None

    class Meta(BaseResource.Meta):
        identifier = 'selections'
        attributes = {
            'marketId': 'market_id',
            'marketType': 'market_type',
            'selectionId': 'selection_id'
        }


class Trainer(BaseResource):
    """
    :type location: unicode
    :type name: unicode
    :type trainer_id: unicode
    """
    location = None
    name = None
    trainer_id = None

    class Meta(BaseResource.Meta):
        identifier = 'trainer'
        attributes = {
            'location': 'location',
            'name': 'name',
            'trainerId': 'trainer_id'
        }


class Wearing(BaseResource):
    """
    :type abbr: unicode
    :type full: unicode
    :type key: unicode
    """
    abbr = None
    full = None
    key = None

    class Meta(BaseResource.Meta):
        identifier = 'wearing'
        attributes = {
            'abbr': 'abbr',
            'full': 'full',
            'key': 'key'
        }


class Runner(BaseResource):
    """
    :type age: int
    :type comment: unicode
    :type days_since_last_run: DaysSinceLastRun
    :type draw: int
    :type gender: unicode
    :type horse_id: unicode
    :type is_non_runner: bool
    :type jockey: Jockey
    :type long_handicap: int
    :type name: unicode
    :type official_rating: int
    :type owner_colours: unicode
    :type recent_form: unicode
    :type saddle_cloth: unicode
    :type selections: list[Selection]
    :type star_rating: int
    :type timeform_123_place: int
    :type trainer: Trainer
    :type wearing: Wearing
    :type weight: int
    :type wins_at_course: int
    :type wins_at_course_and_distance: int
    :type wins_at_distance: int
    """
    age = None
    comment = None
    days_since_last_run = None
    draw = None
    gender = None
    horse_id = None
    is_non_runner = None
    jockey = None
    long_handicap = None
    name = None
    official_rating = None
    owner_colours = None
    recent_form = None
    saddle_cloth = None
    selections = None
    star_rating = None
    timeform_123_place = None
    trainer = None
    wearing = None
    weight = None
    wins_at_course = None
    wins_at_course_and_distance = None
    wins_at_distance = None

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
            'winsAtDistance': 'wins_at_distance',
            'draw': 'draw',
            'officialRating': 'official_rating'
        }
        sub_resources = {
            'daysSinceLastRun': DaysSinceLastRun,
            'jockey': Jockey,
            'selections': Selection,
            'trainer': Trainer,
            'wearing': Wearing
        }


class RaceCard(BaseResource):
    """
    :type betting_forecast_text: unicode
    :type comment: unicode
    :type in_play_hints: InPlayHint
    :type minimum_weight: int
    :type number_of_non_runners: int
    :type number_of_runners: int
    :type prize: unicode
    :type race: Race
    :type runners: list[Runner]
    :type timeform_123_text: unicode
    """
    betting_forecast_text = None
    comment = None
    in_play_hints = None
    minimum_weight = None
    number_of_non_runners = None
    number_of_runners = None
    prize = None
    race = None
    runners = None
    timeform_123_text = None

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
