from flask import Flask, render_template, request, jsonify
import random, time, datetime #, uuid
from heapSort import heapSortIterative

app = Flask(__name__)

item_id = 0
items = []
logs = []

def random_name():
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"
    name = ''.join(random.choice(consonants) + random.choice(vowels)
                   for _ in range(random.randint(2, 4)))
    return name.capitalize()

def random_item():
    global item_id
    item_id += 1
    cost = random.randint(100, 10000)
    discount = random.randint(0, 80)
    stock = random.randint(0, 500)
    final_cost = round(cost * (1 - discount / 100), 2)
    return {
        "id": item_id,
        "name": random_name(),
        "cost": cost,
        "discount": discount,
        "final_cost": final_cost,
        "stock": stock,
        "category": random.choice(["Tech", "Wear", "Home", "Misc"])
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = request.json
    items.pop(data['item_id'] - 1)
    return jsonify(success=True)

@app.route('/add_item', methods=['POST'])
def add_item():
    global item_id
    item_id += 1
    data = request.json
    data['id'] = item_id #str(uuid.uuid4())[:8]
    data['final_cost'] = round(float(data['cost']) * (1 - float(data['discount']) / 100), 2)
    data['cost'] = int(data['cost'])
    data['stock'] = int(data['stock'])
    data['discount'] = int(data['discount'])
    items.append(data)
    return jsonify(success=True)

@app.route('/add_random', methods=['POST'])
def add_random():
    items.append(random_item())
    return jsonify(success=True)

@app.route('/add_random_bulk', methods=['POST'])
def add_random_bulk():
    count = int(request.json.get('count', 10000))
    for _ in range(count):
        items.append(random_item())
    return jsonify(success=True)

@app.route('/randomize_order', methods=['POST'])
def randomize_order():
    random.shuffle(items)
    return jsonify(success=True)

@app.route('/sort', methods=['POST'])
def sort_items():
    req = request.json
    field = req['field']
    order = req['order']  # 'asc' or 'desc'
    reverse = (order == 'desc')

    start = time.perf_counter_ns()
    heapSortIterative(items, lambda x: x[field], reverse)
    elapsed = time.perf_counter_ns() - start

    elapsed /= 1000 * 1000

    log = {
        "field": field,
        "order": order,
        "count": len(items),
        "time": elapsed,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    }
    logs.insert(0, log)
    return jsonify(message=f"Sorted {len(items)} items by {field} ({order}) in {elapsed}ms",
                   logs=logs)

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
