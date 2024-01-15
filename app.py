from flask import Flask, render_template, request, jsonify, session
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

# Initialize the OpenAI client
openai.api_key = os.environ.get("OPENAI_API_KEY")
client = openai.Client(api_key=openai.api_key)

# Current Assistant: MiniMe
assistant_id = 'asst_9DWjbnuDqjQY45Lw0oIGKmBb'


@app.route('/')
def show_home():
    # Start a new thread for each user session
    if 'thread_id' not in session:
        thread = client.beta.threads.create()
        session['thread_id'] = thread.id
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']

    # Retrieve the thread ID from the user session
    thread_id = session.get('thread_id')

    # Add the user's message to the Thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # Run the Assistant to process the conversation
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Wait for the Run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            break

    # Retrieve the latest messages
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    # Find the index of the latest user message
    latest_user_msg_index = next(
        (i for i, m in enumerate(reversed(messages.data)) if m.role == 'user'),
        None
    )

    # Assuming messages are in chronological order, find the first assistant message after the latest user message
    reply = None
    if latest_user_msg_index is not None:
        for message in messages.data[-latest_user_msg_index:]:
            if message.role == 'assistant':
                reply = message.content[0].text.value
                break

    if reply is None:
        reply = "No response."

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
