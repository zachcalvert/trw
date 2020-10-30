# this map ensures our verbs make grammatical sense
# no reactions in here; any action should be able to potentially receive any reaction

from bellybot.context.people import ALL_PEOPLE, PLAYERS

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
  "beat": {
    "past": "beat",
    "present": "is beating",
    "future": "beat",
    "objects": ["my ass", "off"]
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
    "objects": ["train", "wild"],
  },
  "order": {
    "past": "ordered",
    "present": "is ordering",
    "future": "order",
    "objects": ["breakfast burritos", "chinese", "pizza", "a stripper"],
  },
  "drink": {
    "past": "drank",
    "present": "is drinking",
    "future": "drink",
    "objects": ["bb juice", "two white claws", "40s", "at Taylor's", "hella Booz"],
  },
  "take": {
    "past": "took",
    "present": "is taking",
    "future": "take",
    "objects": ["pics", "xannys", "Ls", "that slow Dick", "a knee"],
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
    "objects": ["it together", "off the W", "off an epic comeback"],
  },
  "lose": {
    "past": "lost",
    "present": "is losing",
    "future": "lose",
    "objects": ["his matchup", "it", "it again", "his keys", "his phone"],
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
    "objects": ["me", "my ass", "me and my ass"],
  },
  "fucking fleece": {
    "past": "fucking fleeced",
    "present": "is fucking fleecing",
    "future": "fleece",
    "objects": ["me", "my ass", "me and my ass"],
  },
  "eat": {
    "past": "ate",
    "present": "is eating",
    "future": "eat",
    "objects": ["my ass", "all the chicken sandos", "that ass", "a breakfast burrito", "that ahh", "a bag of dicks", "splashed potatoes"],
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
    "objects": ["through", "to the pit", "back", "over"],
  },
  "throw": {
    "past": "threw",
    "present": "is throwing",
    "future": "throw",
    "objects": ["hands", "up", "me in an uber", "down"],
  },
  "wax": {
    "past": "waxed",
    "present": "is waxing",
    "future": "wax",
    "objects": ["my ass", "that ass", "that ahh"],
  },
  "rip": {
    "past": "ripped",
    "present": "is ripping",
    "future": "rip",
    "objects": ["ass", "my borthole open"],
  },
  "christian ponder": {
    "past": "christian pondered",
    "present": "is christian pondering",
    "future": "christian ponder",
    "objects": ["my trade offer", "my contributions to the squaw"],
  },
  "drop": {
    "past": "dropped",
    "present": "is dropping",
    "future": "drop",
    "objects": ["my ass", "passes"] + PLAYERS,
  },
  "trade": {
    "past": "traded",
    "present": "is trading",
    "future": "trade",
    "objects": ["my ass"] + PLAYERS,
  },
  "bench": {
    "past": "benched",
    "present": "is benching",
    "future": "bench",
    "objects": ["my ass"] + PLAYERS,
  },
  "start": {
    "past": "started",
    "present": "is starting",
    "future": "start",
    "objects": ["my ass"] + PLAYERS,
  },
  "cut": {
    "past": "cut",
    "present": "is cutting",
    "future": "cut",
    "objects": ["lines"],
  },
  "wreck": {
    "past": "wrecked",
    "present": "is wrecking",
    "future": "wreck",
    "objects": ["my ass", "shop"],
  },
  "pierce": {
    "past": "got",
    "present": "is getting",
    "future": "get",
    "objects": ["pierced"],
  },
  "wet": {
    "past": "got",
    "present": "is getting",
    "future": "get",
    "objects": ["wet"],
  },
  "blacked": {
    "past": "got",
    "present": "is getting",
    "future": "get",
    "objects": ["blacked"],
  },
  "high as balls": {
    "past": "got",
    "present": "is getting",
    "future": "get",
    "objects": ["high as balls"],
  },
  "wrecked on molly": {
    "past": "got",
    "present": "is getting",
    "future": "get",
    "objects": ["wrecked on molly"],
  },
  "railed": {
    "past": "got",
    "present": "is getting",
    "future": "get",
    "objects": ["railed"],
  },
  "flip": {
    "past": "flipped",
    "present": "is flipping",
    "future": "flip",
    "objects": ["through my roster"],
  },
  "talk": {
    "past": "was talking",
    "present": "is talking",
    "future": "talk",
    "objects": ["all kinds of shit"],
  },
  "do": {
    "past": "did",
    "present": "is doing",
    "future": "do",
    "objects": ["a strikeout", "me dirty", "the dirty bird", "zamsies"],
  },
  "kill": {
    "past": "killed",
    "present": "is killing",
    "future": "kill",
    "objects": ["me", "my ass", "another mickey's"],
  },
  "crack": {
    "past": "cracked",
    "present": "is cracking",
    "future": "crack",
    "objects": ["the first coffee of the morning", "my ass", "open another beer"],
  },
  "covid": {
    "past": "got",
    "present": "is getting",
    "future": "get",
    "objects": ["covid"],
  }
}

# if we feel positively about a player, it's because of an action in the primary dict
# why would we feel positive?
# player played well and we
## started them
## drafted them (in the x round)
## picked them up
## claimed them off waivers


# if we feel negatively about a player, it's because of an action in the negative
# why would we feel negative
# player played poorly and we
## started them
## spent a waiver claim on them
# or player played well and we
## benched them
## dropped them
PLAYER_ACTIONS = {
  "positive": {
    "pickup": {
      "past": ["picked up", "swooped", "grabbed", "snagged", "added"],
      "future": ["pick up", "swoop", "grab", "snag", "add"],
    },
    "start": {
      "past": ["started", "flexed"],
      "future": ["start", "flex"]
    },
    "claim": {
      "past": ["claimed"],
      "future": ["put in a claim for"]
    }
  },
  "negative": {
    "bench": {
      "past": ["benched", "didn't start", "sat"],
      "future": ["bench", "sit"]
    },
    "drop": {
      "past": ["dropped"],
      "future": ["drop"]
    },
    "claim": {
      "past": ["used my waiver on", "spent my top waiver on"],
      "future": ["use my waiver on", "spend my waiver on"]
    },
    "start": {
      "past": ["started", "flexed"],
      "future": ["start", "flex"]
    },
  }
}