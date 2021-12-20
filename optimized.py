from pprint import pprint
import math
import numpy as np


available_stocks = {"A1": [20, 5],
                    "A2": [30, 10],
                    "A3": [50, 15],
                    "A4": [70, 20],
                    "A5": [60, 17]}


def common_step(dict_of_stocks):
    # Get the greatest common divisor
    # Arg : A dictionnary of stocks where the first value correspond to the cost
    # Return : An int, the GCD

    costs_lists = np.array([x[1][0] for x in dict_of_stocks.items()])
    gcd = np.gcd.reduce(costs_lists)
    return int(gcd)

# Adapt the performance to the ROI/cost

def optimized_algo():
    step = common_step(available_stocks)
    number_of_steps = int(80/step)
    table = [[[0, [], []] for index in range(number_of_steps)] for value in range(len(available_stocks))]

    for stock_name, row in zip(available_stocks, range(0, len(available_stocks))):
        for cell, ref in zip(table[row], range(1, len(table[row])+1)):

            stock_cost = available_stocks[stock_name][0]
            stock_performance = available_stocks[stock_name][1]

            previous_stock_ref = table[row - 1][ref - 1]
            previous_stock_cost = previous_stock_ref[1]

            previous_performance = previous_stock_ref[0]
            previous_stocks_names = previous_stock_ref[2]

            credit_available = step * ref

            # If the stock cost suits the cell prerequisites and if the performance is better update the cell
            if (stock_cost <= credit_available) and (previous_performance < stock_performance):
                table[row][ref - 1][0] = stock_performance
                table[row][ref - 1][1] = stock_cost
                table[row][ref - 1][2].append(stock_name)

                credit_available -= stock_cost

            # Else, enter the old values
            else:
                table[row][ref - 1][0] = previous_performance
                table[row][ref - 1][1] = previous_stock_cost
                if previous_stocks_names:
                    table[row][ref - 1][2].append(previous_stocks_names[0])

            # If there is enough credit left, fill the remaining space with others stocks



    for value in table:
        print(value)


optimized_algo()
