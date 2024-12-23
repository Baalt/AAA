class GameInfo:
    def __init__(self, live_data, smart_data, statistic_name: str,
                 rate_direction: str, live_total, live_coeff, smart_total):
        self.live_data = live_data
        self.smart_data = smart_data
        self.statistic_name = statistic_name
        self.rate_direction = rate_direction
        self.smart_data_dct = smart_data['smart_data'][statistic_name]
        self.live_total = live_total
        self.live_coeff = live_coeff
        self.smart_total = smart_total

    def get_correction_key(self):
        return f"\n{self.smart_data['smart_data']['game_number']}➠{self.statistic_name}➠ref_15_under_t➠"

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
         RED CARDS: {self.live_data['red_score']}

    Statistic Name: {self.statistic_name}
                       Live: {self.live_total} {self.rate_direction}
                    Smart: {self.smart_total} {self.rate_direction}
           Coefficient: {self.live_coeff}

Ref15 T%: {self.smart_data_dct['ref_15_under_t']} - {self.smart_data_dct['ref_15_under_p']:03.2f}% 
RefAllT%: {self.smart_data_dct['ref_all_under_t']} - {self.smart_data_dct['ref_all_under_p']:03.2f}% {self.smart_data_dct['ref_all_len']:03d} | {self.smart_data_dct['ref_avg']}

CYear T%: {self.smart_data_dct['ref_15_under_t']} - {self.smart_data_dct['under_year_p']:03.2f}% {self.smart_data_dct['len_under_year_1']:03d} | {self.smart_data_dct['len_under_year_2']:03d}
CSim  T%: {self.smart_data_dct['ref_15_under_t']} - {self.smart_data_dct['under_sim_p']:03.2f}% {self.smart_data_dct['len_under_sim_1']:03d} | {self.smart_data_dct['len_under_sim_2']:03d}
CL15  T%: {self.smart_data_dct['ref_15_under_t']} - {self.smart_data_dct['under_20_p']:03.2f}% {self.smart_data_dct['len_under_20_1']:03d} | {self.smart_data_dct['len_under_20_2']:03d}
CHA   T%: {self.smart_data_dct['ref_15_under_t']} - {self.smart_data_dct['under_ha_p']:03.2f}% {self.smart_data_dct['len_under_ha_1']:03d} | {self.smart_data_dct['len_under_ha_2']:03d}
----------------  + 1   ----------------
Ref15 T%: {self.smart_data_dct['ref_15_under_t1']} - {self.smart_data_dct['ref_15_under_p1']:03.2f}% 
RefAllT%: {self.smart_data_dct['ref_all_under_t1']} - {self.smart_data_dct['ref_all_under_p1']:03.2f}% 

CYear T%: {self.smart_data_dct['ref_15_under_t1']} - {self.smart_data_dct['under_year_p1']:03.2f}% 
CSim  T%: {self.smart_data_dct['ref_15_under_t1']} - {self.smart_data_dct['under_sim_p1']:03.2f}% 
CL15  T%: {self.smart_data_dct['ref_15_under_t1']} - {self.smart_data_dct['under_20_p1']:03.2f}% 
CHA   T%: {self.smart_data_dct['ref_15_under_t1']} - {self.smart_data_dct['under_ha_p1']:03.2f}% 
"""
        except KeyError as e:
            print(f"GameInfo.get_game_info Key Error: {e} is missing in the data.")


class Info:
    def __init__(self, live_data, message):
        self.live_data = live_data
        self.message = message

    def get_game_info(self):
        try:
            return f"""
########## LIVE ##########
 
LL: {self.live_data['league']}
LT: {self.live_data['team1_name']} - {self.live_data['team2_name']}

                      TIME: {self.live_data['match_time']}
                  SCORE: {self.live_data['match_score']}
    
{self.message}
        """
        except KeyError as e:
            print(f"GameInfo.get_game_info Key Error: {e} is missing in the data.")
            return None


class ScoreInfo:
    def __init__(self, live_data):
        self.live_data = live_data

    def get_game_info(self):
        try:
            return f"""
    ########## LIVE ##########

    LL: {self.live_data['league']}
    LT: {self.live_data['team1_name']} - {self.live_data['team2_name']}

                          TIME: {self.live_data['match_time']}
                      SCORE: {self.live_data['match_score']}
             RED CARDS: {self.live_data['red_score']}

          YELLOW OR FOULS UNDER BY SCORE!!!
            """
        except KeyError as e:
            print(f"GameInfo.get_game_info Key Error: {e} is missing in the data.")
            return None
