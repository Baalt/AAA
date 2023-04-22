from selenium.webdriver.common.by import By


class SmartGameButtons:
    def __init__(self):
        self.browser = None

    @property
    def quantity_of_matches_buttons(self):
        QUANTITY_OF_MATCHES_INPUT_XPATH = '//input[@class="manual-howmuch-input"]'
        QUANTITY_OF_MATCHES_BUTTON_XPATH = '//div[contains(@class, "last_matches_limit-picker")]' \
                                           '/button[last()]'

        quantity_of_matches_input = self.browser.find_element(By.XPATH,
                                                              value=QUANTITY_OF_MATCHES_INPUT_XPATH)
        quantity_of_matches_button = self.browser.find_element(By.XPATH,
                                                               value=QUANTITY_OF_MATCHES_BUTTON_XPATH)

        return quantity_of_matches_input, quantity_of_matches_button

    @property
    def teams_season_buttons_all(self):
        SEASON_HOME_BUTTON_ALL_XPATH = '(//div[@id="teamsSeasons"])[1]/' \
                                       'button[last()]'
        SEASON_AWAY_BUTTON_ALL_XPATH = '(//div[@id="teamsSeasons"])[2]' \
                                       '/button[last()]'

        season_home_button_all = self.browser.find_element(By.XPATH,
                                                           value=SEASON_HOME_BUTTON_ALL_XPATH)
        season_away_button_all = self.browser.find_element(By.XPATH,
                                                           value=SEASON_AWAY_BUTTON_ALL_XPATH)

        return season_home_button_all, season_away_button_all

    def current_league_command_buttons(self, league: str):
        try:
            CURRENT_HOME_LEAGUE_XPATH = f'(//div[@id="refCompetitions"])[1]' \
                                        f'/button[normalize-space(text())=\'{league}\']'
            CURRENT_AWAY_LEAGUE_XPATH = f'(//div[@id="refCompetitions"])[2]' \
                                        f'/button[normalize-space(text())=\'{league}\']'

            current_league_home_command_button = self.browser.find_element(By.XPATH,
                                                                           value=CURRENT_HOME_LEAGUE_XPATH)
            current_league_away_command_button = self.browser.find_element(By.XPATH,
                                                                           value=CURRENT_AWAY_LEAGUE_XPATH)

            return current_league_home_command_button, current_league_away_command_button

        except:
            try:
                button_league = league.split()
                if len(button_league) > 1:
                    league = button_league[0].strip() + ' ' + button_league[1].strip()
                CURRENT_HOME_LEAGUE_XPATH = f'(//div[@id="refCompetitions"])[1]' \
                                            f'/button[normalize-space(text())=\'{league}\']'
                CURRENT_AWAY_LEAGUE_XPATH = f'(//div[@id="refCompetitions"])[2]' \
                                            f'/button[normalize-space(text())=\'{league}\']'
                current_league_home_command_button = self.browser.find_element(By.XPATH,
                                                                               value=CURRENT_HOME_LEAGUE_XPATH)
                current_league_away_command_button = self.browser.find_element(By.XPATH,
                                                                               value=CURRENT_AWAY_LEAGUE_XPATH)
                return current_league_home_command_button, current_league_away_command_button
            except:
                raise AttributeError

    @property
    def open_coefficient_button(self):
        XPATH = '//a[@class="nav-link accent-hvr cursor-pointer"]' \
                '/span[normalize-space(text())="Коэффициенты"]'
        button = self.browser.find_element(By.XPATH,
                                           value=XPATH)
        return button

    @property
    def coefficient_handicap_button(self):
        XPATH = '//div[contains(@class, "stat_format-picker")]' \
                '/button[normalize-space(text())="Исходы и форы"]'
        button = self.browser.find_element(By.XPATH,
                                           value=XPATH)
        return button
