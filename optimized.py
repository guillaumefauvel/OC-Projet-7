from pprint import pprint
import math
import numpy as np


available_stocks = {"A1": [20, 5],
                    "A2": [30, 10],
                    "A3": [50, 15],
                    "A4": [70, 20],
                    "A5": [60, 17]}


def common_step(dict_of_stocks):
    # Fonction qui récupère le pas commun des actions, 2 ou 1 par exemple

    costs_lists = np.array([x[1][0] for x in dict_of_stocks.items()])
    gcd = np.gcd.reduce(costs_lists)
    return int(gcd)


# Variable qui détermine la capacité max du panier
# Fonction qui vérifie si l'élément peut tenir dans une capacité donné
# Adapter ROI en fonction du prix


def optimized_algo():
    step = common_step(available_stocks)
    number_of_steps = int(70/step)
    table = [[[0, [], []] for index in range(number_of_steps)] for value in range(len(available_stocks))]

    for value, index in zip(available_stocks, range(0, len(available_stocks))):
        for cell, ref in zip(table[index], range(1, len(table[index])+1)):

            stock_cost = available_stocks[value][0]
            previous_performance = table[index - 1][ref - 1][0]
            previous_stocks_names = table[index - 1][ref - 1][2]
            stock_performance = available_stocks[value][1]
            cost_equality = (stock_cost == (ref * step))

            # If the stock cost suits the cell prerequisites and if the performance is better update the cell
            if (stock_cost <= ref*step) and (previous_performance < stock_performance):
                if cost_equality == 0:
                    table[index][ref - 1][1] = (ref*step)-stock_cost
                table[index][ref - 1][0] = stock_performance
                table[index][ref - 1][2].append(value)

            # Else, enter the old values
            else:
                table[index][ref - 1][0] = previous_performance
                if previous_stocks_names:
                    table[index][ref - 1][2].append(previous_stocks_names[0])

                if cost_equality == 0:
                    table[index][ref - 1][1] = (ref*step)-stock_cost

    for value in table:
        print(value)


optimized_algo()
