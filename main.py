import sqlite3
from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
import json


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home_page.html")


@app.route("/login_page")
def refer_to_login_page():
    return render_template("login.html")
    
@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route('/logout')
def index():
  return render_template('login.html')

@app.route("/search", methods=["POST"])
def search_engine():
    program = request.form.get('programSelect')
    search_term = request.form.get('search', '').strip()
    if search_term:
        get_search(search_term)
    data = []
    if program == "HTML":
        conn = sqlite3.connect("html.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            if search_term:
                query = 'SELECT search_object, definition FROM HTML_dict WHERE search_object LIKE ?'
                results = conn.execute(query, ('%' + search_term + '%',)).fetchall()
                data = [dict(row) for row in results]
            else:
                query = 'SELECT search_object, definition FROM HTML_dict'
                results = conn.execute(query).fetchall()
                data = [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"SQL query error: {e}")
        #finally:
        conn.close()
        
    if program == "CSS":
        conn = sqlite3.connect("css.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            if search_term:
                query = 'SELECT search_object, definition FROM CSS_dict WHERE search_object LIKE ?'
                results = conn.execute(query, ('%' + search_term + '%',)).fetchall()
                data = [dict(row) for row in results]
            else:
                query = 'SELECT search_object, definition FROM CSS_dict'
                results = conn.execute(query).fetchall()
                data = [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"SQL query error: {e}")
        #finally:
        conn.close()
        
    if program == "Python":
        conn = sqlite3.connect("python.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            if search_term:
                query = 'SELECT search_object, definition FROM Python_dict WHERE search_object LIKE ?'
                results = conn.execute(query, ('%' + search_term + '%',)).fetchall()
                data = [dict(row) for row in results]
            else:
                query = 'SELECT search_object, definition FROM Python_dict'
                results = conn.execute(query).fetchall()
                data = [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"SQL query error: {e}")
        #finally:
        conn.close()
        
    if program == "Javascript":
        conn = sqlite3.connect("java.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            if search_term:
                query = 'SELECT search_object, definition FROM Java_dict WHERE search_object LIKE ?'
                cursor.execute(query, ('%' + search_term + '%',)) # Execute the query using the cursor
                results = cursor.fetchall()
                data = [dict(row) for row in results]
            else:
                query = 'SELECT search_object, definition FROM Java_dict'
                results = conn.execute(query).fetchall()
                data = [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"SQL query error: {e}")
        #finally:
        conn.close()
        
    if program == "Flask":
        conn = sqlite3.connect("flask.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            if search_term:
                query = 'SELECT search_object, definition FROM Flask_dict WHERE search_object LIKE ?'
                cursor.execute(query, ('%' + search_term + '%',)) # Execute the query using the cursor
                results = cursor.fetchall()
                data = [dict(row) for row in results]
            else:
                query = 'SELECT search_object, definition FROM Flask_dict'
                results = conn.execute(query).fetchall()
                data = [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"SQL query error: {e}")
        #finally:
        conn.close()
        
    if program == "SQL":
        conn = sqlite3.connect("sql.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            if search_term:
                query = 'SELECT search_object, definition FROM SQL_dict WHERE search_object LIKE ?'
                cursor.execute(query, ('%' + search_term + '%',)) # Execute the query using the cursor
                results = cursor.fetchall()
                data = [dict(row) for row in results]
            else:
                query = 'SELECT search_object, definition FROM SQL_dict'
                results = conn.execute(query).fetchall()
                data = [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"SQL query error: {e}")
        #finally:
        conn.close()

    return render_template(
        "home_page.html", data=data, program=program,search_term=search_term)

CSV_FILE = 'reflections.csv'

def load_reflections():
    with open(CSV_FILE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

def save_reflections(reflections):
    with open(CSV_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(reflections)

@app.route("/edit/<int:index>", methods=["GET"])
def edit_reflection(index):
    index = index +1
    reflections = load_reflections()
    reflection = reflections[index]
    return render_template("edit_reflection.html", reflection=reflection, index=index)

@app.route("/update/<int:index>", methods=["POST"])
def update_reflection(index):
    program = request.form.get('program')
    date = request.form.get('date')
    ask = request.form.get('ask')
    reflections = request.form.get('reflections')

    reflections_data = load_reflections()
    # Update the specific row
    reflections_data[index] = [program, date, ask, reflections]

    save_reflections(reflections_data)

    return redirect("/reflection")
   
@app.route("/reflections")
def write_reflections():
    return render_template("reflections.html")

@app.route("/add", methods=["POST"])
def add():
  program = request.form["program"]
  date = request.form["date"]
  ask = request.form["ask"]
  reflections = request.form["reflections"]

  try:
        datetime.strptime(date, "%Y-%m-%d")
  except ValueError:
        return "Date incorrect, needs to be YYYY-MM-DD."
      
  # data to put inside csv file
  new_reflection_tracker = [program, date, ask, reflections]
  # file closes after with block
  with open("reflections.csv", "a",newline='') as file:
      writer = csv.writer(file)
      writer.writerow(new_reflection_tracker)
  return redirect("/reflection")
    

@app.route("/reflection")
def reflections():
 reflection_data = []

  # file closes after with block
 try:
    with open("reflections.csv", "r") as file:
      reader = csv.reader(file)
      next(reader)
      for row in reader:
        reflection_data.append(row)
 except FileNotFoundError:
    return "File not found"

 return render_template("reflections.html", reflection_data=reflection_data)



@app.route("/practice_code")
def practice():
    return render_template("practice_code.html")


search_term_list = []
def get_search(search_term):
    global search_term_list
    search_term_list.append(search_term)

@app.route("/recent_searches", methods=["GET", "POST"])
def get_recent_searches():
    global search_term_list
    recent_data = []

    conn = sqlite3.connect("recent_searches.db")  # Connect to the database
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recent_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_term TEXT UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    for item in search_term_list:
        cursor.execute("""
            INSERT INTO recent_searches (search_term, timestamp)
            VALUES (?, CURRENT_TIMESTAMP)
            ON CONFLICT(search_term) 
            DO UPDATE SET timestamp = CURRENT_TIMESTAMP
        """, (item,))
    conn.commit()  # Commiting changes to the database

    try:
        # Fetch recent searches from the database
        query = 'SELECT search_term, timestamp FROM recent_searches ORDER BY timestamp DESC LIMIT 20'
        cursor.execute(query)
        results = cursor.fetchall()
        recent_data = [dict(row) for row in results]
    except sqlite3.Error as e:
        print(f"SQL query error: {e}")
    finally:
        conn.close()

    return render_template("recent_searches.html", recent_data=recent_data)

@app.route("/advanced_search")
def advanced_search():
    return render_template("advanced_search.html")

def load_definitions():
    # Load the content of theory.txt as JSON
    with open('theory.txt', 'r') as file:
        data = json.load(file)

    # Split each question and answer into lists of words
    definitions = {}
    for question, answer in data.items():
        question_words = question.split()  # Split into words
        answer_words = answer.split()  # Split the answer into words
        definitions[tuple(question_words)] = answer_words  # Store as a tuple of words in the dictionary

    return definitions
            

@app.route("/searching", methods=["GET", "POST"])
def search_new():
    definitions = load_definitions()
    result = []

    if request.method == "POST":
        search_term = request.form.get('search2').strip().lower()

        if search_term == "":
            raise ValueError("Search term cannot be empty.")

        # Search through the definitions
        for question_words, answer_words in definitions.items():
            # Check if search_term matches any part of the question
            if " ".join(question_words).lower() in search_term:
                result.append({"search_object": " ".join(question_words), "definition": " ".join(answer_words)})

        # If no match found
        if not result:
            result = [{"search_object": search_term, "definition": "Definition not found."}]

    return render_template("advanced_search.html", result=result)
 
if __name__ == "__main__":
    app.run(debug=True)