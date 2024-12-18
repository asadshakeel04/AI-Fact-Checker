from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

def fact_check(claim):
    try:
        response = client.chat.completions.create(model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fact checking AI. You will tell whether claims are correct, incorrect, or uncertain."},
                {"role": "user", "content": f"Fact-check the following claim and explain briefly why it is correct, incorrect, or uncertain:\n'{claim}'"}
            ],
            max_tokens=50,
            temperature = 0.2)
        return response.choices[0].message
    except Exception as e:
        return f"Error: {e}"
    
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["text_input"]
        if not user_input:
            result = "Error: No text provided for fact-checking."
        else:
            result = fact_check(user_input)
        return render_template("index.html", result=result, user_input=user_input)
    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
