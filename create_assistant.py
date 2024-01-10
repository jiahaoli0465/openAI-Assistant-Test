

# Initialize the OpenAI client

import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")
client = openai.Client(api_key=openai.api_key)

# Create an Assistant
assistant_id = None


assistant = client.beta.assistants.create(
    name="Personal therapist",
    instructions="You are a personal therapist named Jacob. Make sure you act like a therapist.",
    model="gpt-3.5-turbo-16k"
)
assistant_id = assistant.id

print(assistant.id)