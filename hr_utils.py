import json
#import tkinter as tk
#from tkinter import simpledialog
import sqlite3
#Need JSON file genereted by jupyter notebook

# Call the function and provide the database file path
database_file = 'challenge.db'  # Replace with the actual database file path

def process_data_and_update_db():
    conn = sqlite3.connect('challenge.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table named "hr_collaborator_scores" if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hr_collaborator_scores (
            id INTEGER PRIMARY KEY,
            collaborator_score FLOAT,
            score_txt TEXT
        )
    ''')

    # Read data from JSON file
    with open('hr_data_prediction.json', 'r') as f:
        data = json.load(f)

    # Process and update the data
    for item in data:
        py_list_id = item['ID']
        py_list_prediction = item['prediction']

        if py_list_prediction >= 0.8:
            grade = 'High'
        elif py_list_prediction >= 0.7:
            grade = 'Above_Average'
        elif py_list_prediction >= 0.5:
            grade = 'Average'
        elif py_list_prediction >= 0.3:
            grade = 'Below_Average'
        else:
            grade = 'Low'

        # Check if the value exists in the table
        cursor.execute('SELECT id FROM hr_collaborator_scores WHERE id = ?', (py_list_id,))
        id_result = cursor.fetchall()

        cursor.execute('SELECT collaborator_score FROM hr_collaborator_scores WHERE id = ?', (py_list_id,))
        score_result = cursor.fetchall()

        # Extract the float value from the tuple
        if score_result:
            existing_score = score_result[0][0]

        if id_result:
            existing_id = id_result[0][0]

        if not id_result:
            # Set a default value for new entries
            existing_score = 0.0  # Default value for new entries
            
            # Insert data into the table
            cursor.execute('INSERT INTO hr_collaborator_scores (id, collaborator_score, score_txt) VALUES (?, ?, ?)',
                        (py_list_id, existing_score, grade))
            conn.commit()
            print(f"Score for ID {py_list_id} was added with a score {py_list_prediction} and grade {grade}")

        elif py_list_prediction != existing_score and id_result == py_list_id:
            # Update the specified fields in the row
            cursor.execute('UPDATE hr_collaborator_scores SET collaborator_score = ?, score_txt = ? WHERE id = ?',
                        (py_list_prediction, grade, py_list_id))
            # Commit the changes
            conn.commit()
            print(f"Score for ID {py_list_id}, {existing_id} updated to {py_list_prediction} from {existing_score}")

        else:
            print(f"ID {py_list_id} exists with the same score and grade")

    # Close the cursor and the connection
    cursor.close()
    conn.close()

def retrieve_scores_and_ids(database_file,id):
    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve scores and IDs
    cursor.execute('SELECT id, collaborator_score, score_txt FROM hr_collaborator_scores WHERE id = ?', (id,))

    # Fetch and return the result
    result = cursor.fetchall()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    return result