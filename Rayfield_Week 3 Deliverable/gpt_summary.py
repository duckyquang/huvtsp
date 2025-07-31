import openai

def gpt_summary(prompt_text, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content
