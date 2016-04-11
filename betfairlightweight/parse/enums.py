from enum import Enum


class RaceStatusEnum(Enum):
    DORMANT = 'There is no data available for this race.'
    DELAYED = 'The start of the race has been delayed'
    PARADING = 'The horses are in the parade ring'
    GOINGDOWN = 'The horses are going down to the starting post'
    GOINGBEHIND = 'The horses are going behind the stalls'
    ATTHEPOST = 'The horses are at the post'
    UNDERORDERS = 'The horses are loaded into the stalls/race is about to start'
    OFF = 'The race has started'
    FINISHED = 'The race has finished'
    FALSESTART = 'There has been a false start'
    PHOTOGRAPH = 'The result of the race is subject to a photo finish'
    RESULT = 'The result of the race has been announced'
    WEIGHEDIN = 'The jockeys have weighed in'
    RACEVOID = 'The race has been declared void'
    ABANDONED = 'The meeting has been cancelled'
