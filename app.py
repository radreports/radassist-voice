from flask import Flask, render_template, request, jsonify
import openai
from openai import OpenAI
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

# Set your OpenAI API key here
openai.api_key = ''
client = OpenAI(api_key = '')

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/convert', methods=['POST'])
# def convert_text_to_fhir():
#     text = request.json['text']
#     try:
#         # Using OpenAI's API to process the text and generate FHIR resource
#         response = openai.Completion.create(
#             engine="gpt-3.5-turbo",  # Updated to use 'engine' instead of 'model'
#             prompt=f"Convert the following medical notes into a FHIR resource: {text}",
#             max_tokens=150,
#             temperature=0.5  # Optional: Adjusts randomness in responses
#         )
#         # Construct a FHIR resource from the response
#         fhir_resource = {
#             "resourceType": "Observation",
#             "text": text,
#             "interpretation": response.choices[0].text.strip()
#         }
#     except Exception as e:
#         print(e)
#         return jsonify({"error": str(e)}), 500

#     return jsonify(fhir_resource)


@app.route('/fhir', methods=['POST'])
def convert_text_to_fhir():
    text = request.json['text']
    try:
        # Using OpenAI's API to process the text and generate FHIR resource
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                "role": "user",
                "content": f"convert radiologist dictation to fhir resources, don't respond with verbose just return FHIR resources.extract the relevant clinical information and structure it into appropriate FHIR resources such as DiagnosticReport, Observation, and ImagingStudy: {text}"
                }
            ],
            temperature=0.5,
            max_tokens=900,
            top_p=1
            )
        # Construct a FHIR resource from the response
        print(response.choices[0].message.content)
        print(response)
        # fhir_resource = {
        #     "resourceType": "Observation",
        #     "text": text,
        #     "interpretation": response.choices[0].message.content.strip()
        # }
        fhir_resource = response.choices[0].message.content.strip()
    except Exception as e:
        # print(e)
        return jsonify({"error": str(e)}), 500

    return jsonify(fhir_resource)
    # return fhir_resource

@app.route('/layman', methods=['POST'])
def convert_text_to_layman():
    text = request.json['text']
    try:
        # Using OpenAI's API to process the text and generate FHIR resource
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                "role": "user",
                "content": f"convert radiologist dictation to text which a layman can understand: {text}"
                }
            ],
            temperature=0.5,
            max_tokens=900,
            top_p=1
            )
        # Construct a FHIR resource from the response
        print(response.choices[0].message.content)
        print(response)
        # fhir_resource = {
        #     "resourceType": "Observation",
        #     "text": text,
        #     "interpretation": response.choices[0].message.content.strip()
        # }
        fhir_resource = response.choices[0].message.content.strip()
    except Exception as e:
        # print(e)
        return jsonify({"error": str(e)}), 500

    return jsonify(fhir_resource)
    # return fhir_resource


@app.route('/conversation', methods=['POST'])
def convert_conversation_to_layman():
    text = request.json['text']
    try:
        # Using OpenAI's API to process the text and generate FHIR resource
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                "role": "user",
                "content": f"convert conversation between a patient and a doctor consultation into Diagnostic report: {text}"
                }
            ],
            temperature=0.5,
            max_tokens=900,
            top_p=1
            )
        # Construct a FHIR resource from the response
        print(response.choices[0].message.content)
        print(response)
        # fhir_resource = {
        #     "resourceType": "Observation",
        #     "text": text,
        #     "interpretation": response.choices[0].message.content.strip()
        # }
        fhir_resource = response.choices[0].message.content.strip()
    except Exception as e:
        # print(e)
        return jsonify({"error": str(e)}), 500

    return jsonify(fhir_resource)
    # return fhir_resource
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=False,threaded=True)
