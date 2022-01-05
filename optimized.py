import numpy as np
from datetime import datetime
import csv


CAPITAL = 500


def stocks_dict(csv_file):
    """ Make a sorted stock dict out of a csv file
        Arg : A csv file, with containing three columns, 1:reference, 2:cost, 3:stock_performance
        Return : A sorted dict in non ascending order """
    stock_dict = {}
    with open(csv_file, 'r', encoding="utf-8", ) as csv:
        index = 0
        for line in csv:
            listed_line = line.split(",")
            listed_line[2] = listed_line[2].split('\n')[0]

            try:
                cost = float(listed_line[1])
                performance = float(listed_line[2])
                added_performance = round(cost*performance/100,3)
                name = listed_line[0]
                stock_dict[index] = cost, added_performance, name
                index += 1

            except ValueError:
                pass

    return stock_dict

def common_step(dict_of_stocks):
    # Get the greatest common divisor in order to reduce the table
    # Arg : A dictionnary of stocks where the first value correspond to the cost
    # Return : An int, the GCD

    formated_dict = [dict_of_stocks[a][0] for a in dict_of_stocks]

    def to_int(array, coef):
        signal = True
        for value in array:
            if not value.is_integer():

                return to_int(np.array(array)*10, coef+1)
        if signal is True:
            reference_list = [int(a) for a in array]

            return [reference_list, coef]

    adjusted_array, coef = to_int(formated_dict, 0)
    gcd = np.gcd.reduce(adjusted_array)/(10**coef)

    return gcd


def optimized_algo(stocks_dict):

    start_time = datetime.now()

    step = common_step(stocks_dict)
    number_of_steps = int(CAPITAL/step)
    table = [[[0, []] for index in range(number_of_steps+1)] for value in range(len(stocks_dict))]

    for stock, row in zip(stocks_dict, range(0, len(stocks_dict))):

        for column in range(len(table[row])):

            above_cell_perf = table[row - 1][column][0]
            above_cell_stocks = table[row - 1][column][1]

            if stocks_dict[stock][0] <= column*step:

                if column*step - stocks_dict[stock][0] >= 0:

                    added_value = stocks_dict[stock][1]
                    added_stock_name = stocks_dict[stock][2]

                    without_last = table[row - 1][column - int(stocks_dict[stock][0] / step)][0]
                    without_last_stock = table[row - 1][column - int(stocks_dict[stock][0] / step)][1]

                    if (added_value + without_last) > above_cell_perf:
                        table[row][column][0] = added_value + without_last
                        for stock_ref in without_last_stock:
                            table[row][column][1].append(stock_ref)
                        table[row][column][1].append(added_stock_name)

                    else:
                        table[row][column][0] = above_cell_perf
                        table[row][column][1] = above_cell_stocks

                else:
                    table[row][column][0] = above_cell_perf

            else:
                table[row][column] = table[row - 1][column]


    best_cell = table[len(stocks_dict)-1][number_of_steps]
    added_value, combinations = best_cell
    return_on_investment = round(added_value / CAPITAL * 100,3)

    print(f"\nLe meilleur ROI possible avec {CAPITAL} de crédit est de {return_on_investment}%."
          f"\nIl est obtenu avec la combinaison suivante : {', '.join(combinations)}")
    print(f"\nL'opération a été effectué en {datetime.now()-start_time}")


available_stocks = (stocks_dict("stocks.csv"))
optimized_algo(available_stocks)

