This repository contains my solution to the Globant Data Engineering Coding Challenge. The challenge involved building a REST API to handle CSV data uploads and performing SQL queries to analyze employee hiring data.

## Table of Contents

* [Project Description](#project-description)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Setup and Installation](#setup-and-installation)
    * [Prerequisites](#prerequisites)
    * [Installation Steps](#installation-steps)
* [API Endpoints](#api-endpoints)
    * [Section 1: API](#section-1-api)
    * [Section 2: SQL](#section-2-sql)
* [Data Structures](#data-structures)
* [Assumptions](#assumptions)
* [Future Improvements](#future-improvements)
* [Author](#author)

## Project Description

The goal of this project was to develop a REST API that can:

* Receive historical data from CSV files (departments, jobs, hired\_employees).
* Upload these files to a SQL database (PostgreSQL).
* Insert data in batch transactions (up to 1000 rows per request).

Additionally, the project requires creating API endpoints to provide specific data insights through SQL queries:

* Number of employees hired for each job and department in 2021, divided by quarter, ordered alphabetically.
* List of departments that hired more employees than the average in 2021, ordered by the number of employees hired (descending).

## Features

* **CSV Data Upload:** API endpoints to upload data from CSV files to the database.
* **Batch Data Insertion:** Efficient insertion of multiple rows into the database.
* **Data Analysis Endpoints:** API endpoints that use SQL queries to provide hiring insights.
* **Modular Design:** The application is structured with Flask blueprints for better organization.
* **Database Interaction:** Uses `psycopg2` to interact with the PostgreSQL database.
* **Error Handling:** Includes robust error handling for database operations and data processing.

## Technologies Used

* Python 3.x
* Flask:  A micro web framework for building the API.
* psycopg2:  A PostgreSQL adapter for Python.
* PostgreSQL: The SQL database used to store the data.
* CSV:  For reading data from CSV files.
* datetime: Python's datetime module for handling date and time data.

## Setup and Installation

### Prerequisites

* Python 3.6 or higher
* PostgreSQL installed and running
* pip (Python package installer)

### Installation Steps

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/diego0819/Globant_Challenge.git](https://github.com/diego0819/Globant_Challenge.git)
    cd Globant_Challenge
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the Database:**

    * Create a PostgreSQL database named `postgres` (or change the `dbname` in `app/db.py` to match your database name).
    * Update the database connection details in `app/db.py` with your PostgreSQL username, password, host, and port if necessary.

5.  **Run the Application:**

    ```bash
    python run.py
    ```

    The API will be accessible at `http://127.0.0.1:5000`.

## API Endpoints

### Section 1: API

* **`POST /upload-csv/<string:table_name>?file_path=<path_to_csv>`**
    * Description:  Uploads data from a CSV file to the specified table.
    * `table_name`: The name of the table to upload to (`departments`, `jobs`, or `hired_employees`).
    * `file_path`:  The path to the CSV file.
    
### Section 2: SQL

* **`GET /hires-by-quarter`**
    * Description:  Returns the number of employees hired for each job and department in 2021, divided by quarter, ordered alphabetically by department and job.
    *  Example:

        ```json
        {
            "Staff": {
                "Manager": {"Q1": 2, "Q2": 1, "Q3": 0, "Q4": 2},
                "Recruiter": {"Q1": 3, "Q2": 0, "Q3": 7, "Q4": 11}
            },
            "Supply Chain": {
                "Manager": {"Q1": 0, "Q2": 1, "Q3": 3, "Q4": 0}
            }
        }
        ```
      * http://127.0.0.1:5000/departments_above_average_hires
      

* **`GET /departments-above-average-hires`**
    * Description:  Returns a list of departments that hired more employees than the average in 2021, ordered by the number of employees hired (descending).
    * Output Example:

        ```json
        [
            {"id": 7, "department": "Staff", "hired": 45},
            {"id": 9, "department": "Supply Chain", "hired": 12}
        ]
        ```
      * http://127.0.0.1:5000/hires_by_quarter

## Data Structures

* **hired\_employees.csv:**
    * `id` (INTEGER):  Id of the employee.
    * `name` (STRING): Name and surname of the employee.
    * `datetime` (STRING): Hire datetime in ISO format (YYYY-MM-DD).
    * `department_id` (INTEGER): Id of the department which the employee was hired for.
    * `job_id` (INTEGER): Id of the job which the employee was hired for. 

* **departments.csv:**
    * `id` (INTEGER): Id of the department.
    * `department` (STRING): Name of the department. 

* **jobs.csv:**
    * `id` (INTEGER): Id of the job.
    * `job` (STRING): Name of the job. 

## Assumptions

* The CSV files are located in a `data/` directory relative to the project root.
* The database connection details are hardcoded in `app/db.py` (For production, environment variables would be preferred).
* Basic error handling is implemented, but more sophisticated logging and error management could be added.

## Future Improvements

* **Input Validation:** Add more robust validation for CSV file content and API requests.
* **Authentication/Authorization:** Secure the API endpoints with authentication and authorization.
* **Testing:** Implement unit and integration tests to ensure code quality and reliability.
* **Containerization:** Containerize the application using Docker for easier deployment.
* **Cloud Deployment:** Deploy the application to a cloud provider (e.g., AWS, Azure, Google Cloud).
* **Logging:** Implement comprehensive logging for debugging and monitoring.
* **Configuration:** Use environment variables or configuration files for settings (database connection, etc.).
* **ORM (Object-Relational Mapper):** Consider using SQLAlchemy to abstract database interactions.

## Author

* Diego Ojeda
