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

    def all_played(self, lineup):
        for i in lineup:
            if i.slot_position != 'BE' and i.game_played < 100:
                return False
        return True

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

    def get_trophies(self, week=None):
        # Gets trophies for highest score, lowest score, closest score, and biggest win
        week = self.league.current_week - 1
        matchups = self.league.box_scores(week=week)
        low_score = 9999
        low_team_name = ''
        high_score = -1
        high_team_name = ''
        closest_score = 9999
        close_winner = ''
        close_loser = ''
        biggest_blowout = -1
        blown_out_team_name = ''
        ownerer_team_name = ''

        for i in matchups:
            if i.home_score > high_score:
                high_score = i.home_score
                high_team_name = i.home_team.team_name
            if i.home_score < low_score:
                low_score = i.home_score
                low_team_name = i.home_team.team_name
            if i.away_score > high_score:
                high_score = i.away_score
                high_team_name = i.away_team.team_name
            if i.away_score < low_score:
                low_score = i.away_score
                low_team_name = i.away_team.team_name
            if i.away_score - i.home_score != 0 and \
                    abs(i.away_score - i.home_score) < closest_score:
                closest_score = abs(i.away_score - i.home_score)
                if i.away_score - i.home_score < 0:
                    close_winner = i.home_team.team_name
                    close_loser = i.away_team.team_name
                else:
                    close_winner = i.away_team.team_name
                    close_loser = i.home_team.team_name
            if abs(i.away_score - i.home_score) > biggest_blowout:
                biggest_blowout = abs(i.away_score - i.home_score)
                if i.away_score - i.home_score < 0:
                    ownerer_team_name = i.home_team.team_name
                    blown_out_team_name = i.away_team.team_name
                else:
                    ownerer_team_name = i.away_team.team_name
                    blown_out_team_name = i.home_team.team_name

        low_score_str = ['Low score: %s with %.2f points' % (low_team_name, low_score)]
        high_score_str = ['High score: %s with %.2f points' % (high_team_name, high_score)]
        close_score_str = ['Nailbiter: %s barely beat %s by a margin of %.2f points' % (close_winner, close_loser, closest_score)]
        blowout_str = [
            'Wax of the week: %s blew out %s by a margin of %.2f points' % (ownerer_team_name, blown_out_team_name, biggest_blowout)]

        text = [f'Week {week} Trophies:'] + low_score_str + high_score_str + close_score_str + blowout_str
        return '\n'.join(text)

    def get_projected_scoreboard(self, week=None):
        # Gets current week's scoreboard projections
        box_scores = self.league.box_scores(week=week)
        score = ['%s %.2f - %.2f %s' % (i.home_team.team_abbrev, self.get_projected_total(i.home_lineup),
                                        self.get_projected_total(i.away_lineup), i.away_team.team_abbrev) for i in box_scores
                 if i.away_team]
        text = ['Approximate Projected Scores'] + score
        return '\n'.join(text)

    def get_projected_total(self, lineup):
        total_projected = 0
        for i in lineup:
            if i.slot_position != 'BE':
                if i.points != 0 or i.game_played > 0:
                    total_projected += i.points
                else:
                    total_projected += i.projected_points
        return total_projected

    def get_close_scores(self, week=None):
        # Gets current closest scores (15.999 points or closer)
        matchups = self.league.box_scores(week=week)
        score = []

        for i in matchups:
            if i.away_team:
                diffScore = i.away_score - i.home_score
                if (-16 < diffScore <= 0 and not self.all_played(i.away_lineup)) or (
                        0 <= diffScore < 16 and not self.all_played(i.home_lineup)):
                    score += ['%s %.2f - %.2f %s' % (i.home_team.team_abbrev, i.home_score,
                                                     i.away_score, i.away_team.team_abbrev)]
        if not score:
            return ('')
        text = ['Close Scores'] + score
        return '\n'.join(text)

    def scoreboard(self, week=None):
        scores = []
        scoreboard = self.league.box_scores(week=week)

        for matchup in scoreboard:
            scores += ['%s %.2f - %.2f %s' % (matchup.home_team.team_name, matchup.home_score, matchup.away_score, matchup.away_team.team_name)]
            text = ['Scoreboard'] + scores

        return '\n'.join(text)