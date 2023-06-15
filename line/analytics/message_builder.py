class KushMessageBuilder:
    def __init__(self, statistic_name: str, league_name: str, big_match_data: dict, big_data_percent: float,
                 last_year_percent: float, similar_percent_low: float, similar_percent_high: float,
                 last_20_percent: float, last_12_percent: float, last_8_percent: float, last_4_percent: float,
                 coefficients: dict, coeff_total: float, coeff_value: float, rate_direction: str, category: str,
                 big_data_kush_by_rate: float, last_year_kush_by_rate,
                 similar_kush_by_rate_low: float, similar_kush_by_rate_high: float,
                 last_20_kush_by_rate: float, last_12_kush_by_rate: float,
                 last_8_kush_by_rate: float, last_4_kush_by_rate: float,
                 big_data_current_percent: float, big_data_opposing_percent: float,
                 last_year_current_percent: float, last_year_opposing_percent: float,
                 similar_current_percent_low: float, similar_opposing_percent_low: float,
                 similar_current_percent_high: float, similar_opposing_percent_high: float,
                 last_20_current_percent: float, last_20_opposing_percent: float,
                 last_12_current_percent: float, last_12_opposing_percent: float,
                 last_8_current_percent: float, last_8_opposing_percent: float,
                 last_4_current_percent: float, last_4_opposing_percent: float):
        self.statistic_name = statistic_name or ''
        self.league_name = league_name or ''

        self.big_data_percent = big_data_percent
        self.last_year_percent = last_year_percent
        self.similar_percent_low = similar_percent_low
        self.similar_percent_high = similar_percent_high
        self.last_20_percent = last_20_percent
        self.last_12_home_away_percent = last_12_percent
        self.last_8_percent = last_8_percent
        self.last_4_percent = last_4_percent

        self.big_match_data = big_match_data or {}
        self.coeff_total = coeff_total or 0
        self.coeff_value = coeff_value or 0
        self.rate_direction = rate_direction or ''
        self.category = category or ''
        self.coefficients = coefficients or {}

        self.big_data_kush_by_rate = big_data_kush_by_rate or 0
        self.last_year_kush_by_rate = last_year_kush_by_rate or 0
        self.similar_kush_by_rate_low = similar_kush_by_rate_low or 0
        self.similar_kush_by_rate_high = similar_kush_by_rate_high or 0
        self.last_20_kush_by_rate = last_20_kush_by_rate or 0
        self.last_12_kush_by_rate = last_12_kush_by_rate or 0
        self.last_8_kush_by_rate = last_8_kush_by_rate or 0
        self.last_4_kush_by_rate = last_4_kush_by_rate or 0

        self.big_data_current = big_data_current_percent
        self.big_data_opposing = big_data_opposing_percent
        self.last_year_current = last_year_current_percent
        self.last_year_opposing = last_year_opposing_percent
        self.similar_current_low = similar_current_percent_low
        self.similar_opposing_low = similar_opposing_percent_low
        self.similar_current_high = similar_current_percent_high
        self.similar_opposing_high = similar_opposing_percent_high
        self.last_20_current = last_20_current_percent
        self.last_20_opposing = last_20_opposing_percent
        self.last_12_current = last_12_current_percent
        self.last_12_opposing = last_12_opposing_percent
        self.last_8_current = last_8_current_percent
        self.last_8_opposing = last_8_opposing_percent
        self.last_4_current = last_4_current_percent
        self.last_4_opposing = last_4_opposing_percent

    def get_message(self):
        return f"""         
########## LINE ##########

__League: {self.league_name}
ST Teams: {self.big_match_data['home_command_name']} - {self.big_match_data['away_command_name']}
Category: {self.category}
        
StatName: {self.statistic_name}
RateType: {'Part for combine rate' if float(self.coeff_value) < 1.683 else 'Single rate'}
_____Bet: {self.coeff_total} {self.rate_direction}  
____Coeff: {self.coeff_value}
    
Big Data: {self.big_data_kush_by_rate:3.2f} kush
LastYear: {self.last_year_kush_by_rate:3.2f} kush
SimlLow: {self.similar_kush_by_rate_low:3.2f} kush
SimiHigh: {self.similar_kush_by_rate_high:3.2f} kush
_____L15: {self.last_20_kush_by_rate:3.2f} kush
L10___HA: {self.last_12_kush_by_rate:3.2f} kush
_____L10: {self.last_8_kush_by_rate:3.2f} kush
______L5: {self.last_4_kush_by_rate:3.2f} kush 
    
Big Data: {self.big_data_current:3.2f} __ {self.big_data_opposing:3.2f} __ {self.big_data_percent:3.2f}%
LastYear: {self.last_year_current:3.2f} __ {self.last_year_opposing:3.2f} __ {self.last_year_percent:3.2f}%
SimlLow: {self.similar_current_low:3.2f} __ {self.similar_opposing_low:3.2f} __ {self.similar_percent_low:3.2f}%
SimiHigh: {self.similar_current_high:3.2f} __ {self.similar_opposing_high:3.2f} __ {self.similar_percent_high:3.2f}%
_____L15: {self.last_20_current:3.2f} __ {self.last_20_opposing:3.2f} __ {self.last_20_percent:3.2f}%
L10__HA: {self.last_12_current:3.2f} __ {self.last_12_opposing:3.2f}  __  {self.last_12_home_away_percent:3.2f}%
_____L10: {self.last_8_current:3.2f} __ {self.last_8_opposing:3.2f} __ {self.last_8_percent:3.2f}%
______L5: {self.last_4_current:3.2f} __ {self.last_4_opposing:3.2f} __ {self.last_4_percent:3.2f}%"""


