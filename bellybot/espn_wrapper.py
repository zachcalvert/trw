from espn_api.football import League


class ESPNWrapper:

    def __init__(self):
        league_id = "832593"
        year = 2020
        swid = "{ADB2C88A-0CCD-4491-B8B7-4657E6A412FD}"
        espn_s2 = "AECvR2KuFAHIFNvXPmowC7LgFu4G2jj6tzWOaOd8xnX2wu3BaSy3Dogb5KU0KAiHu3xcqKzkMa%2FwbLIIzA4DMqtr%2FZF48Xs" \
                  "PMFyOGScz3xl0qO3ekELFD7qgY0qYdGbg%2BwbX0NntqxWwPaLPdrEaIc1vlXxehme7cbLRq6Uf5iP3f%2FpQvG51KexkEMJy6H" \
                  "c1C1zZxZ41fQ4EddVA%2BhaqQ9%2BADWELwT9hFbPFjoBxco8T%2FvSxS0TJFEqLiBUBfp%2F2RbE%3D"
        self.league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)

    def get_power_rankings(self, week=None):
        # power rankings requires an integer value, so this grabs the current week for that
        if not week:
            week = self.league.current_week
        # Gets current week's power rankings
        # Using 2 step dominance, as well as a combination of points scored and margin of victory.
        # It's weighted 80/15/5 respectively
        power_rankings = self.league.power_rankings(week=week)

        score = ['%s - %s' % (i[0], i[1].team_name) for i in power_rankings
                 if i]
        text = ['Power Rankings'] + score
        return '\n'.join(text)
