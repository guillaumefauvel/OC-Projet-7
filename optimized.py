import numpy as np
from datetime import datetime
import math

CAPITAL = 500


def stocks_dict_maker(csv_file):
    """ Make a sorted stock dict out of a csv file
        Arg : A csv file, with containing three columns, 1:reference, 2:cost, 3:stock_performance
        Return : A dict containing stocks infos """
    stock_dict = {}
    with open(csv_file, 'r', encoding="utf-8", ) as csv:
        index = 0
        for line in csv:
            listed_line = line.split(",")
            listed_line[2] = listed_line[2].split('\n')[0]
            try:
                cost = float(listed_line[1])
                performance = float(listed_line[2])
                if cost > 0:
                    added_performance = round(cost*performance/100, 3)
                    name = listed_line[0]
                    stock_dict[index] = cost, added_performance, name
                    index += 1

            except ValueError:
                pass

    return stock_dict


def to_int(array):
    """ Convert an array of number into integers with multiplication factor
    Arg : An array of number ( float, usually )
    Returns : An array of integers, the multiplication factor """

    longest_frac = 0

    for value in array:
        frac, whole = math.modf(value)
        whole_len = len(str(int(whole)))
        frac_len = len(str(value).replace('.', ''))-whole_len
        if frac_len > longest_frac:
            longest_frac = frac_len

    adjusted_array = []

    for value in array:
        adjusted_array.append(round(value * 10 ** longest_frac))

    return adjusted_array, longest_frac


def common_step(dict_of_stocks):
    """ Get the greatest common divisor in order to reduce the table
    Arg : A dictionnary of stocks where the first value correspond to the cost
    Return : The GCD ( Greatest Common Divisor ) """

    formated_dict = [dict_of_stocks[a][0] for a in dict_of_stocks]

    adjusted_array, coef = to_int(formated_dict)
    gcd = np.gcd.reduce(adjusted_array)/(10**coef)

    return gcd


def optimized_algo(stocks_dict, max_credit):
    """ Create a grid in order to have the best possible value for money
    Arg : A dictionnary of stocks ( key=index, v1=cost, v2=added_value, v3=stocks_reference )
    Return : the return on investment(float), added_value(float), total_cost(float),
             combinations (list), total_runtime(datetime object)"""

    start_time = datetime.now()

    step = common_step(stocks_dict)
    number_of_steps = int(max_credit/step)

    table = [[[0, [], 0] for index in range(number_of_steps+1)] for value in range(len(stocks_dict))]

    for stock, row in zip(stocks_dict, range(0, len(stocks_dict))):
        for column in range(len(table[row])):
            above_cell_perf = table[row - 1][column][0]

            if stocks_dict[stock][0] <= column*step:

                added_stock_cost = stocks_dict[stock][0]
                added_value = stocks_dict[stock][1]
                added_stock_name = stocks_dict[stock][2]

                without_last = table[row - 1][column - int(stocks_dict[stock][0] / step)][0]
                without_last_stock = table[row - 1][column - int(stocks_dict[stock][0] / step)][1]
                without_last_cost = table[row - 1][column - int(stocks_dict[stock][0] / step)][2]

                condition_one = (added_value + without_last) > above_cell_perf
                condition_two = (added_stock_cost + without_last_cost) <= column*step

                if condition_one and condition_two:
                    table[row][column][0] = added_value + without_last
                    table[row][column][1].extend(without_last_stock)
                    table[row][column][1].append(added_stock_name)
                    table[row][column][2] = added_stock_cost + without_last_cost

                else:
                    table[row][column] = table[row - 1][column]

            else:
                table[row][column] = table[row - 1][column]

    best_cell = table[len(stocks_dict)-1][number_of_steps]
    added_value, combinations, total_cost = best_cell
    return_on_investment = round(added_value / max_credit * 100, 4)

    total_cost = 0
    for stock in stocks_dict.values():
        if stock[2] in combinations:
            total_cost += stock[0]

    total_runtime = datetime.now()-start_time

    return return_on_investment, added_value, total_cost, combinations, total_runtime


def main():

    available_stocks = (stocks_dict_maker("série2.csv"))

    roi, added_value, total_cost, combinations, total_runtime = optimized_algo(available_stocks, CAPITAL)

    print(f"\nLe meilleur ROI possible avec {CAPITAL} de crédit est de {roi}%,"
          f" soit {round(added_value, 4)}e de gains.")
    print(f"Le coût total est de {total_cost}e.")
    print(f"\nIl est obtenu avec la combinaison suivante : \n{', '.join(combinations)}")
    print(f"\nL'opération a été effectué en {total_runtime}")


main()
