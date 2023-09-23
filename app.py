from flask import Flask, jsonify, request, Response
from scraping import scrapeData
from translation import translateData

app = Flask(__name__)


@app.route("/trigger", methods=["GET"])
def triggerScraping():
    status = 200
    try:
        if(request.method == "GET"):
            scrapeData()
            translateData()
        return Response(200)
    except:
        return Response(500)


if __name__ == "__main__":
    app.run(debug=True)
