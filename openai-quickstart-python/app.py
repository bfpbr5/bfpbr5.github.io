import os

# import openai
from flask import Flask, redirect, render_template, request, url_for, send_from_directory
import promptlayer
promptlayer.api_key = "pl_05337f1031d3847d1ab630cb52132d16"

app = Flask(__name__)
openai = promptlayer.openai
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
            max_tokens=2000
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """请总结以下数据材料:\n\n{}:""".format(
        animal
    )

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run()