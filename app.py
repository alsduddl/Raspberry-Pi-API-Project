from flask import Flask, render_template, request
import requests  # pip install requests
from urllib.parse import urlencode, unquote
import json
import csv
from dotenv import load_dotenv
import os

load_dotenv()
myWeatherKey = os.environ.get("WEATHER_FORECAST_KEY")
print(myWeatherKey)

app = Flask(__name__)  # Initialise app


def getWeather(sido_name):
    url = "http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureSidoLIst"
    queryString = "?" + urlencode(
        {
            "serviceKey": unquote(myWeatherKey),
            "pageNo": "1",
            "numOfRows": "10",
            "returnType": "JSON",
            "sidoName": sido_name,
            "searchCondition": "DAILY",
        }
    )
    response = requests.get(url + queryString)
    r_dict = json.loads(response.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_item = r_body.get("items")

    for item in r_item:
        time = item.get("dataTime")
        pm10 = item.get("pm10Value")  # 미세먼지 pm10Value
        pm25 = item.get("pm25Value")  # 초미세먼지 pm25Value
        break
    return time, pm10, pm25


@app.route("/", methods=["GET", "POST"])
def index():
    sido_name = ""
    if request.method == "POST":
        sido_name = request.form.get("sido_name")
        time, pm10, pm25 = getWeather(sido_name)

        if sido_name == None:
            return render_template("index.html", error_message="City ID를 다시 입력하세요")

        return render_template(
            "index.html",
            sido_name=sido_name,
            time=time,
            pm10=pm10,
            pm25=pm25,
        )
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
