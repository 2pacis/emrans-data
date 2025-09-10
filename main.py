from flask import Flask, request, render_template_string
import requests
import datetime
import random
import string

app = Flask(__name__)

# HTML-Seite mit großer Warnung
html_page = """
<!DOCTYPE html>
<html>
<head>
  <title>IP Logger Tool</title>
</head>
<body>
  <h1 style="color:red;">ACHTUNG!</h1>
  <p>Mit Klick auf den Button stimme ich zu, dass deine öffentliche IP, Standort (ungefähr) und Browserinfos gespeichert werden!</p>
  <form method="POST">
    <button type="submit">Zustimmen</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Besucher-IP ermitteln
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)

        # GeoIP-Daten abfragen
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        city = geo.get("city", "Unbekannt")
        region = geo.get("regionName", "Unbekannt")
        country = geo.get("country", "Unbekannt")
        lat = geo.get("lat", "Unbekannt")
        lon = geo.get("lon", "Unbekannt")

        user_agent = request.headers.get("User-Agent")
        timestamp = datetime.datetime.now().isoformat()

        # Loggen in Textdatei
        with open("logs.txt", "a") as f:
            f.write(f"{timestamp} | IP: {ip} | Stadt: {city} | Region: {region} | Land: {country} | Lat: {lat} | Lon: {lon} | User-Agent: {user_agent}\n")

        # Google Maps Link erzeugen
        map_link = f"https://www.google.com/maps?q={lat},{lon}"

        return f"""
        Danke!<br>
        IP: {ip}<br>
        Stadt: {city}<br>
        Region: {region}<br>
        Land: {country}<br>
        Latitude: {lat}<br>
        Longitude: {lon}<br>
        <a href='{map_link}' target='_blank'>Standort auf Google Maps ansehen</a>
        """

    return render_template_string(html_page)

if __name__ == "__main__":
    # 0.0.0.0 → Server für alle im Netzwerk erreichbar
    app.run(host="0.0.0.0", port=5000)
