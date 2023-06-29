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
        return f"\n{self.smart_data['smart_data']['game_number']}➠{self.statistic_name}➠{self.key}➠"

    def get_game_info(self):
        try:
            return f"""
########## LIVE ##########  
          
LL: {self.live_data['league']}
SL: {self.smart_data['smart_data']['league']}

LT: {self.live_data['team1_name']} - {self.live_data['team2_name']}
ST: {self.smart_data['smart_data']['team1_name']} - {self.smart_data['smart_data']['team2_name']}

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


class RedCardInfo:
    def __init__(self, live_data, smart_data, statistic_name: str):
        self.live_data = live_data
        self.smart_data = smart_data
        self.statistic_name = statistic_name

    def get_correction_key(self):
        return f"\n{self.smart_data['smart_data']['game_number']}➠red_card➠"

    def get_game_info(self):
        try:
            return f"""
########## LIVE ##########  

LL: {self.live_data['league']}
SL: {self.smart_data['smart_data']['league']}

LT: {self.live_data['team1_name']} - {self.live_data['team2_name']}
ST: {self.smart_data['smart_data']['team1_name']} - {self.smart_data['smart_data']['team2_name']}

                      TIME: {self.live_data['match_time']}
                  SCORE: {self.live_data['match_score']}
         RED CARDS: {self.live_data['red cards']}

    Statistic Name: {self.statistic_name}
RECEIVED A RED CARD IN THE MATCH!!!
TAKE A FOULS HANDICAP ON A TEAM WHICH DID NOT RECEIVE A RED CARD!"""
        except KeyError as e:
            print(f"GameInfo.get_game_info Key Error: {e} is missing in the data.")
            return None
