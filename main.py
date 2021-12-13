import csv


def stock_sorter(csv_file):
    """"""
    stock_dict = {}
    with open(csv_file, 'r', encoding="utf-8", ) as csv:
        for line in csv:
            list = line.split(",")
            list[2] = list[2].split('\n')[0]
            try:
                stock_dict[list[0]] = int(list[1]), int(list[2])
            except ValueError:
                pass

    stock_dict = {k: v for k, v in sorted(stock_dict.items(), key=lambda item: item[1][1], reverse=True)}

    return stock_dict


def stock_selection(stocks_dict):
    CREDIT = 500
    selected_stocks = {}
    for value in stocks_dict:
        cost = stocks_dict[value][0]
        performance = stocks_dict[value][1]
        if (CREDIT - cost) >= 0:
            selected_stocks[value] = cost, performance
            CREDIT -= cost
        else:
            pass
    return selected_stocks

def perfomance_counter(dict_of_stocks):

    overall_cost = 0
    overall_added_value = 0

    for value in dict_of_stocks:
        cost = dict_of_stocks[value][0]
        performance = dict_of_stocks[value][1]
        added_value = cost*(performance*0.01)
        overall_added_value += added_value
        overall_cost += cost

    return_on_investment = ((round((overall_added_value + overall_cost) / overall_cost, 3))*100)-100
    print(f"ROI : {round(return_on_investment,3)} %")

selected_stocks = stock_selection(stock_sorter("stocks.csv"))


for stock in selected_stocks:
    print(f"{stock} : {selected_stocks[stock][0]}, {selected_stocks[stock][1]} ")


perfomance_counter(selected_stocks)



