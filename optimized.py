from pprint import pprint
import math
import numpy as np

CAPITAL = 500

def stock_sorter(csv_file):
    """ Make a sorted stock dict out of a csv file
        Arg : A csv file, with containing three columns, 1:reference, 2:cost, 3:stock_performance
        Return : A sorted dict in non ascending order """
    stock_dict = {}
    with open(csv_file, 'r', encoding="utf-8", ) as csv:
        for line in csv:
            listed_line = line.split(",")
            listed_line[2] = listed_line[2].split('\n')[0]
            try:
                stock_dict[listed_line[0]] = int(listed_line[1]), int(listed_line[2])
            except ValueError:
                pass

    stock_dict = {k: v for k, v in sorted(stock_dict.items(), key=lambda item: item[1][0], reverse=False)}

    return stock_dict

available_stocks = (stock_sorter("stocks.csv"))


def common_step(dict_of_stocks):
    # Get the greatest common divisor
    # Arg : A dictionnary of stocks where the first value correspond to the cost
    # Return : An int, the GCD

    costs_lists = np.array([x[1][0] for x in dict_of_stocks.items()])
    gcd = np.gcd.reduce(costs_lists)
    return int(gcd)

def optimized_algo():
    step = common_step(available_stocks)
    number_of_steps = int(CAPITAL/step)
    table = [[[0, 0, []] for index in range(number_of_steps)] for value in range(len(available_stocks))]

    for stock_name, row in zip(available_stocks, range(0, len(available_stocks))):
        for cell, ref in zip(table[row], range(1, len(table[row])+1)):

            current_cell = table[row][ref - 1]

            stock_cost = available_stocks[stock_name][0]
            stock_performance = available_stocks[stock_name][1]*stock_cost/100

            previous_stock_ref = table[row - 1][ref - 1]
            previous_stock_cost = previous_stock_ref[1]
            previous_performance = previous_stock_ref[0]
            previous_stocks_names = previous_stock_ref[2]

            credit_available = step * ref

            # If the stock cost suits the cell prerequisites and if the performance is better update the cell
            if (stock_cost <= credit_available) and (previous_performance < stock_performance):
                current_cell[0] = stock_performance
                current_cell[1] = stock_cost
                current_cell[2].append(stock_name)

            # Else, enter the old values
            else:
                current_cell[0] = previous_performance
                current_cell[1] = previous_stock_cost
                if previous_stocks_names:
                    current_cell[2].extend(previous_stocks_names)

            # If there is enough credit left, fill the remaining space with others stocks
            remaining_credit = credit_available - table[row][ref - 1][1]
            if remaining_credit > 0 and row != 0:
                max_allocation = (int(remaining_credit / step))
                while True:

                    additionnal_performance = table[row][max_allocation][0]
                    additionnal_cost = table[row][max_allocation][1]
                    additonnal_stocks_names = table[row][max_allocation][2]
                    duplicates = False

                    if len(current_cell[2]) > 1:
                        duplicates = any(stock in current_cell[2] for stock in additonnal_stocks_names)

                    elif len(current_cell[2]) == 1:
                        duplicates = current_cell[2][0] in additonnal_stocks_names

                    if not duplicates and additionnal_cost <= remaining_credit:
                        current_cell[0] += additionnal_performance
                        current_cell[1] += additionnal_cost
                        current_cell[2].extend(additonnal_stocks_names)
                        break

                    max_allocation -= 1
                    if max_allocation == 0:
                        break
    print(table[len(available_stocks)-1][number_of_steps-1])
    print((table[len(available_stocks)-1][number_of_steps-1][0]/CAPITAL)*100,"%")

    import csv
    with open('audit.csv', 'w', encoding="utf-8", newline='' ) as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow([x for x in range(step,CAPITAL+step,step)])
        for value in table:
            writer.writerow(value)


optimized_algo()
