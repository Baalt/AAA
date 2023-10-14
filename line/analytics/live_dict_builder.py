import os

from line.analytics.coefficient_analyzer import DataMetrics
from line.analytics.structures import FromDictToStructure
from line.analytics.struct2live import FromStructureToLiveDict
from line.control_units.filters.structure_valid import ValidStructureFilter
from utils.pickle_manager import PickleHandler
from utils.error import LiveDictBuilderError, ValidStructureError


class LiveDictBuilder(FromDictToStructure):
    def __init__(self, big_match_data: dict, last_year_data: dict, schedule_data: dict, all_league_data: dict,
                 coefficients, game_number: str, league_name: str, referee_data: dict,
                 big_matrix_data, year_matrix_data, telegram):
        self.big_match_data = big_match_data
        self.last_year_data = last_year_data
        self.all_league_data = all_league_data
        self.coefficients = coefficients
        self.league_name = league_name
        self.game_number = game_number
        self.referee_data = referee_data
        self.big_matrix_data = big_matrix_data
        self.year_matrix_data = year_matrix_data
        self.telegram = telegram
        self.data_file_name = f"data/{schedule_data['date']}_AllGamesData.pkl"
        self.data = {'lst': []}

    def add_similar_commands_in_list(self,
                                     statistic_name,
                                     main_home_command_name,
                                     main_away_command_name):
        command = None
        current_home_position = None
        current_away_position = None
        similar_home_commands_list_high = []
        similar_home_commands_list_low = []
        similar_away_commands_list_high = []
        similar_away_commands_list_low = []

        try:
            for command in self.all_league_data['current_season'][statistic_name]:
                if main_home_command_name in command['team_name'] or command['team_name'] in main_home_command_name:
                    current_home_position = int(command['team_position'])
                elif '(' in command['team_name'] and command['team_name'].split('(')[
                    0].strip() in main_home_command_name:
                    current_home_position = int(command['team_position'])

                if main_away_command_name in command['team_name'] or command['team_name'] in main_away_command_name:
                    current_away_position = int(command['team_position'])
                elif '(' in command['team_name'] and command['team_name'].split('(')[
                    0].strip() in main_away_command_name:
                    current_away_position = int(command['team_position'])

        except Exception as err:
            print(err)
            raise LiveDictBuilderError(f"""
        SIMILAR_COMMAND_ERROR !!!
        future/FromHistoryToRate.add_similar_commands_in_list

        HOME COMMAND NAME -- {main_home_command_name}
        AWAY COMMAND NAME -- {main_away_command_name}
        CURRENT COMMAND NAME -- {command if command['team_name'] else 'No commands in self.league_data[statistic_name]'}""")

        if current_home_position and current_away_position:
            for command in self.all_league_data['current_season'][statistic_name]:
                try:
                    current_position = int(command['team_position'])
                    if current_position in range(current_home_position - 3, current_home_position + 1):
                        similar_home_commands_list_high.append(command['team_name'])
                    if current_position in range(current_home_position, current_home_position + 4):
                        similar_home_commands_list_low.append(command['team_name'])
                    if current_position in range(current_away_position - 3, current_away_position + 1):
                        similar_away_commands_list_high.append(command['team_name'])
                    if current_position in range(current_away_position, current_away_position + 4):
                        similar_away_commands_list_low.append(command['team_name'])

                except IndexError:
                    return None

                except Exception as err:
                    print('FromHistoryToRate.add_similar_commands_in_list.ERROR: ', err)
                    return None

        self.similar_home_commands_list_high = similar_home_commands_list_high
        self.similar_home_commands_list_low = similar_home_commands_list_low
        self.similar_away_commands_list_high = similar_away_commands_list_high
        self.similar_away_commands_list_low = similar_away_commands_list_low

    async def run(self):
        main_home_command_name = self.big_match_data['home_command_name']
        main_away_command_name = self.big_match_data['away_command_name']

        self.add_similar_commands_in_list(statistic_name='goals',
                                          main_home_command_name=main_home_command_name,
                                          main_away_command_name=main_away_command_name)

        if self.similar_home_commands_list_high and self.similar_home_commands_list_low and \
                self.similar_away_commands_list_high and self.similar_away_commands_list_low:
            live_data_manager = FromStructureToLiveDict(
                league=self.league_name,
                team1_name=main_home_command_name,
                team2_name=main_away_command_name,
                game_number=self.game_number,
                referee_data=self.referee_data,
                big_matrix_data=self.big_matrix_data,
                year_matrix_data=self.year_matrix_data)

            for statistic_name in self.big_match_data:
                if not statistic_name.startswith('home') and not statistic_name.startswith('away'):
                    try:
                        home_structure = self.convert(
                            big_match_data=self.big_match_data,
                            last_year_data=self.last_year_data,
                            statistic_name=statistic_name,
                            main_command_name=main_home_command_name,
                            home_away_collection='home_collections',
                            similar_home_commands_list_high=self.similar_home_commands_list_high,
                            similar_home_commands_list_low=self.similar_home_commands_list_low,
                            similar_away_commands_list_high=self.similar_away_commands_list_high,
                            similar_away_commands_list_low=self.similar_away_commands_list_low)

                        away_structure = self.convert(
                            big_match_data=self.big_match_data,
                            last_year_data=self.last_year_data,
                            statistic_name=statistic_name,
                            main_command_name=main_away_command_name,
                            home_away_collection='away_collections',
                            similar_home_commands_list_high=self.similar_home_commands_list_high,
                            similar_home_commands_list_low=self.similar_home_commands_list_low,
                            similar_away_commands_list_high=self.similar_away_commands_list_high,
                            similar_away_commands_list_low=self.similar_away_commands_list_low)

                        try:
                            structures = ValidStructureFilter(home_structure=home_structure,
                                                              away_structure=away_structure)
                            structures.valid_and_create()
                            if structures.is_home_structure_valid() and structures.is_away_structure_valid():
                                is_valid = live_data_manager.big_data_structures_validation(
                                    home_structure=home_structure,
                                    away_structure=away_structure)
                                if is_valid:
                                    live_data_manager.calculate(
                                        home_structure=home_structure,
                                        away_structure=away_structure,
                                        statistic_name=statistic_name)

                                compare = DataMetrics(
                                    telegram=self.telegram,
                                    home_structure=structures.home_structure,
                                    away_structure=structures.away_structure,
                                    big_match_data=self.big_match_data,
                                    coefficients=self.coefficients,
                                    statistic_name=statistic_name,
                                    all_league_data=self.all_league_data,
                                    referee_data=self.referee_data,
                                    big_matrix_data=self.big_matrix_data,
                                    year_matrix_data=self.year_matrix_data)
                                await compare.search(statistic_name=statistic_name, full_league_name=self.league_name)


                        except ValidStructureError as err:
                            print('ValidStructureError: ', err)
                            continue

                        except KeyError as err:
                            print('FromHistoryToRate.run.ERROR: ', err)
                            continue

                    except AttributeError as err:
                        print('FromHistoryToRate.run.ERROR: ', err)
                        continue

            live_data = live_data_manager.get_data
            if live_data:
                pickle_handler = PickleHandler()
                self.load_data_from_file()
                self.data['lst'].append(live_data)
                pickle_handler.write_data(self.data, self.data_file_name)

    def load_data_from_file(self):
        if os.path.exists(self.data_file_name):
            pickle_handler = PickleHandler()
            self.data = pickle_handler.read_data(self.data_file_name)
