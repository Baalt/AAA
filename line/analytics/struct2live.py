from line.analytics.live_utils.total import LiveTotalCalculation
from line.analytics.live_utils.ind_total import LiveIndividualCalculation
from line.analytics.live_utils.handicap import LiveHandicapCalculation
from line.analytics.structures import HomeDataStructure, AwayDataStructure
from utils.stat_switcher import stats_dict


class FromStructureToLiveDict(LiveTotalCalculation,
                              LiveIndividualCalculation,
                              LiveHandicapCalculation):
    def add_referee_data(self, statistic_name):
        try:
            print(self.referee_data[statistic_name]['first_15_elements'])
            referee_15 = self.referee_data[statistic_name]['first_15_elements']
            referee_all = self.referee_data[statistic_name]['all']
            under_15, over_15 = self.total_calculation(seq=referee_15, percent=93)
            under_all, over_all = self.total_calculation(seq=referee_all, percent=93)
            if statistic_name == 'ЖК':
                self.main_data['yellow_reff_15_under'] = under_15
                self.main_data['yellow_reff_15_over'] = over_15
                self.main_data['yellow_reff_all_under'] = under_all
                self.main_data['yellow_reff_all_over'] = over_all
                print('Вроде как сохранил данные о рефери ЖК')
            elif statistic_name == 'Фолы':
                self.main_data['foul_reff_15_under'] = under_15
                self.main_data['foul_reff_15_over'] = over_15
                self.main_data['foul_reff_all_under'] = under_all
                self.main_data['foul_reff_all_over'] = over_all
                print('Вроде как сохранил данные о рефери Фолы')
        except KeyError as e:
            print('FromStructureToLiveDict.add_referee_data()Error: ', e)

    def calculate(self,
                  home_structure: HomeDataStructure,
                  away_structure: AwayDataStructure,
                  statistic_name: str):

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

        if statistic_name == 'ЖК' or statistic_name == 'Фолы':
            print('statistic_name ', statistic_name)
            self.add_referee_data(statistic_name=statistic_name)

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
        return self.main_data

    def big_data_structures_validation(self,
                                       home_structure: HomeDataStructure,
                                       away_structure: AwayDataStructure):

        big_data_home_structure = len(home_structure.big_data_total_current_home_in_home_away_games)
        big_data_away_structure = len(away_structure.big_data_total_current_away_in_home_away_games)
        if big_data_home_structure > 49 and big_data_away_structure > 49:
            return True

    def percent_define(self, statistic_name):
        # if statistic_name in ['yellow cards']:
        #     return 96
        return 96.6
