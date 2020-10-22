# this map ensures our verbs make grammatical sense
# no reactions in here; any action should be able to potentially receive any reaction

from bellybot.context.people import ALL_PEOPLE


ACTIONS = {
  "shotgun": {
    "past": "shotgunned",
    "present": "is shotgunning",
    "future": "to shotgun",
    "objects": ["a tallboy", "a coors", "a PBR", "a Montucky"]
  },
  "fuck": {
    "past": "fucked",
    "present": "is fuckin",
    "future": "to fuck",
    "objects": ["my ass", "me"]
  },
  "kick": {
    "past": "kicked",
    "present": "is kicking",
    "future": "to kick",
    "objects": ["my ass"]
  },
  "whoop": {
    "past": "whooped",
    "present": "is whooping",
    "future": "to whoop",
    "objects": ["my ass"]
  },
  "smoke": {
    "past": "smoked",
    "present": "is smoking",
    "future": "to smoke",
    "objects": ["my ass", "a blunt", "a spliff", "a J"],
  },
  "cancel": {
    "past": "canceled",
    "present": "is canceling",
    "future": "to cancel",
    "objects": ["my ass", "red zone", "our season", "our league"] + ALL_PEOPLE
  },
  "buy": {
    "past": "bought",
    "present": "is buying",
    "future": "to buy",
    "objects": ["red zone", "a midget whore", "a stripper"]
  },
  "rejoin": {
    "past": "rejoined",
    "present": "is rejoining",
    "future": "to rejoin",
    "objects": ["tinder"],
  }
}