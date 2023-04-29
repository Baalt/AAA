from line.analytics.live_utils.total import LiveTotalCalculation
from line.analytics.live_utils.ind_total import LiveIndividualCalculation
from line.analytics.live_utils.handicap import LiveHandicapCalculation
from line.analytics.structures import HomeDataStructure, AwayDataStructure


class FromStructureToLiveDict(LiveTotalCalculation,
                              LiveIndividualCalculation,
                              LiveHandicapCalculation):
    def calculate(self, home_structure: HomeDataStructure,
                  away_structure: AwayDataStructure,
                  statistic_name: str):
        stats_dict = {
            'Голы': 'goals',
            'Угловые': 'corners',
            'ЖК': 'yellow cards',
            'Фолы': 'fouls',
            'Уд. в створ': 'shots on goal',
            'Офсайды': 'offsides',
            'Ауты': 'throw-ins',
            'Удары от ворот': 'goal kicks',
            'Удары': 'shots',
        }
        if statistic_name in stats_dict.keys():
            statistic_name = stats_dict[statistic_name]

        percent = self.percent_define(statistic_name=statistic_name)
        total = self.calculate_total_live_data(home_structure=home_structure,
                                               away_structure=away_structure,
                                               percent=percent)
        total_1 = self.calculate_individual_1_live_data(home_structure=home_structure,
                                                        away_structure=away_structure,
                                                        percent=percent)
        total_2 = self.calculate_individual_2_live_data(home_structure=home_structure,
                                                        away_structure=away_structure,
                                                        percent=percent)
        handicap_1 = self.calculate_handicap_1_live_data(home_structure=home_structure,
                                                         away_structure=away_structure,
                                                         percent=percent)
        handicap_2 = self.calculate_handicap_2_live_data(home_structure=home_structure,
                                                         away_structure=away_structure,
                                                         percent=percent)

        total_under, total_over = total
        total_1_under, total_1_over = total_1
        total_2_under, total_2_over = total_2

        self.add_live_data_to_dict(statistic_name=statistic_name,
                                   total_under=total_under, total_over=total_over,
                                   total_1_under=total_1_under, total_1_over=total_1_over,
                                   total_2_under=total_2_under, total_2_over=total_2_over,
                                   handicap_1=handicap_1, handicap_2=handicap_2)

    def add_live_data_to_dict(self, statistic_name,
                              total_under, total_over,
                              total_1_under, total_1_over,
                              total_2_under, total_2_over,
                              handicap_1, handicap_2):

        live_dict = {statistic_name: {'TU': total_under, 'TO': total_over,
                                      'TU_1': total_1_under, 'TO_1': total_1_over,
                                      'TU_2': total_2_under, 'TO_2': total_2_over,
                                      'H1': handicap_1, 'H2': handicap_2}}
        self.main_data.update(live_dict)

    @property
    def get_data(self):
        if len(self.main_data) > 4:
            return self.main_data

    def big_data_structures_validation(self,
                                       home_structure: HomeDataStructure,
                                       away_structure: AwayDataStructure):

        big_data_home_structure = len(home_structure.big_data_total_current_home_in_home_away_games)
        big_data_away_structure = len(away_structure.big_data_total_current_away_in_home_away_games)
        if big_data_home_structure > 49 and big_data_away_structure > 49:
            return True

    def percent_define(self, statistic_name):
        if statistic_name in ['goals', 'corners']:
            return 97
        return 90
