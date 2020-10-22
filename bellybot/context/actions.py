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
    "present": "is liking",
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
    "objects": ["it together", "off the W", "off an epic comeback"],
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
    "objects": ["me", "my ass"],
  },
  "fucking fleece": {
    "past": "fucking fleeced",
    "present": "is fucking fleecing",
    "future": "fleece",
    "objects": ["me", "my ass"],
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
    "objects": ["back down to earth", "inside me", "through", "to the pit", "back", "over"],
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
    "objects": ["my ass", "that ass", "nostalgic"],
  },
  "rip": {
    "past": "ripped",
    "present": "is ripping",
    "future": "rip",
    "objects": ["ass", "my borthole open"],
  },
  "spit": {
    "past": "spat",
    "present": "is spitting",
    "future": "spit",
    "objects": ["game", "rhymes"],
  },
  "be": {
    "past": "was being",
    "present": "is being",
    "future": "be",
    "objects": ["a bish", "a botch", "an ass", "a complete ass"],
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
    "objects": ["my ass"] + PLAYERS,
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
}