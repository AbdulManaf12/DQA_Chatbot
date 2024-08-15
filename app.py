from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure the Google Generative AI API
GOOGLE_API_KEY = ''

file = open('api_key.txt', 'r')
GOOGLE_API_KEY = file.read()
file.close()

genai.configure(api_key=GOOGLE_API_KEY)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling the file upload and question
@app.route('/ask', methods=['POST'])
def ask_question():
    if 'image' not in request.files or 'question' not in request.form:
        return jsonify({"error": "No image or question provided"}), 400
    
    image = request.files['image']
    question = request.form['question']

    # Save the uploaded image
    image_path = os.path.join("uploads", image.filename)
    image.save(image_path)

    # Upload the file to the Google API
    sample_file = genai.upload_file(path=image_path, display_name=image.filename)
    file = genai.get_file(name=sample_file.name)

    # Generate a response from the AI model
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    response = model.generate_content([question, sample_file])

    # Remove the uploaded image after processing
    os.remove(image_path)

    # Return the response as JSON
    return jsonify({"response": response.text})

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
