from flask import *
import time
import re

app = Flask(__name__)


# Define character classes
endingPuctuation = "."


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/essay")
def viewEssay(data):
    return render_template('essay.html', essay=data)

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/favicon.ico'), code=302)

# Backend
@app.route('/submit', methods=['POST'])
def submit():
    inputText = request.form['text']
    #createFile(inputText)

    # Split on page break
    pages = inputText.split("\x0c")
    if len(pages) > 1:
        # Get rid of the first (title) page
        pages.pop(0)
    essay = pages[0]

    finalProduct = ""
    # Split text up
    words = essay.split(" ")
    paragraphs = essay.split("\n")


    # Find quotes (includes pulling out words)
    quoteRegex = r'["“]([^"”]*)["”]'
    quotes = re.findall(quoteRegex, essay)
    for quote in quotes:
        #print(quote)
        print()

    print()
    print()
    print()

    # Find citation and characters around it
    citationRegex = r'["“][^"”]*(.{4}["”][^\)"”]*\).{4})'
    citations = re.findall(citationRegex, essay)
    for citation in citations:
        print(citation)
        print()







    wordCount = len(words)

    for p in paragraphs:
        finalProduct += (p + "<br>")


    return viewEssay(finalProduct)


def createFile(text):
    # Save to file with name of current timestamp
    timestamp = time.time()
    myFile = open("essays/{}.txt".format(timestamp), "w")
    myFile.write(text)
    myFile.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
