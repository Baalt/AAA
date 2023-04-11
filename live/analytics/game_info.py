class GameInfo:
    def __init__(self, live_data, smart_data, statistic_name: str,
                 rate_direction: str, live_total,
                 live_coeff, smart_total, key):
        self.live_data = live_data
        self.smart_data = smart_data
        self.statistic_name = statistic_name
        self.rate_direction = rate_direction

        self.live_total = live_total
        self.live_coeff = live_coeff
        self.smart_total = smart_total
        self.key = key

    def get_correction_key(self):
        return f"""
    Correction Key: {self.smart_data['smart_data']['game_number']}_{self.statistic_name}_{self.key}_"""

    def get_game_info(self):
        try:
            return f"""########## LIVE ##########
          Live League: {self.live_data['league']}
      Smart League: {self.smart_data['smart_data']['league']}

           Live Teams: {self.live_data['team1_name']} - {self.live_data['team2_name']}
       Smart Teams: {self.smart_data['smart_data']['team1_name']} - {self.smart_data['smart_data']['team2_name']}

                      TIME: {self.live_data['match_time']}
                  SCORE: {self.live_data['match_score']}
         RED CARDS: {self.live_data['red cards']}

    Statistic Name: {self.statistic_name}
                       Live: {self.live_total} {self.rate_direction}
                    Smart: {self.smart_total} {self.rate_direction}
           Coefficient: {self.live_coeff}"""
        except KeyError as e:
            print(f"GameInfo.get_game_info Key Error: {e} is missing in the data.")
            return None
