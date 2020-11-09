import math
import random

from espn_api.football import League


POSSIBLE_DRIFTS = []
POSSIBILITIES = {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 4, 7: 4, 8: 4, 9: 4, 10: 3, 11: 3, 12: 3, 13: 3, 14: 2, 15: 2, 16: 2,
                 17: 1, 18: 1, 19: 1, 20: 1}

for k, v in POSSIBILITIES.items():
    POSSIBLE_DRIFTS += [k] * v


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

    def weekly_finish(self, week, team=None):
        ''' Returns the rank of a team based on the weekly score of a team for a given week. '''
        ranks = {}
        for box in self.league.box_scores(week=week):
            ranks[box.away_team] = box.away_score
            ranks[box.home_team] = box.home_score

        sorted_ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}

        if team:
            return list(sorted_ranks.keys()).index(team) + 1
        return sorted_ranks

    def final_standings(self):
        final_records = []
        results = self.simulate_season()
        for team in self.league.teams:
            team_dict = results[team]
            final_records.append(team_dict)

        standings = sorted(final_records, key=lambda i: (i['wins'], i['points_scored']), reverse=True)

        printed_standings = ['{}. {} ({} - {}) {} points scored'.format(
            count, team["name"], team["wins"], team["losses"], round(team["points_scored"], 2)
        ) for count, team in enumerate(standings, 1)]
        text = ['Projected final standings'] + printed_standings
        return '\n'.join(text)

    def simulate_season(self):
        """
        This function simulates the remaining matchups for the season, based on each team's average points
        scored (with some accounting for drift). These results are added to the team's current matchup results.
        """
        results = {
            team: {
                'name': team.team_name,
                'wins': team.wins,
                'losses': team.losses,
                'points_scored': team.points_for
            } for team in self.league.teams
        }

        for week in range(self.league.current_week, 13):
            matchups = self.league.box_scores(week=week)

            for matchup in matchups:
                home_team = matchup.home_team
                average_home_points = self.get_average_points_scored(team=home_team)
                home_drift = random.choice(POSSIBLE_DRIFTS)
                home_points = average_home_points + home_drift if random.choice([1,2]) == 1 else average_home_points - home_drift
                results[home_team]['points_scored'] += home_points

                away_team = matchup.away_team
                average_away_points = self.get_average_points_scored(team=away_team)
                away_drift = random.choice(POSSIBLE_DRIFTS)
                away_points = average_away_points + away_drift if random.choice([1,2]) == 1 else average_away_points - away_drift
                results[away_team]['points_scored'] += away_points

                if home_points > away_points:
                    results[home_team]['wins'] += 1
                    results[away_team]['losses'] += 1
                else:
                    results[away_team]['wins'] += 1
                    results[home_team]['losses'] += 1

        return results

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

    def get_average_points_scored(self, team=None):
        if team:
            scores = [score for score in team.scores if score > 0]
            return round( sum(scores) / len(scores), 2)

        team_scores = [{
            "name": team.team_name,
            "scores": [score for score in team.scores if score > 0],
        } for team in self.league.teams ]

        for team in team_scores:
            team["average"] = round( sum(team["scores"]) / len(team["scores"]), 2)

        averages = ['%s - %s' % (i['name'], i['average']) for i in sorted(team_scores, key = lambda i: i['average'], reverse=True)]
        text = ['Average Points Scored:'] + averages
        return '\n'.join(text)

    def get_average_points_against(self):
        team_scores = [{
            "name": team.team_name,
            "scores": [score for score in team.scores if score > 0],
            "points_against": team.points_against
        } for team in self.league.teams ]

        for team in team_scores:
            team["average"] = round( team["points_against"] / len(team["scores"]), 2)

        averages = ['%s - %s' % (i['name'], i['average']) for i in sorted(team_scores, key = lambda i: i['average'], reverse=True)]
        text = ['Average Points Against:'] + averages
        return '\n'.join(text)

    def players_of_the_week(self, week=None):
        over_points = 0
        under_points = 0
        star = None
        bust = None

        if not week:
            week = self.league.current_week - 1

        boxes = self.league.box_scores(week=week)
        for box in boxes:
            box.home_lineup.extend(box.away_lineup)
            for player in box.home_lineup:
                player_diff = player.points - player.projected_points
                if player_diff > over_points:
                    over_points = player_diff
                    star = player
                elif player_diff < under_points:
                    under_points = player_diff
                    bust = player

        return star, bust

    def get_trophies(self, week=None):
        if not week:
            current_week_finished = True
            week = self.league.current_week
            boxes = self.league.box_scores(week=week)
            for box in boxes:
                if not self.all_played(box.away_lineup) or not self.all_played(box.home_lineup):
                    current_week_finished = False
                    break

            if not current_week_finished:
                week = self.league.current_week - 1

        print('fetching trophies for week {}'.format(week))

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
        high_score_str = ['High score: %s racked up %.2f points' % (high_team_name, high_score)]
        close_score_str = ['Fleece of the week: %s beat %s by %.2f points' % (close_winner, close_loser, closest_score)]
        blowout_str = [
            'Wax of the week: %s blew out %s by %.2f points' % (ownerer_team_name, blown_out_team_name, biggest_blowout)]

        star, bust = self.players_of_the_week(week)
        star_str = ['Thiqqy of the week: {} scored {} points ({} projected)'.format(star.name, star.points, star.projected_points)]
        bust_str = [
            'Pencil of the week: {} scored {} points ({} projected)'.format(bust.name, bust.points, bust.projected_points)]

        text = [f'Week {week} Trophies:'] + high_score_str + low_score_str + close_score_str + blowout_str + star_str + bust_str
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

    def scoreboard(self, week=None):
        scores = []
        scoreboard = self.league.box_scores(week=week)

        for matchup in scoreboard:
            scores += ['%s %.2f - %.2f %s' % (matchup.home_team.team_abbrev, matchup.home_score, matchup.away_score, matchup.away_team.team_abbrev)]
            text = ['Scoreboard'] + scores

        return '\n'.join(text)

    def matchups(self, week=None):
        scores = []
        scoreboard = self.league.scoreboard(week=week)

        for matchup in scoreboard:
            scores += ['%s vs. %s' % (matchup.home_team.team_abbrev, matchup.away_team.team_abbrev)]
            text = ['Week {} matchups'.format(week)] + scores

        return '\n'.join(text)

    def standings(self):
        scoreboard = self.league.box_scores(week=None)

        results = {
            team: {
                'name': team.team_name,
                'wins': team.wins,
                'losses': team.losses,
                'points_scored': team.points_for
            } for team in self.league.teams
        }

        for team in self.league.standings():
            matchup = next(m for m in scoreboard if m.home_team == team or m.away_team == team)
            print('score is {} - {}'.format(matchup.away_score, matchup.home_score))

            if matchup.away_score != matchup.home_score:
                print('score is not tied')
                if matchup.home_team == team:
                    results[team]['points_scored'] += matchup.home_score
                    if matchup.home_score > matchup.away_score:
                        results[team]['wins'] += 1
                    else:
                        results[team]['losses'] += 1
                else:
                    results[team]['points_scored'] += matchup.away_score
                    if matchup.away_score > matchup.home_score:
                        results[team]['wins'] += 1
                    else:
                        results[team]['losses'] += 1

        current_standings = []
        for team in self.league.teams:
            team_dict = results[team]
            current_standings.append(team_dict)

        standings = sorted(current_standings, key=lambda i: (i['wins'], i['points_scored']), reverse=True)

        printed_standings = ['{}. {} ({} - {}) {} points scored'.format(
            count, team["name"], team["wins"], team["losses"], round(team["points_scored"], 2)
        ) for count, team in enumerate(standings, 1)]
        text = ['Current standings'] + printed_standings
        return '\n'.join(text)

    def pickup(self):
        variety_intros = [
            'I like',
            'You could make a case for',
            'I\'m feeling good about',
            '',
            'This week I like',
        ]

        potentials = []
        for player in self.league.free_agents()[:20]:
            if player.position not in ['QB', 'D/ST'] and player.projected_points > 0:
                potentials.append(player)

        intro = random.choice(variety_intros)
        player = random.choice(potentials)
        message = '{} {}. Im thinking he scores {} against the {} defense'.format(
            intro, player.name, player.projected_points, player.pro_opponent)

        return message
