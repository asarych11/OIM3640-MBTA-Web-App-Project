from flask import Flask, render_template, request
from mbta_helper import find_stop_near, get_predictions_for_stop

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place = request.form.get("place")

    if not place:
        return render_template("error.html", message="No location provided.")

    stop_name, is_accessible, stop_id = find_stop_near(place)

    if stop_name == "No stop found":
        return render_template("error.html", message=f"No MBTA stop found near '{place}'.")

    departure_time = get_predictions_for_stop(stop_id)

    return render_template(
        "mbta_station.html",
        place=place,
        stop=stop_name,
        accessible=is_accessible,
        departure_time=departure_time or "Unavailable"
    )

if __name__ == "__main__":
    app.run(debug=True)
