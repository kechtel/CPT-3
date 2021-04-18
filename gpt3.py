import openai

from settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def prompt(quest):
    # create prompt
    _prompt = (
        open('gpt-3-prompts/input_train.txt', 'r').read() + "\n" +
        'Someone asked me to summarize the following text:\n' +
        quest +
        "\n\nI structured my summary into symptoms, diagnosis, and treatment as follows:"
    )

    # push prompt
    response = openai.Completion.create(
        engine="davinci",
        prompt=_prompt,
        temperature=0.1,
        stop=["###"],
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text


def parse_response(response):
    response += '###'
    keys = [line for line in response.split('\n') if not line.startswith('-') and len(line) > 0]
    print(keys)
    result = {}
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            break
        values = response.split(key)[1].split(keys[i+1])[0]
        result[key] = [v.strip() for v in values.replace('\n', '').split('-') if len(v) > 0]
    return result
