import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    MAX_HANZI = 1000
    if request.method == "POST":
        # Get the data input from the form
        data = request.form["data"]
        # Get the format input from the form
        format = request.form["format"]
        # Split the data into chunks of size MAX_HANZI
        data_chunks = [data[i:i + MAX_HANZI] for i in range(0, len(data), MAX_HANZI)]
        # Generate a document with the summarized data in the specified format using OpenAI
        response = ""
        for i, chunk in enumerate(data_chunks):
            # If this is not the first chunk, use the last few tokens from the previous chunk as the starting point
            if i > 0:
                chunk = previous_tokens + chunk
            
            # Send the prompt to OpenAI and get the response
            summary = summarize_data(chunk)
            response += summary

            # Save the last summary from the response for use in the next chunk
            previous_tokens = summary
            
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def summarize_data(data):
    """Summarize the given data using OpenAI.
    
    Args:
        data (str): The raw data to be summarized.
        
    Returns:
        str: The generated summary.
    """
    prompt = "请总结以下数据资料：\n\n{}".format(data)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.3,
        max_tokens=4000
    )
    return response.choices[0].text


def generate_document(data, format):
    """Generate a document with the given data in the specified format using OpenAI.
    
    Args:
        data (str): The raw data to be included in the document.
        format (str): The desired format of the document (e.g. "PDF", "Word", etc.).
        
    Returns:
        str: The generated document.
    """
    prompt = "Please generate a document with the following data in {} format:\n\n{}".format(format, data)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.6,
        max_tokens=4000
    )
    return response.choices[0].text



    