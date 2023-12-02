import requests

def pegasus(text, max_length=None, min_length=None):
    if max_length is None:
        max_length = 100
    
    if min_length is None:
        min_length = 50
    print(len(text))
    print("------------------")

    API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"
    headers = {"Authorization": "Bearer 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"}
    

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": text,
        
    })
    print(output)

    return output[0]['summary_text']
