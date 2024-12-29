import requests
import json

def query_gemma2_model(prompt):
    """
    Query the Gemma2:2b model with a given prompt and return the response.
    """
    template = {
        "model": "gemma2:2b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post('http://127.0.0.1:11434/api/generate', json=template)
        if response.status_code == 200:
            llm_response = json.loads(response.text)
            return llm_response.get('response', "No response received.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# import requests
# import json

# template = {
#     "model":"gemma2:2b",
#     "prompt":"Why is the sky blue?",
#     "stream": False
# }

# response = requests.post('http://127.0.0.1:11434/api/generate',json=template)

# llm_response = json.loads(response.text)

# print(response)

# #print(response.text)

# # print(llm_response.keys())

# #print("Response by the google gemma 2 model -->",llm_response['response'])