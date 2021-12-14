from datetime import datetime
from itertools import combinations


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

    stock_dict = {k: v for k, v in sorted(stock_dict.items(), key=lambda item: item[1][1], reverse=True)}

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

    reversed_dict = {k: v for k, v in sorted(reference_dict.items(), key=lambda item: item[1][1], reverse=False)}
    total = 0
    maximum_value = 0
    for value in reversed_dict:
        if total <= max_credit:
            total += reversed_dict[value][0]
            maximum_value += 1

    return minimum_value, maximum_value


def perfomance_counter(dict_of_stocks, reference_dict):
    """ Compute the total of a given combination
        Args : The combination to compute, The dict that contains stocks reference cost and performance
        Return : The ROI, The combination reference"""

    overall_cost = 0
    overall_added_value = 0

    for value in dict_of_stocks:
        cost = reference_dict[value][0]
        performance = reference_dict[value][1]
        added_value = cost*(performance*0.01)
        overall_added_value += added_value
        overall_cost += cost

    return_on_investment = ((round((overall_added_value + overall_cost) / overall_cost, 3))*100)-100

    return return_on_investment, dict_of_stocks


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
    Arg : The cost limit """

    min_length, max_lenght = get_limit(reference_dict, max_cost)
    best_score = 0
    best_combination = []

    start_time = datetime.now()
    for lenght in range(min_length, max_lenght+1):
        combi = list(combinations(reference_dict, lenght))
        for value in combi:
            if cost_counter(value, reference_dict) <= max_cost:
                score, combination = perfomance_counter(value, reference_dict)
                if score > best_score:
                    best_score = score
                    best_combination = combination
    print(datetime.now()-start_time)

    print(f"La meilleur score est {round(best_score, 4)}%")
    print(f"Voici la meilleur combinaisons {best_combination}")


sorted_dict = (stock_sorter("stocks.csv"))
bruteforce(sorted_dict, 500)
