import requests

def pegasus(text, max_length=None, min_length=None):
    if max_length is None:
        max_length = len(text) - 5
    
    if min_length is None:
        min_length = int(len(text) / 2)

    API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"
    headers = {"Authorization": "Bearer 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"}
    

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": text,
        "parameters": {'max_length': max_length, 'min_length': min_length}
    })
    print(output)

    return output[0]['summary_text']
