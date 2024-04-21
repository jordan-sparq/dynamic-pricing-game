import random


def n_customers(min_num: int, max_num: int):
    """
    Return a random number of customers in a day between min_num and max_num

    :param min_num: minimum number of customers in a day
    :param max_num: maximum number of customers in a day

    :return: number of customers (int)
    """
    if min_num > max_num:
        min_num, max_num = max_num, min_num  # Swap the values if min_num is greater
    return random.randint(min_num, max_num)


def maximum_prices(n_customers: int, max_price_mean = 50, max_price_std = 10):
    """

    :param n_customers: number of customers in a day
    :param max_price_mean: mean price they are willing to pay
    :param max_price_std: standard deviation of max price

    :return: list of maximum prices
    """
    customer_prices = []
    for _ in range(n_customers):
        price = round(random.gauss(max_price_mean, max_price_std), 2)
        # Ensure that the generated price is non-negative
        price = max(price, 0)
        customer_prices.append(price)

    return customer_prices


def revenue_per_look(n_customers: int, price_set: float, max_prices: list[float], prob_purchase = 0.8):
    """
    revenue per look from the day

    :param n_customers: number of customers in a day
    :param price_set: price set by user
    :param max_prices: max prices for each customer
    :param prob_purchase: if the price is < max price, prob of purchase

    :return: revenue per look
    """
    total_revenue = []
    for i in range(n_customers):
        chance = random.random()
        if (chance <= prob_purchase) and (price_set <= max_prices[i]):
            # customer buys
            total_revenue.append(price_set)

    return sum(total_revenue) / n_customers

