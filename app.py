from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

import google.generativeai as genai
import sqlite3
import os
import json

#API Key setup

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

#SQL Safety check

def is_unsafe_question(question):

    unsafe_words = [
        "delete",
        "drop",
        "truncate",
        "update",
        "insert",
        "remove",
        "alter"
    ]

    question = question.lower()

    return any(word in question for word in unsafe_words)


#SQL Generation

def generate_sql(question):

    prompt = f"""
You are a SQLite expert.

Database Schema:

customers(
id INTEGER,
name TEXT,
email TEXT,
city TEXT,
created_at DATE
)

products(
id INTEGER,
name TEXT,
category TEXT,
price REAL
)

orders(
id INTEGER,
customer_id INTEGER,
product_id INTEGER,
quantity INTEGER,
order_date DATE
)

Rules:
1. Return ONLY SQL
2. Use SQLite syntax
3. Generate SELECT queries only
4. No markdown
5. No explanations
6. Use exact table and column names

Question:
{question}
"""

    response = model.generate_content(prompt)

    sql = response.text.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


#Logging the queries

def log_query(question, sql, status):

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "sql": sql,
        "status": status
    }

    try:
        with open("query_logs.json", "r") as f:
            logs = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open("query_logs.json", "w") as f:
        json.dump(logs, f, indent=4)


#SQL Validation

FORBIDDEN = [
    "DELETE",
    "UPDATE",
    "INSERT",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "ATTACH",
    "REPLACE",
    "PRAGMA"
]


def validate_sql(sql):

    if not isinstance(sql, str):
        return False

    if not sql.strip().upper().startswith("SELECT"):
        return False

    upper_sql = sql.upper()

    for keyword in FORBIDDEN:
        if keyword in upper_sql:
            return False

    return True


# Database execution


def run_query(sql):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(sql)

    rows = cursor.fetchall()

    results = [dict(row) for row in rows]

    conn.close()

    return results



#QueryExplanation

def explain_results(question, results):

    prompt = f"""
Question:
{question}

Results:
{results}

Explain these results in plain English for a business user.

Maximum 3 sentences.
Keep it concise.
"""

    response = model.generate_content(prompt)

    return response.text.strip()



#Routes

@app.route("/")
def home():

    return jsonify({
        "message": "AI SQL Assistant Running"
    })


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


@app.route("/logs")
def logs():

    try:

        with open("query_logs.json", "r") as f:
            data = json.load(f)

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/query", methods=["POST"])
def query():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body missing"
            }), 400

        question = data.get("question")

        if not question:
            return jsonify({
                "error": "Question is required"
            }), 400

        # Block unsafe requests immediately
        if is_unsafe_question(question):

            log_query(
                question,
                "BLOCKED",
                "blocked"
            )

            return jsonify({
                "error": "Unsafe request detected"
            }), 400

        # Generate SQL
        sql = generate_sql(question)

        # Validate SQL
        if not validate_sql(sql):

            log_query(
                question,
                sql,
                "blocked"
            )

            return jsonify({
                "error": "Unsafe SQL detected",
                "generated_sql": sql
            }), 400

        # Execute SQL
        results = run_query(sql)

        # Generate explanation
        explanation = explain_results(
            question,
            results
        )

        # Log successful request
        log_query(
            question,
            sql,
            "success"
        )

        return jsonify({
            "sql": sql,
            "results": results,
            "explanation": explanation
        })

    except sqlite3.Error as e:

        return jsonify({
            "error": "Database Error",
            "details": str(e)
        }), 400

    except Exception as e:

        return jsonify({
            "error": "Server Error",
            "details": str(e)
        }), 500



# Final app

if __name__ == "__main__":
    app.run(debug=True)