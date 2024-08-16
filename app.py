from flask import Flask, request, Response, jsonify, render_template
import openai
from openai import OpenAI
from flask_cors import CORS
import logging
import io
# from PIL import Image
import base64
# import requests
import json

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key here
token = ''
openai.api_key = token
client = OpenAI(api_key=token)

@app.route('/')
def index():
    return render_template('index.html')

# FHIR-related route
@app.route('/fhir', methods=['GET'])
def convert_text_to_fhir():
    text = request.args.get('text')
    logging.debug(f"Received text: {text}")
    if not text:
        return jsonify({"error": "Missing text"}), 400

    def generate_fhir_data():
        try:
            responses = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": f"Convert radiologist dictation to FHIR resources, please do not return any content other than the FHIR resources. I am using streaming so please return the content appropriately: {text}"
                }],
                temperature=0,
                max_tokens=900,
                top_p=1,
                stream=True
            )
            
            for response in responses:
                part = response.choices[0].delta.content
                logging.debug(f"Streaming response part: {part}")
                if part:
                    yield f"data: {part}\n\n".encode('utf-8')
                
        except Exception as e:
            logging.error(f"An error occurred while streaming: {e}")
            yield json.dumps({"error": str(e)})  # Send error message as JSON

    return Response(generate_fhir_data(), mimetype='text/event-stream')

# Layman conversion route
@app.route('/layman', methods=['GET'])
def convert_text_to_layman():
    text = request.args.get('text')
    logging.debug(f"Received text: {text}")
    if not text:
        return jsonify({"error": "Missing text"}), 400

    def generate_fhir_data():
        try:
            responses = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": f"convert radiologist dictation to text which a layman can understand: {text}"
                }],
                temperature=0,
                max_tokens=900,
                top_p=1,
                stream=True
            )
            
            for response in responses:
                part = response.choices[0].delta.content
                logging.debug(f"Streaming response part: {part}")
                if part:
                    yield f"data: {part}\n\n".encode('utf-8')
                
        except Exception as e:
            logging.error(f"An error occurred while streaming: {e}")
            yield json.dumps({"error": str(e)})  # Send error message as JSON

    return Response(generate_fhir_data(), mimetype='text/event-stream')

# Conversation conversion route
@app.route('/conversation', methods=['GET'])
def convert_conversation_to_layman():
    text = request.args.get('text')
    logging.debug(f"Received text: {text}")
    if not text:
        return jsonify({"error": "Missing text"}), 400

    def generate_fhir_data():
        try:
            responses = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": f"convert conversation between a patient and a doctor consultation into Diagnostic report along with medical codes: {text}"
                }],
                temperature=0,
                max_tokens=900,
                top_p=1,
                stream=True
            )
            
            for response in responses:
                part = response.choices[0].delta.content
                logging.debug(f"Streaming response part: {part}")
                if part:
                    yield f"data: {part}\n\n".encode('utf-8')
                
        except Exception as e:
            logging.error(f"An error occurred while streaming: {e}")
            yield json.dumps({"error": str(e)})  # Send error message as JSON

    return Response(generate_fhir_data(), mimetype='text/event-stream')

# New image processing route
@app.route('/process-image', methods=['POST'])
def process_image():
    # Ensure both image and prompt are provided in the request
    if 'image' not in request.files or 'prompt' not in request.form:
        return jsonify({"error": "Image and prompt are required"}), 400

    image_file = request.files['image']
    prompt = request.form['prompt']

    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Load the image file
        image = Image.open(image_file)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        img_byte_arr = img_byte_arr.getvalue()

        # Encode image to base64
        encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

        # Prepare the payload with image and prompt
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image",
                            "image": {
                                "base64": encoded_image
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        # Send the request to OpenAI API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai.api_key}"
        }
        
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(payload))
        response_data = response.json()

        # Extract and return the response
        if response.status_code == 200:
            return jsonify(response_data)
        else:
            return jsonify({"error": response_data}), response.status_code

    except Exception as e:
        logging.error(f"An error occurred while processing the image: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
