import random
import time
from flask import Flask, render_template, jsonify, request
from RestrictedPython import compile_restricted_function, safe_builtins, compile_restricted
from RestrictedPython.Eval import default_guarded_getiter
import customers as customers
import logging
from urllib.parse import unquote
import json

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

# Define a whitelist of safe modules/packages
safe_modules_whitelist = {
    'math': None,   # Allow the entire math module
    'random': None, # Allow the entire random module
    'numpy': None,
    'pandas': None,
    # Add other safe modules/packages as needed
}

@app.route("/execute_python_code", methods=["POST"])
def execute_python_code():
    data = request.json  # Parse JSON data from request body
    code = data.get("code")
    xData = data.get("xData")
    yData = data.get("yData")
    prices = data.get("prices")
    
    # Remove print statements from the code
    code = remove_print_statements(code)

    # Compile the restricted function
    restricted_code = compile_restricted(code, '<inline>', 'exec')
    
    # Execute the restricted function in a sandboxed environment
    try:
        restricted_globals = {'__builtins__': safe_builtins}
        restricted_globals.update(safe_modules_whitelist) # Extend with safe modules whitelist
        exec(restricted_code, restricted_globals)
        
        if 'set_price' in restricted_globals:
            set_price_func = restricted_globals['set_price']
            result = set_price_func(xData, yData, prices)
            return jsonify({"result": result})
        else:
            return jsonify({"error": "Function 'set_price' not found in the code"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def remove_print_statements(code):
    # Remove print statements from the code
    lines = code.split('\n')
    code_lines = []
    for line in lines:
        if 'print' not in line:
            code_lines.append(line)
    return '\n'.join(code_lines)

if __name__ == "__main__":
    app.run(debug=True)
