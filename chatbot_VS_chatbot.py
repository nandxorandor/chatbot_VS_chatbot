from flask import Flask, request, jsonify, render_template
from langchain.llms import LlamaCpp  # Import the LlamaCpp library
app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize conversation history for Chatbot-1 and Chatbot-2
chatbot1_history = []
chatbot2_history = []

# Initialize LlamaCpp Model
llm_chatbot = LlamaCpp(
    streaming=True,
    model_path="zephyr-7b-alpha.Q4_K_M.gguf",  # Replace with your actual model path
    temperature=0.75,
    top_p=0.9,
    verbose=True,
    n_ctx=4096,
    n_gpu_layers=32  # Adjust as per your configuration
)

@app.route('/')
def index():
    return render_template('chatVSchat.html')

@app.route('/chatbot1', methods=['POST'])
def chatbot1():
    user_input = request.form['user_input']
    
    # Generate a response using a higher max_tokens value
    chatbot1_response = llm_chatbot.generate([f"User: {user_input}\nChatbot:"], max_tokens=80)
    chatbot1_response_text = chatbot1_response.generations[0][0].text.strip()
    
    # Append Chatbot-1's response to its conversation history
    chatbot1_history.append(user_input)
    chatbot1_history.append(chatbot1_response_text)
    
    # Return the response with the name "Ahmed"
    return jsonify({"name": "Ahmed", "response": chatbot1_response_text})

@app.route('/chatbot2', methods=['POST'])
def chatbot2():
    user_input = request.form['user_input']
    
    # Generate a response using a higher max_tokens value
    chatbot2_response = llm_chatbot.generate([f"User: {user_input}\nChatbot:"], max_tokens=80)
    chatbot2_response_text = chatbot2_response.generations[0][0].text.strip()
    
    # Append Chatbot-2's response to its conversation history
    chatbot2_history.append(user_input)
    chatbot2_history.append(chatbot2_response_text)
    
    # Return the response with the name "Ayse"
    return jsonify({"name": "Ayse", "response": chatbot2_response_text})


def generate_response(user_input):
    # Use the local Zephyr model to generate a response based on user input
    response = llm_chatbot.generate([f"User: {user_input}\nChatbot:"], max_tokens=80)
    return response.generations[0][0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)
