from flask import Flask, render_template, request
from hr_utils import process_data_and_update_db, retrieve_scores_and_ids

app = Flask(__name__)
app.debug = True  

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/process', methods=['POST'])

def process():
    process_data_and_update_db()
    return render_template('index.html', status='Data processed and scores updated')

@app.route('/retrieve', methods=['POST'])
def retrieve():
    id_to_retrieve = request.form['id_to_retrieve']
    result = retrieve_scores_and_ids('challenge.db', id_to_retrieve)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
