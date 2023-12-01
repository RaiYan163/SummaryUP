import requests

def punctuation(text):
    API_URL = "https://api-inference.huggingface.co/models/unikei/distilbert-base-re-punctuate"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": text,
    })

    punctuated_sentences = ""

    def capital(word, cap):
        if cap == 'U':
            return word[0].upper() + word[1:]
        else:
            return word

    def punc_func(sign):
        if sign == '_':
            return ' '
        else:
            return sign + ' '

    for item in output:
        word = item['word']
        entity = item['entity_group']
        if len(entity) != 0:
            capital_letter = entity[0]
            punctuation = entity[-1]
        else:
            punctuated_sentence += item['word']
        capitalized_word = capital(word, capital_letter)
        punctuated_sentence += capitalized_word + punc_func(punctuation)

    return punctuated_sentence
