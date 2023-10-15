from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine


app = Flask(__name__)

# Google Cloud SQL (change this accordingly)
PASSWORD ="cloudrun"
PUBLIC_IP_ADDRESS ="35.195.82.82"
DBNAME ="items_data"
PROJECT_ID ="my-cloud-run-test-db2"
INSTANCE_NAME ="my-cloud-run-test-353212:europe-west1:my-cloud-run-test-db2"
SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}'
 
# configuration
app.config["SECRET_KEY"] = "SECRET"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

engine = create_engine(SQLALCHEMY_DATABASE_URI)


@app.route('/', methods=['GET'])
def home():
    with engine.connect() as connection:
        items = connection.execute(f"""SELECT id, text FROM items_data """).fetchall()
        print(items)
        return render_template("index.html", items = items)

@app.route('/add', methods=["POST"])
def add():
    item = request.form["item"]

    with engine.connect() as connection:
        connection.execute(f"""INSERT INTO items_data (text) VALUES ('{item}') """)
        return redirect(url_for('home'))

@app.route('/update/<id>', methods=['POST'])
def update(id):
    value = "updated"

    with engine.connect() as connection:
        connection.execute(f""" UPDATE item_data SET text = {value} WHERE id = {id} """)
        return redirect(url_for('home'))

@app.route('/delete/<this_id>', methods=["POST"])
def delete(this_id):
    
    with engine.connect() as connection:
        connection.execute( f""" DELETE FROM items_data WHERE id = {this_id}; """)
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
