from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
from gradio_client import Client

client = Client("https://atulit23-google-flan-t5.hf.space/")
unified_url = "https://review-and-ads.vercel.app/text-interference"
app = Flask(__name__)
CORS(app)  

@app.route('/review-terms-of-cancellation', methods=['GET'])
def termsOfCancellation():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Please provide a URL in the "url" parameter.'}), 400

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        all_text = soup.get_text()
        all_text = all_text.lower().split(" ")

        new_text = ""
        indices = []
        for i, j in enumerate(all_text):
            if j.lower().find("cancellation") != -1:
                indices.append(i)

        if not indices:
            return jsonify({'response': 'No occurrences of "cancellation" found in the text.'})

        if len(indices) > 1:
            if (indices[-1] - indices[0] > 600):
                new_text = ' '.join(all_text[indices[0] + 200: indices[-1] + 100])
                # if (indices[-1] - indices[-2] > 600):
                #     new_text = ' '.join(all_text[indices[-1] - 120: indices[-1] + 120])
                # else:
                #     new_text = ' '.join(all_text[indices[-2] - 60: indices[-1] + 120])
            else:
                new_text = ' '.join(all_text[indices[0]: indices[-1]])
        else:
            new_text = ' '.join(all_text[indices[0] - 120: indices[0] + 150])

        new_text = new_text + '. Are the terms of cancellation clear ? Answer in yes or no.'

        print(new_text)

        data = {'text': new_text}

        try:
            result = client.predict(
				new_text,
				api_name="/predict"
            )
            print(result)
            print(type(result))
            # response = requests.post(unified_url, json=data)
            # response.raise_for_status()
            # print(response.text)
            if(result.find("no") != -1):
                return jsonify({"response": "The terms of cancellation are not clear."})
            else:
                return jsonify({"response": "The terms of cancellation are clear."})
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"response": f"Error occurred: {str(e)}"})

    else:
        return jsonify({'error': f"Failed to retrieve the webpage. Status code: {response.status_code}"}), 500

@app.route('/how-to-cancel', methods=['GET'])
def howToCancel():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Please provide a URL in the "url" parameter.'}), 400

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        all_text = soup.get_text()
        all_text = all_text.lower().split(" ")

        new_text = ""
        indices = []
        for i, j in enumerate(all_text):
            if j.lower().find("cancellation") != -1:
                indices.append(i)

        if not indices:
            return jsonify({'response': 'No occurrences of "cancellation" found in the text.'})
        print(indices)
        if len(indices) > 1:
            if (indices[-1] - indices[0] > 600):
                new_text = ' '.join(all_text[indices[0] + 200: indices[-1] + 100])
                # if (indices[-1] - indices[-2] > 600):
                #     new_text = ' '.join(all_text[indices[-1] - 120: indices[-1] + 120])
                # else:
                #     new_text = ' '.join(all_text[indices[-2] - 60: indices[-1] + 120])
            else:
                new_text = ' '.join(all_text[indices[0]: indices[-1]])
        else:
            new_text = ' '.join(all_text[indices[0] - 120: indices[0] + 150])

        new_text = new_text + '. Do they tell you how to cancel the subscription? Answer in yes or no.'
        # print(new_text)

        data = {'text': new_text}

        try:
            result = client.predict(
				new_text,
				api_name="/predict"
            )
            print(result)
            # response = requests.post(unified_url, json=data)
            # response.raise_for_status()
            # print(response.text)
            if(result.find("no") != -1):
                return jsonify({"response": "They don't explain you how to cancel your subscription!"})
            else:
                return jsonify({"response": "They explain you how to cancel your subscription!"})
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"response": f"Error occurred: {str(e)}"})
    
    else:
        return jsonify({'error': f"Failed to retrieve the webpage. Status code: {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
