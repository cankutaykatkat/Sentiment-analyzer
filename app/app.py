from flask import Flask, request, jsonify, render_template
from model.sentiment import analyze_sentiment
import sqlite3
from datetime import datetime

# Initialize the Flask application
app = Flask(
    __name__,
    static_folder='../static',  # Path to static files
    template_folder='templates'  # Path to templates folder
)

# Home route for rendering the main interface
@app.route('/')
def home():
    return render_template('index.html')

# Route for sentiment prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get JSON data from the request
    text = data.get('text', '')  # Extract the 'text' field
    sentiment = analyze_sentiment(text)  # Analyze the sentiment using the model
    return jsonify({'sentiment': sentiment})  # Return the result as JSON

# Route for saving user feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    text = data.get('text', '')
    sentiment = data.get('sentiment', '')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp

    # Collect IP address and User-Agent
    ip_address = request.remote_addr  # Get the user's IP address
    user_agent = request.headers.get('User-Agent')  # Get browser/device info

    try:
        # Connect to the database
        conn = sqlite3.connect('app/database/feedback.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (ip_address, user_agent, text, sentiment, timestamp) VALUES (?, ?, ?, ?, ?)",
            (ip_address, user_agent, text, sentiment, timestamp)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Feedback saved successfully'})
    except sqlite3.Error as e:
        return jsonify({'error': f"Failed to save feedback: {str(e)}"}), 500

# Route to view feedback
@app.route('/feedback/view', methods=['GET'])
def view_feedback():
    try:
        # Connect to the database
        conn = sqlite3.connect('app/database/feedback.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ip_address, user_agent, text, sentiment, timestamp FROM feedback")
        feedback = cursor.fetchall()
        conn.close()

        # Generate HTML table
        feedback_html = '''
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; color: #333; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f4f4f4; }
        </style>
        <h1>User Feedback</h1>
        <table>
            <tr>
                <th>IP Address</th>
                <th>User-Agent</th>
                <th>Text</th>
                <th>Sentiment</th>
                <th>Timestamp</th>
            </tr>
        '''
        for entry in feedback:
            feedback_html += f'''
            <tr>
                <td>{entry[0]}</td>
                <td>{entry[1]}</td>
                <td>{entry[2]}</td>
                <td>{entry[3]}</td>
                <td>{entry[4]}</td>
            </tr>
            '''
        feedback_html += '</table>'
        return feedback_html
    except sqlite3.Error as e:
        return f"Error retrieving feedback: {str(e)}"

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
