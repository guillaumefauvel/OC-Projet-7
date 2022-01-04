import numpy as np
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
                cost = int(listed_line[1])
                performance = int(listed_line[2])
                added_performance = round(cost*performance/100,3)
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


def credit_left(credit, dict_reference):

    available_credit = credit
    for stock in dict_reference:
        start, end = stock.split("-")
        available_credit -= available_stocks[int(end)-1][0]

    return available_credit

def optimized_algo(stocks_dict):

    step = common_step(stocks_dict)
    number_of_steps = int(CAPITAL/step)
    table = [[[0, [], 0] for index in range(CAPITAL+1)] for value in range(len(stocks_dict))]

    for stock, row in zip(stocks_dict, range(0, len(stocks_dict))):
        for column in range(len(table[row])):

            above_cell_perf = table[row - 1][column][0]
            above_cell_stocks = table[row - 1][column][1]


            if row == 0 or column == 0:
                table[row][column][0] = 0

            elif stocks_dict[stock][0] <= column:

                if column - stocks_dict[stock][0] >= 0:

                    added_value = stocks_dict[stock][1]
                    added_stock_name = stocks_dict[stock][2]

                    without_last = table[row - 1][column - stocks_dict[stock][0]][0]
                    without_last_stock = table[row - 1][column - stocks_dict[stock][0]][1]

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

            table[row][column][2] = credit_left(column,table[row][column][1])

    with open('audit.csv', 'w', encoding="utf-8", newline='' ) as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow([x for x in range(0,CAPITAL+1)])
        # writer.writerow([x for x in range(step,CAPITAL+step,step)])
        for value in table:
            writer.writerow(value)


optimized_algo(available_stocks)

