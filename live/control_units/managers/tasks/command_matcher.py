from utils.stat_switcher import exclude_list

class FootballTeamsComparison:
    def compare_teams(self, live_team_1, live_team_2, smart_team_1, smart_team_2):
        live_teams = [live_team_1, live_team_2]
        smart_teams = [smart_team_1, smart_team_2]

        for i in range(2):
            smart_team = smart_teams[i]
            live_team = live_teams[i]

            # Split the team names into words
            smart_words = [word for word in smart_team.split() if
                           len(word) > 4 and word.lower() not in exclude_list]
            live_words = [word for word in live_team.split() if
                          len(word) > 4 and word.lower() not in exclude_list]

            # Compare the teams based on their names
            if any((word.lower() in live_team.lower()) for word in smart_words) or \
                    any((word.lower() in smart_team.lower()) for word in live_words):
                return True
