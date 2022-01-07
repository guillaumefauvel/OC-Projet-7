from datetime import datetime
from itertools import combinations
import operator

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
                if float(listed_line[1]) > 0:
                    stock_dict[listed_line[0]] = float(listed_line[1]), float(listed_line[2])
            except ValueError:
                pass

    stock_dict = dict(sorted(stock_dict.items(), key=operator.itemgetter(1), reverse=True))

    return stock_dict


def get_limit(reference_dict, max_credit):
    """ Get the range for the combinations generator
        Args : The sorted stocks dict, The maximum total cost of a combination (included)
        Return : The minimum lenght, The maximum lenght"""

    total = 0
    minimum_value = 0
    for value in reference_dict:
        if total <= max_credit:
            total += reference_dict[value][0]
            minimum_value += 1

    reversed_dict = dict(sorted(reference_dict.items(), key=operator.itemgetter(1), reverse=False))

    total = 0
    maximum_value = 0
    for value in reversed_dict:
        if total <= max_credit:
            total += reversed_dict[value][0]
            maximum_value += 1

    return minimum_value, maximum_value


def perfomance_counter(dict_of_stocks, reference_dict, credit):
    """ Compute the total of a given combination
        Args : The combination to compute, The dict that contains stocks reference cost and performance
        Return : The ROI, The combination reference"""


    overall_added_value = 0

    for value in dict_of_stocks:
        cost = reference_dict[value][0]
        performance = reference_dict[value][1]
        added_value = cost*(performance*0.01)
        overall_added_value += added_value

    return overall_added_value, dict_of_stocks


def cost_counter(selected_stocks, reference_dict):
    """ Compute the cost of a given combination
        Args : The combination to compute, The dict that contains stocks reference cost and performance
        Return : The total cost
    """

    total_weight = 0
    for value in selected_stocks:
        total_weight += reference_dict[value][0]

    return total_weight


def bruteforce(reference_dict, max_cost):
    """ Print the best combination
    Arg : A sorted dict of stocks, The cost limit """
    start_time = datetime.now()

    min_length, max_lenght = get_limit(reference_dict, max_cost)
    best_score = 0
    best_combination = []

    for lenght in range(min_length, max_lenght+1):
        combi = combinations(reference_dict, lenght)
        for value in combi:
            if cost_counter(value, reference_dict) <= max_cost:

                score, combination = perfomance_counter(value, reference_dict, max_cost)
                if score > best_score:
                    best_score = score
                    best_combination = combination

    return_on_investment = round(best_score / max_cost, 4)*100
    total_cost = cost_counter(best_combination, reference_dict)
    total_runtime = datetime.now()-start_time

    return return_on_investment, best_score, total_cost, best_combination, total_runtime


def main():
    sorted_dict = (stock_sorter("stocks.csv"))
    return_on_investment, best_score, total_cost, best_combination, total_runtime = bruteforce(sorted_dict, CAPITAL)

    print(f"\nLe meilleur ROI possible avec {CAPITAL} de crédit est de {round(return_on_investment, 4)}%,"
          f" soit {round(best_score,4)}e de gains.")
    print(f"Le coût total est de {total_cost}e.")
    print(f"\nIl est obtenu avec la combinaison suivante : {', '.join(best_combination)}")
    print(f"\nL'opération a été effectué en {total_runtime}")

main()