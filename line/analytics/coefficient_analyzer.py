from line.analytics.line_utils.handicap import HandicapCatcher
from line.analytics.line_utils.ind_total import IndividualTotalCatcher
from line.analytics.line_utils.total import TotalCatcher


class DataMetrics(TotalCatcher,
                  IndividualTotalCatcher,
                  HandicapCatcher):
    async def search(self, statistic_name: str, full_league_name: str):
        try:
            await self.search_total_rate(statistic_name=statistic_name, league_name=full_league_name)
        except KeyError:
            pass
        try:
            await self.search_individual_1_total_rate(statistic_name=statistic_name, league_name=full_league_name)
        except KeyError:
            pass
        try:
            await self.search_individual_2_total_rate(statistic_name=statistic_name, league_name=full_league_name)
        except KeyError:
            pass
        try:
            await self.search_handicap_1_rate(statistic_name=statistic_name, league_name=full_league_name)
        except KeyError:
            pass
        try:
            await self.search_handicap_2_rate(statistic_name=statistic_name, league_name=full_league_name)
        except KeyError:
            pass
