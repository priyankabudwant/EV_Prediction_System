from flask import Flask, render_template, request
from models.predict import predict_ev_growth

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    year = int(request.form["year"])
    category = request.form["category"]

    result = predict_ev_growth(year, category)

    return render_template("index.html", prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
