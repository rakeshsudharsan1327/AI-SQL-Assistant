# AI SQL Assistant

## Overview

AI SQL Assistant is a REST API that enables non-technical users to interact with a database using natural language. Instead of writing SQL queries manually, users can ask questions such as:

> "Show all customers"

> "How many orders were placed last month?"

> "Show customers from Chennai"

The system uses Google's Gemini LLM to convert natural language questions into SQLite queries, execute them safely, and return both structured results and a business-friendly explanation.

This project was built as part of a technical assessment for an LLM Engineer / AI Engineer role.

---

## Features

* Natural Language → SQL conversion
* SQLite query execution
* Business-friendly result explanations
* REST API interface
* Structured JSON responses
* Read-only query enforcement
* Multi-layer SQL safety validation
* Query audit logging
* Health monitoring endpoint
* Query history endpoint

---

## Architecture

```text
User Question
      ↓
Gemini LLM
      ↓
SQL Generation
      ↓
Safety Validation
      ↓
SQLite Database
      ↓
Query Results
      ↓
Gemini Explanation
      ↓
JSON Response
```

---

## Technology Stack

### Backend

* Python
* Flask

### Database

* SQLite

### AI / LLM

* Google Gemini 2.5 Flash

### Supporting Libraries

* python-dotenv
* google-generativeai

---

## Project Structure

```text
ai-sql-assistant/

├── app.py
├── database.db
├── schema.sql
├── requirements.txt
├── README.md
├── query_logs.json
├── .env (local only, not commited)
└── .gitignore
```

---

## Database Schema

### customers

| Column     | Type    |
| ---------- | ------- |
| id         | INTEGER |
| name       | TEXT    |
| email      | TEXT    |
| city       | TEXT    |
| created_at | DATE    |

### products

| Column   | Type    |
| -------- | ------- |
| id       | INTEGER |
| name     | TEXT    |
| category | TEXT    |
| price    | REAL    |

### orders

| Column      | Type    |
| ----------- | ------- |
| id          | INTEGER |
| customer_id | INTEGER |
| product_id  | INTEGER |
| quantity    | INTEGER |
| order_date  | DATE    |

---

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd ai-sql-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Obtain a free Gemini API key from Google AI Studio.

---

## Running the Application

```bash
python app.py
```

The application will start on:

```text
http://127.0.0.1:5000
```

---

## API Endpoints

### GET /

Health message confirming the API is running.

#### Response

```json
{
    "message": "AI SQL Assistant Running"
}
```

---

### GET /health

Returns application health status.

#### Response

```json
{
    "status": "healthy"
}
```

---

### GET /logs

Returns query execution history and audit logs.

#### Response

```json
[
    {
        "timestamp": "2026-06-08 14:20:00",
        "question": "Show all customers",
        "sql": "SELECT * FROM customers",
        "status": "success"
    }
]
```

---

### POST /query

Converts natural language into SQL, executes the query, and explains the results.

#### Request

```json
{
    "question": "Show all customers"
}
```

#### Response

```json
{
    "sql": "SELECT id, name, email, city, created_at FROM customers",
    "results": [
        {
            "id": 1,
            "name": "Vijay",
            "email": "vijay@test.com",
            "city": "perambur",
            "created_at": "2026-05-10"
        }
    ],
    "explanation": "This data provides a comprehensive list of all customers."
}
```

---

## SQL Safety Implementation

To prevent accidental or malicious database modifications, the system implements multiple layers of protection.

### Natural Language Validation

The following request types are blocked before SQL generation:

* DELETE
* DROP
* TRUNCATE
* UPDATE
* INSERT
* REMOVE
* ALTER

Example:

```json
{
    "question": "Delete all customers"
}
```

Response:

```json
{
    "error": "Unsafe request detected"
}
```

---

### SQL Validation

Only SELECT queries are permitted.

Blocked operations include:

* DELETE
* UPDATE
* INSERT
* DROP
* ALTER
* TRUNCATE
* ATTACH
* REPLACE
* PRAGMA

This ensures the database remains read-only.

---

## Query Logging

Every request is recorded in `query_logs.json`.

Logged information includes:

* Timestamp
* User question
* Generated SQL
* Execution status

This provides auditability and easier debugging.

---

## Example Questions

```text
Show all customers

How many customers are there?

Show customers from Chennai

Show all products

What is the average product price?

Show top customers by number of orders
```

---

## Error Handling

The API handles:

* Missing request bodies
* Missing questions
* Unsafe requests
* Invalid SQL generation
* SQLite execution failures
* Unexpected server errors

All errors are returned in structured JSON format.

---

## Design Decisions

### Why Gemini?

Gemini 2.5 Flash was selected because it provides:

* Fast response times
* Strong natural language understanding
* High-quality SQL generation
* Free developer access

### Why SQLite?

SQLite is lightweight, easy to set up, and suitable for local analytics use cases and technical demonstrations.

### Why Flask?

Flask offers a minimal and flexible framework for rapidly developing REST APIs.

---

## Future Improvements

Potential enhancements include:

* Conversational memory for follow-up questions
* SQL self-correction loop
* Chart recommendations
* Data visualization endpoints
* Multi-database support
* User authentication
* Query caching
* Docker deployment
* Role-based access control

---

## Assumptions

* Database schema is known and fixed.
* Only analytical, read-only queries are supported.
* Users interact through the REST API.
* SQLite is used as the primary data source.

---

## Author

Developed as part of an AI Engineer / LLM Engineer technical assessment demonstrating:

* LLM integration
* Prompt engineering
* SQL generation
* API development
* Secure query execution
* Audit logging
* Error handling
  
## Assumptions

* The database schema is known and fixed at runtime.
* Users interact with the system through the REST API.
* Only analytical and read-only queries are supported.
* SQLite is used as the underlying database.
* The Gemini model generates syntactically valid SQL for the provided schema.

---

## Limitations

* The application currently supports only SQLite databases.
* Follow-up conversational questions are not supported.
* The system relies on LLM-generated SQL and may occasionally produce incorrect queries for highly complex questions.
* Chart generation and data visualization are not implemented.
* SQL self-correction is not implemented if a generated query fails.
* Authentication and user-specific access controls are not included.
* The database schema is currently embedded in the prompt and must be updated manually if the schema changes.
* The application is intended for demonstration and assessment purposes and is not production-hardened.




