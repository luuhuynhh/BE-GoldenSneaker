import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app, origins='*', methods='*')

# Load environment variables from file
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            os.environ[key] = value

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '12121212')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'golden_sneaker')

mysql = MySQL(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response


# Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data['name']
    description = data['description']
    color = data['color']
    price = data['price']
    image = data['image']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO product (name, description, color, price, image) VALUES (%s, %s, %s, %s, %s)",
        (name, description, color, price, image)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Product created successfully'}), 201


# Get all products
@app.route('/products', methods=['GET'])
def get_all_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    cur.close()

    product_list = []
    for product in products:
        product_dict = {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'image': product[4],
            'color': product[5]
        }
        product_list.append(product_dict)

    return jsonify(product_list), 200


# Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if product:
        product_dict = {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': product[3],
            'image': product[4],
            'color': product[5]
        }
        return jsonify(product_dict), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


# Update a product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    name = data['name']
    description = data['description']
    color = data['color']
    price = data['price']
    image = data['image']

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE product SET name = %s, description = %s, color = %s, price = %s, image = %s WHERE id = %s",
        (name, description, color, price, image, product_id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Product updated successfully'}), 200


# Delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM product WHERE id = %s", (product_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Product deleted successfully'}), 200

# Create a new cart item


@app.route('/cart-items', methods=['POST'])
def create_cart_item():
    data = request.get_json()
    product_id = data['product_id']
    count = data['count']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO cart_item (product_id, count) VALUES (%s, %s)",
        (product_id, count)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Cart item created successfully'}), 201


# Get all cart items
@app.route('/cart', methods=['GET'])
def get_all_cart_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart_item")
    cart_items = cur.fetchall()
    cur.close()

    cart_item_list = []
    for cart_item in cart_items:
        cart_item_dict = {
            'id': cart_item[0],
            'count': cart_item[1],
            'product_id': cart_item[2]
        }
        cart_item_list.append(cart_item_dict)

    return jsonify(cart_item_list), 200


# Get a specific cart item by ID
@app.route('/cart-items/<int:cart_item_id>', methods=['GET'])
def get_cart_item(cart_item_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart_item WHERE id = %s", (cart_item_id,))
    cart_item = cur.fetchone()
    cur.close()

    if cart_item:
        cart_item_dict = {
            'id': cart_item[0],
            'count': cart_item[1],
            'product_id': cart_item[2]
        }
        return jsonify(cart_item_dict), 200
    else:
        return jsonify({'message': 'Cart item not found'}), 404


# Update a cart item
@app.route('/cart-items', methods=['PUT'])
def update_cart_item():
    data = request.get_json()
    product_id = data['product_id']
    count = data['count']

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE cart_item SET count = %s WHERE product_id = %s",
        (count, product_id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Cart item updated successfully'}), 200


# Delete a cart item
@app.route('/cart-items/<int:product_id>', methods=['DELETE'])
def delete_cart_item(product_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart_item WHERE product_id = %s", (product_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Cart item deleted successfully'}), 200


if __name__ == '__main__':
    app.run()
