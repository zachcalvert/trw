# this map ensures our verbs make grammatical sense
# no reactions in here; any action should be able to potentially receive any reaction

from bellybot.context.people import ALL_PEOPLE


ACTIONS = {
  "shotgun": {
    "past": "shotgunned",
    "present": "is shotgunning",
    "future": "shotgun",
    "objects": ["a tallboy", "a coors", "a PBR", "a Montucky"]
  },
  "fuck": {
    "past": "fucked",
    "present": "is fuckin",
    "future": "fuck",
    "objects": ["my ass", "me"]
  },
  "kick": {
    "past": "kicked",
    "present": "is kicking",
    "future": "kick",
    "objects": ["my ass"]
  },
  "whoop": {
    "past": "whooped",
    "present": "is whooping",
    "future": "whoop",
    "objects": ["my ass"]
  },
  "smoke": {
    "past": "smoked",
    "present": "is smoking",
    "future": "smoke",
    "objects": ["my ass", "a blunt", "a spliff", "a J"],
  },
  "cancel": {
    "past": "canceled",
    "present": "is canceling",
    "future": "cancel",
    "objects": ["my ass", "red zone", "our season", "our league"] + ALL_PEOPLE
  },
  "buy": {
    "past": "bought",
    "present": "is buying",
    "future": "buy",
    "objects": ["red zone", "a midget whore", "a stripper"]
  },
  "rejoin": {
    "past": "rejoined",
    "present": "is rejoining",
    "future": "rejoin",
    "objects": ["tinder"],
  },
  "run": {
    "past": "ran",
    "present": "is running",
    "future": "run",
    "objects": ["train", "wild", "a marathon"],
  },
  "order": {
    "past": "ordered",
    "present": "is ordering",
    "future": "order",
    "objects": ["breakfast burritos", "chinese", "pizza", "a stripper"],
  },
  "like": {
    "past": "liked",
    "present": "liking",
    "future": "like",
    "objects": ["his own comment"],
  },
  "drink": {
    "past": "drank",
    "present": "is drinking",
    "future": "drink",
    "objects": ["bb juice", "two white claws", "40s", "at Taylor's", "hella Booz", "a smoothie", "champagne"],
  },
  "take": {
    "past": "took",
    "present": "is taking",
    "future": "take",
    "objects": ["pictures", "xannys", "Ls", "that slow Dick", "a knee"],
  },
  "autodraft": {
    "past": "autodrafted",
    "present": "is autodrafting",
    "future": "autodraft",
    "objects": ["all Americans", "allstars", "complete ass"],
  },
  "pull": {
    "past": "pulled",
    "present": "is pulling",
    "future": "pull",
    "objects": ["it together", "it off", "off an epic comeback"],
  },
  "lose": {
    "past": "lost",
    "present": "is losing",
    "future": "lose",
    "objects": ["his matchup", "it", "again", "his keys", "his phone"],
  },
  "black out": {
    "past": "blacked",
    "present": "is blacking",
    "future": "black",
    "objects": ["out"],
  },
  "fleece": {
    "past": "fleeced",
    "present": "is fleecing",
    "future": "fleece",
    "objects": ["me", "my ass", "everyone"],
  },
  "eat": {
    "past": "ate",
    "present": "is eating",
    "future": "eat",
    "objects": ["my ass", "all the chicken sandos", "that ass", "a breakfast burrito", "that ahh", "a bag of dicks"],
  },
  "walk": {
    "past": "walked",
    "present": "is walking",
    "future": "walk",
    "objects": ["all the way home"],
  },
  "come": {
    "past": "came",
    "present": "is coming",
    "future": "come",
    "objects": ["back down to earth", "inside me", "through", "to the pit", "back", "over"],
  },
  "throw": {
    "past": "threw",
    "present": "throw",
    "future": "throw",
    "objects": ["hands", "up"],
  },
  "wax": {
    "past": "waxed",
    "present": "wax",
    "future": "wax",
    "objects": ["my ass", "that ass", ""],
  },
}