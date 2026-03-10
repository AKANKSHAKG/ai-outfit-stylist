from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# ---------------- API KEYS ----------------

RAPID_API_KEY = "ee7328a924msh14393245e3df97bp19437fjsn3c67bcbd30f6"
WEATHER_KEY = "8a6eebc2fa16e7e050c32d20ad11161b"

AMAZON_URL = "https://real-time-amazon-data.p.rapidapi.com/search"


# ---------------- WEATHER FUNCTION ----------------

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"

    res = requests.get(url).json()

    if "main" in res:
        temp = res["main"]["temp"]
        weather = res["weather"][0]["main"]
    else:
        temp = 25
        weather = "Clear"

    return temp, weather


# ---------------- PRODUCT SEARCH ----------------

def search_products(query):

    querystring = {
        "query": query,
        "country": "IN"
    }

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }

    response = requests.get(AMAZON_URL, headers=headers, params=querystring)

    data = response.json()

    products = []

    if "data" in data and "products" in data["data"]:
        results = data["data"]["products"]

        if len(results) > 8:
            products = random.sample(results, 8)
        else:
            products = results

    return products


# ---------------- QUERY GENERATOR ----------------

def generate_query(gender, mood, season):

    styles = ["trendy", "streetwear", "minimalist", "modern", "stylish"]

    style = random.choice(styles)

    queries = {

        "male": {

            "casual": [
                f"{season} casual shirt men",
                f"{season} casual tshirt men",
                f"{season} {style} casual outfit men",
                f"{season} relaxed men fashion",
                f"{season} everyday casual wear men"
            ],

            "party": [
                f"{season} party shirt men",
                f"{season} stylish party outfit men",
                f"{season} club wear men",
                f"{season} night party fashion men",
                f"{season} trendy party wear men"
            ],

            "gym": [
                f"{season} gym workout clothes men",
                f"{season} fitness training outfit men",
                f"{season} activewear men",
                f"{season} sports gym outfit men",
                f"{season} breathable gym clothes men"
            ],

            "formal": [
                f"{season} formal shirt men",
                f"{season} office wear men",
                f"{season} professional outfit men",
                f"{season} business casual men",
                f"{season} corporate attire men"
            ],

            "wedding": [
                f"{season} wedding suit men",
                f"{season} sherwani men",
                f"{season} traditional wedding outfit men",
                f"{season} festive ethnic wear men",
                f"{season} indian wedding fashion men"
            ],

            "beach": [
                f"{season} beach outfit men",
                f"{season} vacation outfit men",
                f"{season} beach shirt men",
                f"{season} tropical summer wear men",
                f"{season} beach casual men"
            ],

            "festival": [
                f"{season} festival outfit men",
                f"{season} ethnic kurta men",
                f"{season} traditional festive wear men",
                f"{season} indian festival clothing men",
                f"{season} festive kurta men"
            ]
        },

        "female": {

            "casual": [
                f"{season} casual dress women",
                f"{season} casual top women",
                f"{season} {style} casual outfit women",
                f"{season} everyday fashion women",
                f"{season} relaxed summer style women"
            ],

            "party": [
                f"{season} party dress women",
                f"{season} cocktail dress women",
                f"{season} stylish party wear women",
                f"{season} night party fashion women",
                f"{season} elegant evening dress women"
            ],

            "gym": [
                f"{season} gym workout outfit women",
                f"{season} fitness activewear women",
                f"{season} yoga outfit women",
                f"{season} sports gym clothes women",
                f"{season} breathable gym wear women"
            ],

            "formal": [
                f"{season} office wear women",
                f"{season} formal outfit women",
                f"{season} professional business attire women",
                f"{season} corporate fashion women",
                f"{season} formal blouse women"
            ],

            "wedding": [
                f"{season} wedding lehenga women",
                f"{season} bridal dress women",
                f"{season} indian wedding outfit women",
                f"{season} festive saree women",
                f"{season} traditional wedding attire women"
            ],

            "beach": [
                f"{season} beach dress women",
                f"{season} vacation outfit women",
                f"{season} summer beachwear women",
                f"{season} tropical beach fashion women",
                f"{season} beach casual dress women"
            ],

            "festival": [
                f"{season} festival outfit women",
                f"{season} ethnic kurti women",
                f"{season} festive saree women",
                f"{season} traditional indian wear women",
                f"{season} festive ethnic dress women"
            ]
        }

    }

    return random.choice(queries[gender][mood])


# ---------------- MAIN ROUTE ----------------

@app.route("/", methods=["GET", "POST"])
def home():

    products = []
    weather = None
    temp = None
    maps_query = None

    if request.method == "POST":

        gender = request.form["gender"]
        mood = request.form["mood"]
        city = request.form["city"]

        temp, weather = get_weather(city)

        if temp < 18:
            season = "winter"
        elif temp < 28:
            season = "mild"
        else:
            season = "summer"

        query = generate_query(gender, mood, season)

        products = search_products(query)

        maps_query = f"clothing stores near {city}"

    return render_template(
        "index.html",
        products=products,
        weather=weather,
        temp=temp,
        maps_query=maps_query
    )


if __name__ == "__main__":
    app.run(debug=True)