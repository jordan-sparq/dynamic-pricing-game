import random
import time
from flask import Flask, render_template, jsonify, request
import customers as customers
import logging
from urllib.parse import unquote
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_plot", methods=["GET"])
def update_plot():
    price_set = float(request.args.get("mean_value", 0))
    xData = json.loads(request.args.get("xData", "[]"))  # Parse xData from request parameters
    yData = json.loads(request.args.get("yData", "[]")) 
    print(xData)
    # global mean_value
    x = time.time() * 1000  # x-axis: time in milliseconds. Doesnt get used
    
    n_customers = customers.n_customers(10, 100)
    max_prices = customers.maximum_prices(n_customers, max_price_mean=50, max_price_std=3)

    ### get reward from the user's input
    reward = customers.revenue_per_look(n_customers, price_set, max_prices)
    ### get reward from the RL price
    # need to create qtable if first iteration. Can implement a counter in index.html and request it here?
    if price_set == 0:
        reward = 0
    # z is a placeholder to put the RL reward
    return jsonify(x=x, y=reward, z=1)

@app.route("/set_mean/<float:mean>", methods=["GET"])
def set_mean(mean):
    global mean_value
    mean_value = mean
    return "Mean set to {:.2f}".format(mean)

@app.route("/execute_python_code", methods=["POST"])
def execute_python_code():
    data = request.json  # Parse JSON data from request body
    code = unquote(data.get("code"))
    xData = data.get("xData")
    yData = data.get("yData")
    prices = data.get("prices")
    print("code = ", code)
    print("xData = ", xData)
    print("yData = ", yData)
    # run python code
    func_dict = {}
    exec(code, globals())
    print("executed code")
    for name, obj in globals().items():
        if name == 'set_price':
            # Add functions to the dictionary
            func_dict['set_price'] = obj

    result = func_dict['set_price'](xData, yData, prices)
    # Do something with the code
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
