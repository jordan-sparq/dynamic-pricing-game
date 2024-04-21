import random
import time
from flask import Flask, render_template, jsonify
from flask import request
import customers as customers
import logging

app = Flask(__name__)

# Global variables for data
mean_value = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_plot", methods=["GET"])
def update_plot():
    price_set = float(request.args.get("mean_value", 0))
    # global mean_value
    x = time.time() * 1000  # x-axis: time in milliseconds. Doesnt get used

    n_customers = customers.n_customers(10, 100)
    max_prices = customers.maximum_prices(n_customers, max_price_mean=50, max_price_std=3)

    ### get reward from the user's input
    reward = customers.revenue_per_look(n_customers, price_set, max_prices)
    ### get reward from the RL price
    # need to create qtable if first iteration. Can implement a counter in index.html and request it here?

    # z is a placeholder to put the RL reward
    return jsonify(x=x, y=reward, z=1)

@app.route("/set_mean/<float:mean>", methods=["GET"])
def set_mean(mean):
    global mean_value
    mean_value = mean
    return "Mean set to {:.2f}".format(mean)

if __name__ == "__main__":
    app.run(debug=True)
