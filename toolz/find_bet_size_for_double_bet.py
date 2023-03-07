def calculate_bets_and_coeff(coeff_1: float, coeff_2: float, bet_1: str, bet_2: str, rate: float = 10000):
    bet_size_1 = rate / coeff_1
    bet_size_2 = rate - bet_size_1
    bet_win_1 = bet_size_1 * coeff_1
    bet_win_2 = bet_size_2 * coeff_2
    coeff = (bet_win_2 + bet_win_1) / rate

    print(f"""
    Для ставок на общую сумму {rate} разбиваем на две части {round(bet_size_1, 2)} и {round(bet_size_2, 2)} с коэффициентами {coeff_1} и {coeff_2}:")
    выигрыш составит {round(bet_win_1, 2)} на {bet_1} и {round(bet_win_2, 2)} на {bet_2},")
    а общая выплата составит {round(bet_win_1 + bet_win_2, 2)}.")
    Общий коэффициент для этой комбинации ставок: {round(coeff, 2)}.""")


if __name__ == '__main__':
    calculate_bets_and_coeff(coeff_1=0, coeff_2=0, bet_1='', bet_2='', rate=10000)
