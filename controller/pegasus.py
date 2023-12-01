import requests

def pegasus(text):
    API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": text,
    })

    return output[0]['summary_text']