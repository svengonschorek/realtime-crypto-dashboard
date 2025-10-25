import os, sys, json

# Add the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..", "..", "..")
sys.path.append(os.path.abspath(project_root))

analysis_results = next(os.walk('./data/analysis_results'))

with open(f"{analysis_results[0]}/{analysis_results[2][-1]}", "r") as f:
    last_analysis = json.load(f)

def get_analysis_metadata():
    return json.loads(last_analysis)['analysis_metadata']

def get_market_structure():
    return json.loads(last_analysis)['market_structure']

def get_liquidity_zones():
    return json.loads(last_analysis)['liquidity']

def get_order_blocks():
    return json.loads(last_analysis)['order_blocks']

def get_fair_value_gaps():
    return json.loads(last_analysis)['fair_value_gaps']

def get_chart_patterns():
    return json.loads(last_analysis)['chart_patterns']

def get_trading_setups():
    return json.loads(last_analysis)['trading_setups']

def get_summary():
    return json.loads(last_analysis)['summary']