class ExpressMessageBuilder:
    def __init__(self, statistic_name: str, league_name: str, big_match_data: dict, big_data_percent: float,
                 last_year_percent: float, similar_percent_low: float, similar_percent_high: float,
                 last_20_percent: float, last_12_percent: float, last_8_percent: float, last_4_percent: float,
                 coefficients: dict, coeff_total: float, coeff_value: float, rate_direction: str, category: str,
                 big_data_current_percent: float, big_data_opposing_percent: float,
                 last_year_current_percent: float, last_year_opposing_percent: float,
                 similar_current_percent_low: float, similar_opposing_percent_low: float,
                 similar_current_percent_high: float, similar_opposing_percent_high: float,
                 last_20_current_percent: float, last_20_opposing_percent: float,
                 last_12_current_percent: float, last_12_opposing_percent: float,
                 last_8_current_percent: float, last_8_opposing_percent: float,
                 last_4_current_percent: float, last_4_opposing_percent: float):
        self.statistic_name = statistic_name or ''
        self.league_name = league_name or ''

        self.big_data_percent = big_data_percent
        self.last_year_percent = last_year_percent
        self.similar_percent_low = similar_percent_low
        self.similar_percent_high = similar_percent_high
        self.last_20_percent = last_20_percent
        self.last_12_home_away_percent = last_12_percent
        self.last_8_percent = last_8_percent
        self.last_4_percent = last_4_percent

        self.big_match_data = big_match_data or {}
        self.coeff_total = coeff_total or 0
        self.coeff_value = coeff_value or 0
        self.rate_direction = rate_direction or ''
        self.category = category or ''
        self.coefficients = coefficients or {}

        self.big_data_current = big_data_current_percent
        self.big_data_opposing = big_data_opposing_percent
        self.last_year_current = last_year_current_percent
        self.last_year_opposing = last_year_opposing_percent
        self.similar_current_low = similar_current_percent_low
        self.similar_opposing_low = similar_opposing_percent_low
        self.similar_current_high = similar_current_percent_high
        self.similar_opposing_high = similar_opposing_percent_high
        self.last_20_current = last_20_current_percent
        self.last_20_opposing = last_20_opposing_percent
        self.last_12_current = last_12_current_percent
        self.last_12_opposing = last_12_opposing_percent
        self.last_8_current = last_8_current_percent
        self.last_8_opposing = last_8_opposing_percent
        self.last_4_current = last_4_current_percent
        self.last_4_opposing = last_4_opposing_percent

    def get_message(self):
        return f"""         
########## LINE ##########
__League: {self.league_name}
STTeams: {self.big_match_data['home_command_name']} - {self.big_match_data['away_command_name']}
Category: {self.category}

StatName: {self.statistic_name}
RateType: {'Part for combine rate' if float(self.coeff_value) < 1.683 else 'Single rate'}
______Bet: {self.coeff_total} {self.rate_direction}  
____Coeff: {self.coeff_value}

Big Data: {self.big_data_current:3.2f} __ {self.big_data_opposing:3.2f} __ {self.big_data_percent:3.2f}%
LastYear: {self.last_year_current:3.2f} __ {self.last_year_opposing:3.2f} __ {self.last_year_percent:3.2f}%
SimilLow: {self.similar_current_low:3.2f} __ {self.similar_opposing_low:3.2f} __ {self.similar_percent_low:3.2f}%
SimiHigh: {self.similar_current_high:3.2f} __ {self.similar_opposing_high:3.2f} __ {self.similar_percent_high:3.2f}%
_____L15: {self.last_20_current:3.2f} __ {self.last_20_opposing:3.2f} __ {self.last_20_percent:3.2f}%
L10__HA: {self.last_12_current:3.2f} __ {self.last_12_opposing:3.2f}  __  {self.last_12_home_away_percent:3.2f}%
_____L10: {self.last_8_current:3.2f} __ {self.last_8_opposing:3.2f} __ {self.last_8_percent:3.2f}%
______L5: {self.last_4_current:3.2f} __ {self.last_4_opposing:3.2f} __ {self.last_4_percent:3.2f}%"""


class RefereeMessageBuilder:
    def __init__(self, all_data, last15, average, length, coeff_total, rate_direction):
        self.all_data = all_data,
        self.last15 = last15,
        self.average = average,
        self.length = length,
        self.rate_direction = rate_direction
        self.coeff_total = float(coeff_total) * 2 if self.rate_direction.startswith(
            'Total_1') or self.rate_direction.startswith('Total_2') else coeff_total

    def get_message(self):
        return f"""         
######## REFEREE ########
______Bet: {self.coeff_total} {self.rate_direction} 
Big Data: {self.all_data:3.2f} %
_____L15: {self.last15:3.2f} %
 
allcount: {self.length}
__avg_15: {self.average}"""
