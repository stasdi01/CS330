from flask import Flask, request, jsonify, render_template,  redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from config import create_app,db,mm
from model import User
import sqlite3
import csv
import os
import re
from datetime import datetime

app = create_app()
app.config["JWT_SECRET_KEY"] = "super-secret" 
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app, supports_credentials=True)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/register', methods=['POST'])
def register():
    data=request.json
    existing_user=User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message':'Email already registered please login'})
    hashed_password=bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )

    # Save the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json 
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Set the token to expire in 1 day
        print(type(user.id), type(user.username))
        access_token = create_access_token(identity=str(user.id), additional_claims={'username': user.username})
        return jsonify({'access_token': access_token})
    return jsonify({'message': 'Invalid credentials'}), 401

#test a protected route (ie route that can only be accessed by logged in user)
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        # Access the current user's identity from the JWT
        user_id = get_jwt_identity()  # This is the user.id from the token (as a string)
        user = User.query.get(int(user_id))  # Fetch user details from the database

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Include both id and username in the response
        response = jsonify({
            'message': 'This is a protected route',
            'user': {
                'id': user.id,
                'username': user.username
            }
        })
        return response
    except Exception as e:
        # Return detailed error if token verification fails
        print(f"Error: {str(e)}")  # Debugging
        return jsonify({'message': f'Token validation failed: {str(e)}'}), 422

# Fridge

DB_NAME = 'fridge.db'

def init_db_fridge():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS fridge_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            date_added TEXT,
            quantity TEXT,
            brand TEXT
        )
        ''')
        conn.commit()


def populate_db_from_csv():
    filename = "Item.csv"
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Make sure the file exists in the directory.")
        return


    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM fridge_items")
        if c.fetchone()[0] == 0: 
            print("Populating database from CSV...")
            with open(filename, "r", encoding="utf-8-sig") as csvfile: 
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames
                print(f"CSV Headers: {headers}")  
                if "ItemName" not in headers:
                    print("Error: 'ItemName' column not found in CSV.")
                    return
                for row in reader:
                    print(f"Row: {row}") 
                    c.execute("INSERT INTO fridge_items (item_name, date_added, quantity, brand) VALUES (?, ?, ?, ?)",
          (row["ItemName"], datetime.now().strftime("%Y-%m-%d"), "0 items", None))

            conn.commit()
        else:
            print("Database already populated.")


def get_fridge_items():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, item_name, date_added, quantity, brand FROM fridge_items")
        items = c.fetchall()
    return items




def add_fridge_item(item_name, date_added, quantity, brand=None):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO fridge_items (item_name, date_added, quantity, brand) VALUES (?, ?, ?, ?)",
                  (item_name, date_added, quantity, brand))
        conn.commit()


def load_items_from_csv():
    items = []
    filename = "Item.csv"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8-sig") as csvfile: 
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Loaded Item: {row['ItemName']}")  
                items.append(row["ItemName"])
    return items


def extract_keyword_and_types(items):
    result = {}
    for item in items:
        match = re.match(r"^(.*?)\s*\((.*?)\)", item)
        if match:
            keyword = match.group(1).strip()
            item_type = match.group(2).strip()
            result.setdefault(keyword, []).append(item_type)
        else:
            keyword = item.strip()
            result.setdefault(keyword, [])
    print("Extracted Data:", result)  
    return result


@app.route("/fridge", methods=["GET", "POST"])
def index_fridge():
    if request.method == "POST":
        item_name = request.form.get("item_name")
        brand = request.form.get("brand")
        quantity_type = request.form.get("quantityType")
        date_added = datetime.now().strftime("%Y-%m-%d") 
        if request.form.get("number"): 
            number_of_items = request.form.get("number")
            quantity = f"{number_of_items} items"
        elif quantity_type == "size":
            size_inch = request.form.get("sizeInch")
            size_cm = request.form.get("sizeCm")
            
            if size_inch and size_cm:
                quantity = f"{size_inch} inches //// {size_cm} cm"
            elif size_inch:
                quantity = f"{size_inch} inches"
            elif size_cm:
                quantity = f"{size_cm} cm"
            else:
                quantity = "No size specified"
        elif quantity_type == "weight":
            weight_kg = request.form.get("weightKg")
            weight_lb = request.form.get("weightLb")
            
            if weight_kg and weight_lb:
                quantity = f"{weight_kg} kg //// {weight_lb} lbs"
            elif weight_kg:
                quantity = f"{weight_kg} kg"
            elif weight_lb:
                quantity = f"{weight_lb} lbs"
            else:
                quantity = "No weight specified" 
        elif quantity_type == "liquid":
            liquid_gallon = request.form.get("liquidGallon")
            liquid_liter = request.form.get("liquidLiter")
            
            if liquid_gallon and liquid_liter:
                quantity = f"{liquid_gallon} gallon //// {liquid_liter} liter"
            elif liquid_gallon:
                quantity = f"{liquid_gallon} gallon"
            elif liquid_liter:
                quantity = f"{liquid_liter} liter"
            else:
                quantity = "No quantity specified"

        if item_name:
            add_fridge_item(item_name, date_added, quantity, brand)
        return redirect(url_for("index_fridge"))

    fridge_items = get_fridge_items()
    return render_template("fridge.html", fridge_items=fridge_items)

@app.route("/fridge/search_items_fridge", methods=["GET"])
def search_items_fridge():
    query = request.args.get("q", "").lower()
    all_items = load_items_from_csv()
    print("All Items:", all_items)
    keyword_types = extract_keyword_and_types(all_items)
    matching_items = {k: v for k, v in keyword_types.items() if query in k.lower()}

    return jsonify(matching_items)


@app.route("/fridge/edit_item/<int:item_id>", methods=["POST"])
def edit_item_fridge(item_id):
    new_quantity = request.form.get("quantity")
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE fridge_items SET quantity = ? WHERE id = ?", (new_quantity, item_id))
        conn.commit()
    return redirect(url_for("index_fridge"))


@app.route("/fridge/delete_item/<int:item_id>", methods=["POST"])
def delete_item_fridge(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM fridge_items WHERE id = ?", (item_id,))
        conn.commit()
    return redirect(url_for("index_fridge"))

def update_db_schema():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        try:
            c.execute("ALTER TABLE fridge_items ADD COLUMN brand TEXT")
        except sqlite3.OperationalError:
            pass  




if __name__ == '__main__':
    app.run(debug=True)
