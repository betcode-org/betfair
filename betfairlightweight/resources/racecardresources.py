from .baseresource import BaseResource


class RaceType(object):
    """
    :type abbr: unicode
    :type full: unicode
    :type key: unicode
    """

    def __init__(self, abbr, full, key):
        self.abbr = abbr
        self.full = full
        self.key = key


class RaceClassification(object):
    """
    :type classification: unicode
    :type classification_abbr: unicode
    :type code: unicode
    :type display_name: unicode
    :type display_name_abbr: unicode
    """

    def __init__(self, classification, classificationAbbr, code, displayName, displayNameAbbr):
        self.classification = classification
        self.classification_abbr = classificationAbbr
        self.code = code
        self.display_name = displayName
        self.display_name_abbr = displayNameAbbr


class Market(object):
    """
    :type market_id: unicode
    :type market_type: unicode
    :type number_of_winners: int
    """

    def __init__(self, marketId, marketType, numberOfWinners):
        self.market_id = marketId
        self.market_type = marketType
        self.number_of_winners = numberOfWinners


class Going(object):
    """
    :type abbr: unicode
    :type full: unicode
    :type key: unicode
    """

    def __init__(self, abbr, full, key):
        self.abbr = abbr
        self.full = full
        self.key = key


class Course(object):
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

    def __init__(self, country, countryCode, courseId, name, surfaceType, timeformCourseCode, timezone, courseType=None):
        self.country = country
        self.country_code = countryCode
        self.course_id = courseId
        self.course_type = courseType
        self.name = name
        self.surface_type = surfaceType
        self.timeform_course_code = timeformCourseCode
        self.timezone = timezone


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

    def __init__(self, **kwargs):
        super(Race, self).__init__(**kwargs)
        self.betfair_meeting_id = kwargs.get('betfairMeetingId')
        self.distance = kwargs.get('distance')
        self.eligibility = kwargs.get('eligibility')
        self.is_results_available = kwargs.get('isResultAvailable')
        self.meeting_going = kwargs.get('meetingGoing')
        self.meeting_id = kwargs.get('meetingId')
        self.number_of_runners = kwargs.get('numberOfRunners')
        self.race_class = kwargs.get('raceClass')
        self.race_id = kwargs.get('raceId')
        self.race_title = kwargs.get('raceTitle')
        self.start_date = self.strip_datetime(kwargs.get('startDate')) if 'startDate' in kwargs else None
        self.course = Course(**kwargs.get('course')) if 'course' in kwargs else None
        self.going = Going(**kwargs.get('going')) if 'going' in kwargs else None
        self.markets = [Market(**i) for i in kwargs.get('markets') or []]
        self.race_classification = RaceClassification(**kwargs.get('raceClassification')) if 'raceClassification' in kwargs else None
        self.race_type = RaceType(**kwargs.get('raceType')) if 'raceType' in kwargs else None


class InPlayHint(object):
    """
    :type hint_name: unicode
    :type hint_value: unicode
    """

    def __init__(self, hintName, hintValue):
        self.hint_name = hintName
        self.hint_value = hintValue


class DaysSinceLastRun(object):
    """
    :type days: int
    :type type: unicode
    """

    def __init__(self, days, type):
        self.days = days
        self.type = type


class Jockey(object):
    """
    :type jockey_id: unicode
    :type name: unicode
    """

    def __init__(self, jockeyId, name, allowance=None):
        self.jockey_id = jockeyId
        self.name = name
        self.allowance = allowance


class Selection(object):
    """
    :type market_id: unicode
    :type market_type: unicode
    :type selection_id: unicode
    """

    def __init__(self, marketId, marketType, selectionId, bsp=None):
        self.market_id = marketId
        self.market_type = marketType
        self.selection_id = selectionId
        self.bsp = bsp


class Trainer(object):
    """
    :type location: unicode
    :type name: unicode
    :type trainer_id: unicode
    """

    def __init__(self, location, name, trainerId):
        self.location = location
        self.name = name
        self.trainer_id = trainerId


class Wearing(object):
    """
    :type abbr: unicode
    :type full: unicode
    :type key: unicode
    """

    def __init__(self, abbr, full, key):
        self.abbr = abbr
        self.full = full
        self.key = key


class Runner(object):
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

    def __init__(self, age=None, draw=None, gender=None, horseId=None, longHandicap=None, name=None, ownerColours=None, saddleCloth=None,
                 weight=None, selections=None, trainer=None, jockey=None, starRating=None, comment=None, isNonRunner=False,
                 winsAtCourse=None, winsAtCourseAndDistance=None, winsAtDistance=None, daysSinceLastRun=None,
                 timeform123Place=None, officialRating=None, recentForm=None, wearing=None):
        self.age = age
        self.comment = comment
        self.draw = draw
        self.gender = gender
        self.horse_id = horseId
        self.is_non_runner = isNonRunner
        self.long_handicap = longHandicap
        self.name = name
        self.official_rating = officialRating
        self.owner_colours = ownerColours
        self.recent_form = recentForm
        self.saddle_cloth = saddleCloth
        self.star_rating = starRating
        self.timeform_123_place = timeform123Place
        self.weight = weight
        self.wins_at_course = winsAtCourse
        self.wins_at_course_and_distance = winsAtCourseAndDistance
        self.wins_at_distance = winsAtDistance
        self.days_since_last_run = [DaysSinceLastRun(**i) for i in daysSinceLastRun] if daysSinceLastRun else []
        self.jockey = Jockey(**jockey) if jockey else None
        self.selections = [Selection(**i) for i in selections] if selections else []
        self.trainer = Trainer(**trainer) if trainer else None
        self.wearing = Wearing(**wearing) if wearing else None


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

    def __init__(self, **kwargs):
        super(RaceCard, self).__init__(**kwargs)
        self.betting_forecast_text = kwargs.get('bettingForecastText')
        self.comment = kwargs.get('comment')
        self.minimum_weight = kwargs.get('minimumWeight')
        self.number_of_non_runners = kwargs.get('numberOfNonRunners')
        self.number_of_runners = kwargs.get('numberOfRunners')
        self.prize = kwargs.get('prize')
        self.timeform_123_text = kwargs.get('timeform123Text')
        self.in_play_hints = [InPlayHint(**i) for i in
                              kwargs.get('inPlayHints') or []]
        self.race = Race(**kwargs.get('race'))
        self.runners = [Runner(**i) for i in kwargs.get('runners')]
