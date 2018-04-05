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
    # If there are multiple page breaks, we assume it's a bibliography
    essay = pages[0]

    finalProduct = ""


    # Find quotes (includes pulling out words)
    quoteRegex = r'(["“][^"”]*["”])'
    quotes = re.findall(quoteRegex, essay)
    # Highlight all quotes
    for quote in quotes:
        pos = essay.find(quote)
        quoteLength = len(quote)
        # Insert quote with highlight
        #essay = essay[:pos] + "<span class='redBox'>" + quote + "</span>" + essay[pos+quoteLength:]

    # Find citation and characters around it
    anyCitationRegex = r'["“][^"”]*(.{4}[\)"”].*[\)"”].{4})'
    correctCitationRegex = r'([^\.]["”]\s\(\D*\d+\)\.)'
    citations = re.findall(anyCitationRegex, essay)
    for citation in citations:
        if re.search(correctCitationRegex, citation) is None:
            essay = highlight(citation, essay, "red")
        else:
            essay = highlight(citation, essay, "green")


    # Split text up
    words = essay.split(" ")
    paragraphs = essay.split("\n")

    wordCount = len(words)
    # Paragraphs[0] is \r, end of paragraphs are \r
    thesis = paragraphs[1].split(".")[-2]


    for p in paragraphs:
        finalProduct += (p + "<br><br>")

    #print(finalProduct)

    # TODO: add info to database for analysis

    return viewEssay(finalProduct)


def createFile(text):
    # Save to file with name of current timestamp
    timestamp = time.time()
    myFile = open("essays/{}.txt".format(timestamp), "w")
    myFile.write(text)
    myFile.close()

def highlight(s, essay, color):
    pos = essay.find(s)
    sLen = len(s)
    essay = essay[:pos] + "<span class='" + color + "Box'>" + s + "</span>" + essay[pos+sLen:]
    return essay


if __name__ == "__main__":
    app.run(host='0.0.0.0')
