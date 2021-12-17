from pprint import pprint
import math
import numpy as np


available_stocks = {"Action-1":[20,5],
                    "Action-2":[30,10],
                    "Action-3":[50,15],
                    "Action-4":[70,20],
                    "Action-5":[60,17]}

# Fonction qui récupère le pas commun des actions, 2 ou 1 par exemple
def common_step(dict_of_stocks):
    costs_lists = np.array([x[1][0] for x in available_stocks.items()])
    gcd = np.gcd.reduce(costs_lists)
    return int(gcd)

# Variable qui détermine la capacité max du panier
# Fonction qui vérifie si l'élément peut tenir dans une capacité donné

# Reminder  - int(70/common_step(available_stocks))
number_of_steps = 70

table = [[0 for index in range(number_of_steps)] for value in range(len(available_stocks))]

for value, index in zip(available_stocks,range(0,len(available_stocks))):
    for cell, ref in zip(table[index], range(1,len(table[index])+1)):
        ## ref is equal to the slot size
        stock_cost = available_stocks[value][0]
        previous_cost = table[-index][-ref]
        stock_performance = available_stocks[value][1]
        table[index][ref - 1] = table[index-1][ref - 1]

        if (stock_cost <= ref) and (previous_cost <= stock_performance):
            table[index][ref - 1] = stock_performance


for value in table:
    print(value)


