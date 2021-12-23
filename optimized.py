from pprint import pprint
import math
import numpy as np

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
                cost = int(listed_line[1])
                performance = int(listed_line[2])
                added_performance = cost*performance/100
                name = listed_line[0]
                stock_dict[index] = cost, added_performance, name
                index += 1

            except ValueError:
                pass

    return stock_dict

available_stocks = (stocks_dict("stocks.csv"))


def common_step(dict_of_stocks):
    # Get the greatest common divisor
    # Arg : A dictionnary of stocks where the first value correspond to the cost
    # Return : An int, the GCD

    costs_lists = np.array([x[1][0] for x in dict_of_stocks.items()])
    gcd = np.gcd.reduce(costs_lists)
    return int(gcd)


def optimized_algo(stocks_dict):

    step = common_step(stocks_dict)
    number_of_steps = int(CAPITAL/step)
    table = [[[0, []] for index in range(number_of_steps)] for value in range(len(stocks_dict))]

    for stock, row in zip(stocks_dict, range(0, len(stocks_dict))):
        for column in range(1, len(table[row])):

            if row == 0 or column == 0:
                table[row][column][0] = 0

            elif stocks_dict[stock][0] <= column*step:

                back = 0
                added_value = stocks_dict[stock][1]
                without_last = table[row - 1][column - stocks_dict[stock - 1][0] - back][0]
                without_last_ref = table[row - 1][column - stocks_dict[stock - 1][0] - back][1]

                above_cell_roi = table[row - 1][column][0]

                if (added_value + without_last) > above_cell_roi:
                    table[row][column][0] = added_value + without_last
                    table[row][column][1] = table[row - 1][column - stocks_dict[stock - 1][0] - back][1]
                    table[row][column][1].append(stocks_dict[stock][2])

                else:
                    table[row][column][1] = table[row - 1][column][1]
                    table[row][column][0] = above_cell_roi

            else:
                table[row][column] = table[row - 1][column]

    print(stocks_dict)

    import csv
    with open('audit.csv', 'w', encoding="utf-8", newline='' ) as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow([x for x in range(step,CAPITAL+step,step)])
        for value in table:
            writer.writerow(value)



optimized_algo(available_stocks)


