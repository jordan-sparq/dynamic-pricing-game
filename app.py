import random
import time
from flask import Flask, render_template, jsonify, request
import customers as customers
import logging
from urllib.parse import unquote
import json
import subprocess

app = Flask(__name__, static_folder='static/')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_plot", methods=["GET"])
def update_plot():
    # read real time data from app
    price_set = float(request.args.get("mean_value", 0))
    xData = json.loads(request.args.get("xData", "[]"))  # Parse xData from request parameters
    yData = json.loads(request.args.get("yData", "[]")) 

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
    return jsonify(x=x, y=reward, n_customers=n_customers)

@app.route("/set_mean/<float:mean>", methods=["GET"])
def set_mean(mean):
    global mean_value
    mean_value = mean
    return "Mean set to {:.2f}".format(mean)

# @app.route("/execute_python_code", methods=["POST"])
# def execute_python_code():
#     data = request.json  # Parse JSON data from request body
#     code = unquote(data.get("code"))
#     xData = data.get("xData")
#     yData = data.get("yData")
#     prices = data.get("prices")
#     print("code = ", code)
#     print("xData = ", xData)
#     print("yData = ", yData)
#     # run python code
#     func_dict = {}
#     exec(code, globals())
#     print("executed code")
#     for name, obj in globals().items():
#         if name == 'set_price':
#             # Add functions to the dictionary
#             func_dict['set_price'] = obj

#     result = func_dict['set_price'](xData, yData, prices)
#     # Do something with the code
#     return jsonify({"result": result})

@app.route('/execute_python_code', methods=['POST'])
def execute_python_code():
    import os
    import sys

    # Add the directory containing the PyPy executable to the PATH
    pypy_path = "/Users/jordanpalmer/Downloads/pypy3.10-v7.3.16-macos_arm64/bin/pypy3"  # Replace this with the actual path to PyPy
    os.environ["PATH"] += os.pathsep + pypy_path

    # Get the Python code from the request
    code = request.json.get('code', '')
    
    try:
        # Execute Python code using PyPy
        result = subprocess.run(['pypy3', '-c', code], capture_output=True, text=True)
        output = result.stdout
        success = True
    except Exception as e:
        output = str(e)
        success = False

    # Return the result as JSON
    return jsonify({'output': output, 'success': success})

if __name__ == "__main__":
    app.run(debug=True)
