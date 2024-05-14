from flask import Flask, request, Response, jsonify
import openai
from openai import OpenAI
from flask_cors import CORS
import json
import logging


app=Flask(__name__)
CORS(app)

# Set your OpenAI API key here
token = ''
openai.api_key = token
client = OpenAI(api_key = token)

@app.route('/')
def index():
    return render_template('index.html')



# @app.route('/fhir', methods=['POST'])
# def convert_text_to_fhir():
#     text = request.json['text']
#     try:
#         # Using OpenAI's API to process the text and generate FHIR resource
#         response = client.chat.completions.create(
#             model="gpt-4-turbo",
#             messages=[
#                 {
#                 "role": "user",
#                 "content": f"convert radiologist dictation to fhir resources, don't respond with verbose just return FHIR resources.extract the relevant clinical information and structure it into appropriate FHIR resources such as DiagnosticReport, Observation, and ImagingStudy: {text}"
#                 }
#             ],
#             temperature=0.5,
#             max_tokens=900,
#             top_p=1,
#             stream=True
#             )
#         # Construct a FHIR resource from the response
#         print(response.choices[0].message.content)
#         print(response)
#         # fhir_resource = {
#         #     "resourceType": "Observation",
#         #     "text": text,
#         #     "interpretation": response.choices[0].message.content.strip()
#         # }
#         fhir_resource = response.choices[0].message.content.strip()
#     except Exception as e:
#         # print(e)
#         return jsonify({"error": str(e)}), 500

#     return jsonify(fhir_resource)
#     # return fhir_resource

# @app.route('/fhir', methods=['GET'])
# def convert_text_to_fhir():
#     text = request.args.get('text')
#     logging.debug(f"Received text: {text}")
#     if not text:
#         return jsonify({"error": "Missing text"}), 400
    
#     try:
#         responses = client.chat.completions.create(
#             model="gpt-4",
#             messages=[{
#                 "role": "user",
#                 "content": f"Convert radiologist dictation to FHIR resources: {text}"
#             }],
#             temperature=0,
#             max_tokens=900,
#             top_p=1,
#             stream=True
#         )
        
#         print(responses)
#         # for chunk in responses:
#         #     # print(chunk)
#         #     # print(chunk.choices[0].delta.content)
            
#         #     print("****************")
#         full_response = ""
#         for response in responses:
#             part = response.choices[0].delta.content
#             print(part)
#             full_response += part
#             logging.debug(f"Appending response part: {part}")
#             # if 'choices' in response and len(response['choices']) > 0:
#             #     # part = response['choices'][0]['delta']['content']
#             #     part = response.choices[0].delta.content
#             #     print(part)
#             #     full_response += part
#             #     logging.debug(f"Appending response part: {part}")

#         if not full_response:
#             logging.error("Received an empty response from the API.")
#             return jsonify({"error": "Empty response from API"}), 500

#         # Check the full concatenated response before parsing
#         logging.debug(f"Full concatenated response: {full_response}")

#         fhir_resource = json.loads(full_response)
#         return jsonify(fhir_resource)

#     except json.JSONDecodeError as e:
#         logging.error(f"JSON parsing error: {e}")
#         return jsonify({"error": "Failed to parse JSON response"}), 500
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         return jsonify({"error": str(e)}), 500



@app.route('/fhir', methods=['GET'])
def convert_text_to_fhir():
    text = request.args.get('text')
    logging.debug(f"Received text: {text}")
    if not text:
        return jsonify({"error": "Missing text"}), 400

    def generate_fhir_data():
        try:
            responses = client.chat.completions.create(
                model="gpt-4",
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
                # part = response['choices'][0]['delta']['content']
                part = response.choices[0].delta.content
                logging.debug(f"Streaming response part: {part}")
                if part:  # Make sure part is not None
                        logging.debug(f"Streaming response part: {part}")
                        # print(f"Streaming response part: {part}")
                        yield f"data: {part}\n\n".encode('utf-8')
                
        except Exception as e:
            logging.error(f"An error occurred while streaming: {e}")
            print(f"An error occurred while streaming: {e}")
            yield json.dumps({"error": str(e)})  # Send error message as JSON

    return Response(generate_fhir_data(), mimetype='text/event-stream')



@app.route('/layman', methods=['GET'])
def convert_text_to_layman():
    text = request.args.get('text')
    logging.debug(f"Received text: {text}")
    if not text:
        return jsonify({"error": "Missing text"}), 400

    def generate_fhir_data():
        try:
            responses = client.chat.completions.create(
                model="gpt-4",
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
                # part = response['choices'][0]['delta']['content']
                part = response.choices[0].delta.content
                logging.debug(f"Streaming response part: {part}")
                if part:  # Make sure part is not None
                        logging.debug(f"Streaming response part: {part}")
                        # print(f"Streaming response part: {part}")
                        yield f"data: {part}\n\n".encode('utf-8')
                
        except Exception as e:
            logging.error(f"An error occurred while streaming: {e}")
            print(f"An error occurred while streaming: {e}")
            yield json.dumps({"error": str(e)})  # Send error message as JSON

    return Response(generate_fhir_data(), mimetype='text/event-stream')
    # return fhir_resource


@app.route('/conversation', methods=['GET'])
def convert_conversation_to_layman():
    text = request.args.get('text')
    logging.debug(f"Received text: {text}")
    if not text:
        return jsonify({"error": "Missing text"}), 400

    def generate_fhir_data():
        try:
            responses = client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "user",
                    "content": f"convert conversation between a patient and a doctor consultation into Diagnostic report: {text}"
                }],
                temperature=0,
                max_tokens=900,
                top_p=1,
                stream=True
            )
            
            for response in responses:
                # part = response['choices'][0]['delta']['content']
                part = response.choices[0].delta.content
                logging.debug(f"Streaming response part: {part}")
                if part:  # Make sure part is not None
                        logging.debug(f"Streaming response part: {part}")
                        # print(f"Streaming response part: {part}")
                        yield f"data: {part}\n\n".encode('utf-8')
                
        except Exception as e:
            logging.error(f"An error occurred while streaming: {e}")
            print(f"An error occurred while streaming: {e}")
            yield json.dumps({"error": str(e)})  # Send error message as JSON

    return Response(generate_fhir_data(), mimetype='text/event-stream')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
