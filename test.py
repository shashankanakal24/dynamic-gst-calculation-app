from flask import Flask, request, jsonify
import requests
import google.generativeai as genai

app = Flask(__name__)

# Replace with your actual Gemini API endpoint and authentication details
GEMINI_API_URL = "https://aistudio.google.com/app/apikey"
GEMINI_API_KEY = "AIzaSyAjiF2M54OqCfJX8oLhvWF2vHs_YXg3S4w"  # Add authentication if required

@app.route('/test', methods=['POST'])
def process_query():
    try:
        data = request.json
        user_input = data['user_input']

        # Access user input safely
        print(f"Received user input: {user_input}")
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel()  # Remove the 'name' argument
        response = model.generate_content(user_input)

        # Debug: Print the entire response object to understand its structure
        print('response:', response)

        # Accessing the generated content correctly
        generated_content = response.candidates[0].content.parts[0].text
        print('generated_content:', generated_content)
        return jsonify({'result': generated_content})  # Return only the generated text

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)  # Log the error for troubleshooting
        return jsonify({'result': error_message}), 500  # Internal Server Error


if __name__ == '__main__':
    app.run(debug=True)