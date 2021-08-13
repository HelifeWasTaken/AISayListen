# AI Say Listen

A simple wrapper to simply use microphone and microphone to interact with an AI
You can use it this way:

```py
from AISayListen import AISL

ai = AISL()
ai.set_language("en") # Because it is set by default to french
print("The AI will repeat what you said please speak: ")
ai.say(ai.listen())
```

An integration with OpenAI and GPT-3 for example:
```py
import os
import openai
import sys
from AISayListen import AISL

ai = AISL()
ai.set_language("en") # Because it is set by default to french
openai.api_key = os.getenv("OPENAI_API_KEY")
AI_MESSAGES="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

while True:
    try:
        print("Waiting you to talk: ")
        prompt = ai.listen()
        if prompt is None:
            continue
        print(f"You said: {prompt}")
        AI_MESSAGES += prompt + "\nAI:"
    except Exception as e:
        print(f"Except: {e}", file=sys.stderr)
        print("There was an error while connecting with DB maybe permissions to Google Services", file=sys.stderr)
        continue
    while True:
        try:
            print("Waiting for the AI to answer: ")
            response = openai.Completion.create(
                  engine="davinci",
                  prompt=(AI_MESSAGES,),
                  temperature=0.9,
                  max_tokens=150,
                  top_p=1,
                  frequency_penalty=0.0,
                  presence_penalty=0.6,
                  stop=["\n", " Human:", " AI:"]
            )
            response = response["choices"][0]["text"]
            print(f"AI replied: {response}")
            print("Waiting for the text to speech to process info: ")
            ai.say(response)
            print("Text to speech replied")
            AI_MESSAGES += response + "\n\nHuman: "
        except Exception as e:
            print(f"Except: {e}", file=sys.stderr)
            print("OpenAI Request failed", file=sys.stderr)
            continue
        break
