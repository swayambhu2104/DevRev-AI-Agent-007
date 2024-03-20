from openai import OpenAI
import os
from prompt_creater import prompt_creater

def read_api_key_from_file(file_path):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

openai_api_key = read_api_key_from_file('openai_key.txt')

def llm_plus_p_function(query):
    prompt = prompt_creater(query)

    client = OpenAI(
        # This is the default and can be omitted
        api_key=openai_api_key,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )

    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": prompt}
    #     ]
    # )

    return response.choices[0].message.content

