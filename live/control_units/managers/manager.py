import os
import datetime
import time
from pprint import pprint

from bs4 import BeautifulSoup

from browser.browser import LiveChromeDriver, SmartChromeDriver
from line.control_units.managers.leagues_collector import AllLeaguesCollector
from line.control_units.scrapers.schedule_scraper import ScheduleScraper
from live.control_units.managers.schedule import ScheduleManager
from live.control_units.managers.web_crawler import WebCrawler
from toolz.pickle_manager import PickleHandler
from data import football_statistics_translation

from graph.match_stats_viz import MatchStatsVisualizer
from graph.teams_stats_viz import TeamsStatsVisualizer


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
    Correction Key: {self.smart_data['smart_data']['game_number']}_{self.statistic_name}_{self.key}
"""

    def get_game_info(self):
        try:
            return f"""
################ LIVE #################################################################
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


class SmartLiveCompare():
    def __init__(self, smart_data: dict, live_data: dict, league_data: dict):
        self.smart_data = smart_data
        self.live_data = live_data
        self.league_data = league_data

    def show_data(self):
        from pprint import pprint
        pprint(self.live_data['league'])

    def compare(self):
        for statistic in self.live_data:
            if statistic in football_statistics_translation.stats_dict.values():
                try:
                    smart_dct = self.smart_data['smart_data'][statistic]
                    total_under = smart_dct['TU']
                    total_over = smart_dct['TO']
                    total_1_under = smart_dct['TU_1']
                    total_1_over = smart_dct['TO_1']
                    total_2_under = smart_dct['TU_2']
                    total_2_over = smart_dct['TO_2']
                    handicap_1 = smart_dct['H1']
                    handicap_2 = smart_dct['H2']
                except KeyError:
                    continue

                self.__search_total(statistic=statistic,
                                    statistic_key='totals',
                                    total_under=total_under,
                                    total_over=total_over,
                                    rate_direction='total',
                                    key_under='TU',
                                    key_over='TO')

                self.__search_total(statistic=statistic,
                                    statistic_key='team1_totals',
                                    total_under=total_1_under,
                                    total_over=total_1_over,
                                    rate_direction='total_1',
                                    key_under='TU_1',
                                    key_over='TO_1')
                self.__search_total(statistic=statistic,
                                    statistic_key='team2_totals',
                                    total_under=total_2_under,
                                    total_over=total_2_over,
                                    rate_direction='total_2',
                                    key_under='TU_2',
                                    key_over='TO_2')

                self.__search_handicap(statistic=statistic,
                                       statistic_key='team1_handicaps',
                                       handicap=handicap_1,
                                       rate_direction='handicap_1',
                                       key_handicap='H1')
                self.__search_handicap(statistic=statistic,
                                       statistic_key='team2_handicaps',
                                       handicap=handicap_2,
                                       rate_direction='handicap_2',
                                       key_handicap='H2')

    def __search_total(self, statistic, statistic_key,
                       total_under, total_over,
                       rate_direction, key_under, key_over):
        try:
            coeff_box = self.live_data[statistic][statistic_key]
        except KeyError as e:
            print('SmartLiveCompare.search_total_engine coeff_box error: ', e)
            return

        for coeff_set in coeff_box:
            try:
                live_total = float(coeff_set['total_number'])
                coeff_under = float(coeff_set['coefficient_under'])
            except (KeyError, ValueError) as e:
                print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                continue
            if total_under:
                if live_total >= total_under and coeff_under > 1.65:
                    full_rate_direction = rate_direction + '_under'
                    info = GameInfo(
                        live_data=self.live_data,
                        smart_data=self.smart_data,
                        statistic_name=statistic,
                        rate_direction=full_rate_direction,
                        live_total=live_total,
                        live_coeff=coeff_under,
                        smart_total=total_under,
                        key=key_under)
                    self.delete_files_in_folder(folder_path='graph/data')
                    print(info.get_game_info())
                    print(info.get_correction_key())
                    MatchStatsVisualizer(data=self.live_data['match_stats']).plot_bar_chart()
                    current_viz = TeamsStatsVisualizer(
                        data=self.league_data[self.smart_data['smart_data']['league']]['current_season'],
                        team_name_1=self.smart_data['smart_data']['team1_name'],
                        team_name_2=self.smart_data['smart_data']['team2_name'])
                    current_viz.plot_points(
                        data_lst=self.league_data[self.smart_data['smart_data']['league']]['current_season']['goals'],
                        season='Current Season')
                    previous_viz = TeamsStatsVisualizer(
                        data=self.league_data[self.smart_data['smart_data']['league']]['previous_season'],
                        team_name_1=self.smart_data['smart_data']['team1_name'],
                        team_name_2=self.smart_data['smart_data']['team2_name'])
                    previous_viz.plot_points(
                        data_lst=self.league_data[self.smart_data['smart_data']['league']]['previous_season']['goals'],
                        season='Previous Season')
                    if key_under == 'TU':
                        current_viz.plot_team_stats(stat_key=statistic,
                                                    season='current_season',
                                                    sort_by='avg_overall_total')
                        previous_viz.plot_team_stats(stat_key=statistic,
                                                     season='previous_season',
                                                     sort_by='avg_overall_total')
                    else:
                        current_viz.plot_team_stats(stat_key=statistic,
                                                    season='current_season',
                                                    sort_by='avg_individual_team')
                        previous_viz.plot_team_stats(stat_key=statistic,
                                                     season='previous_season',
                                                     sort_by='avg_individual_team')
                    time.sleep(3)

            try:
                coeff_over = float(coeff_set['coefficient_over'])
            except KeyError as e:
                print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                continue

            if total_over:
                if live_total <= total_over and coeff_over > 1.7:
                    full_rate_direction = rate_direction + '_over'
                    info = GameInfo(
                        live_data=self.live_data,
                        smart_data=self.smart_data,
                        statistic_name=statistic,
                        rate_direction=full_rate_direction,
                        live_total=live_total,
                        live_coeff=coeff_over,
                        smart_total=total_over,
                        key=key_over)
                    self.delete_files_in_folder(folder_path='graph/data')
                    print(info.get_game_info())
                    print(info.get_correction_key())
                    MatchStatsVisualizer(data=self.live_data['match_stats']).plot_bar_chart()
                    current_viz = TeamsStatsVisualizer(
                        data=self.league_data[self.smart_data['smart_data']['league']]['current_season'],
                        team_name_1=self.smart_data['smart_data']['team1_name'],
                        team_name_2=self.smart_data['smart_data']['team2_name'])
                    current_viz.plot_points(
                        data_lst=self.league_data[self.smart_data['smart_data']['league']]['current_season']['goals'],
                        season='Current Season')
                    previous_viz = TeamsStatsVisualizer(
                        data=self.league_data[self.smart_data['smart_data']['league']]['previous_season'],
                        team_name_1=self.smart_data['smart_data']['team1_name'],
                        team_name_2=self.smart_data['smart_data']['team2_name'])
                    previous_viz.plot_points(
                        data_lst=self.league_data[self.smart_data['smart_data']['league']]['previous_season']['goals'],
                        season='Previous Season')
                    if key_under == 'TO':
                        current_viz.plot_team_stats(stat_key=statistic,
                                                    season='current_season',
                                                    sort_by='avg_overall_total')
                        previous_viz.plot_team_stats(stat_key=statistic,
                                                     season='previous_season',
                                                     sort_by='avg_overall_total')
                    else:
                        current_viz.plot_team_stats(stat_key=statistic,
                                                    season='current_season',
                                                    sort_by='avg_individual_team')
                        previous_viz.plot_team_stats(stat_key=statistic,
                                                     season='previous_season',
                                                     sort_by='avg_individual_team')

    def __search_handicap(self, statistic, statistic_key, handicap, rate_direction, key_handicap):
        try:
            coeff_box = self.live_data[statistic][statistic_key]
        except KeyError as e:
            print('SmartLiveCompare.search_handicap_engine coeff_box error: ', e)
            return

        for coeff_set in coeff_box:
            try:
                live_handicap = float(coeff_set['total_number'])
                coeff = float(coeff_set['coefficient'])
            except (KeyError, ValueError) as e:
                print('SmartLiveCompare.search_total_engine coeff_set error: ', e)
                continue

            if handicap:
                if live_handicap >= handicap and coeff > 1.65:
                    info = GameInfo(
                        live_data=self.live_data,
                        smart_data=self.smart_data,
                        statistic_name=statistic,
                        live_total=live_handicap,
                        live_coeff=coeff,
                        smart_total=handicap,
                        rate_direction=rate_direction,
                        key=key_handicap)
                    self.delete_files_in_folder(folder_path='graph/data')
                    print(info.get_game_info())
                    print(info.get_correction_key())
                    MatchStatsVisualizer(data=self.live_data['match_stats']).plot_bar_chart()
                    current_viz = TeamsStatsVisualizer(
                        data=self.league_data[self.smart_data['smart_data']['league']]['current_season'],
                        team_name_1=self.smart_data['smart_data']['team1_name'],
                        team_name_2=self.smart_data['smart_data']['team2_name'])
                    current_viz.plot_points(
                        data_lst=self.league_data[self.smart_data['smart_data']['league']]['current_season']['goals'],
                        season='Current Season')
                    current_viz.plot_team_stats(stat_key=statistic,
                                                season='current_season',
                                                sort_by='avg_individual_team')
                    previous_viz = TeamsStatsVisualizer(
                        data=self.league_data[self.smart_data['smart_data']['league']]['previous_season'],
                        team_name_1=self.smart_data['smart_data']['team1_name'],
                        team_name_2=self.smart_data['smart_data']['team2_name'])
                    previous_viz.plot_points(
                        data_lst=self.league_data[self.smart_data['smart_data']['league']]['previous_season']['goals'],
                        season='Previous Season')
                    previous_viz.plot_team_stats(stat_key=statistic,
                                                 season='previous_season',
                                                 sort_by='avg_individual_team')

    def delete_files_in_folder(self, folder_path):
        """
        Deletes all files in the specified folder.
        """
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    driver = LiveChromeDriver()
    driver.maximize_window()
    driver.open_page('https://www.fon.bet/')

    leagues_dct = PickleHandler().read_data(path_to_file='data/08.04_AllLeaguesData.pkl')
    smart_dict = PickleHandler().read_data(path_to_file='data/08.04_AllTeamsData.pkl')
    browser = ScheduleManager(smart_dict=smart_dict)
    full_smart_dict = browser.run()
    from data.test_data import smrt, lv

    slc = SmartLiveCompare(smart_data=smrt, live_data=lv, league_data=leagues_dct)
    slc.compare()

    pprint(lv['league'])
    now = datetime.datetime.now()
    while True:
        now_plus_delta = now + datetime.timedelta(minutes=10)
        browser = ScheduleManager(smart_dict=smart_dict)
        full_smart_dict = browser.run()
        operator = WebCrawler(driver=browser.get_driver(), smart_data=full_smart_dict)
        while now_plus_delta > now:
            operator.run_crawler()
            now = datetime.datetime.now()

    # driver = LiveChromeDriver()
    # driver.maximize_window()
    # driver.open_page('https://www.fon.bet/')
    #
    # soup = BeautifulSoup(driver.get_page_html(), 'lxml')
    # scraper = RealTimeGameScraper()
    # scraper.collect_stats(soup=soup, match_stat='corners', total_text='Total corners',
    #                       team_total_text='Team totals corners',
    #                       handicap_text='Сorners handicap')
    # scraper.scrape_match_time(soup=soup)
    # scraper.scrape_league(soup=soup)
    # scraper.scrape_team_names(soup=soup)
    # scraper.scrape_match_score(soup=soup)
    # scraper.scrape_red_cards(soup=soup)
    # scraper.show_game_info()
