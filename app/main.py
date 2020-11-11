# Import used libraries and packages
import flask
from flask import request, jsonify
import myfitnesspal
from datetime import date
import os
from flask_cors import CORS

# Add user credentials to login on MyFitnesspal
my_username = "demeuem@gmail.com"
my_password = os.environ.get("PASS")

# Create connection with the MyFitnesspal app
client = myfitnesspal.Client(my_username, password=my_password)

# Create the app
app = flask.Flask(__name__)
app.config["DEBUG"] = False
CORS(app)

# -------------- All endpoints below --------------

# Specific day lookup, get all meals for that day
@app.route('/api/v1/entries/day/<year>/<month>/<day>')
def entries_specificday(year, month, day):
    
    # Get all the information for the specific day
    day = client.get_date(year, month, day)
    
    # Filter all information by meal (breakfast, lunch, dinner, snack)
    breakfast = day.meals[0].entries
    lunch = day.meals[1].entries
    dinner = day.meals[2].entries
    snack = day.meals[3].entries

    # Create empty arrays
    breakfast_entries, lunch_entries, dinner_entries, snack_entries = [], [], [], []

    # Create JSON Objects for every meal item
    for item in breakfast: breakfast_entries.append({'gerecht': item.name, 'calories': item.nutrition_information.get('calories')})
    for item in lunch: lunch_entries.append({'gerecht': item.name, 'calories': item.nutrition_information.get('calories')})
    for item in dinner: dinner_entries.append({'gerecht': item.name, 'calories': item.nutrition_information.get('calories')})
    for item in snack: snack_entries.append({'gerecht': item.name, 'calories': item.nutrition_information.get('calories')})
    
    # Merge all meals and items per meal together
    full_day_entries = [{"ontbijt":  breakfast_entries,  "lunch": lunch_entries,
             "dinner": dinner_entries, "snack": snack_entries}]

    # Return JSON
    return jsonify(full_day_entries)

# Specific day lookup, get totals for that day
@app.route('/api/v1/entries/day/totals/<year>/<month>/<day>')
def entries_specificday__totals(year, month, day):

    # Get all the information for the specific day
    day = client.get_date(year, month, day)

    # Filter all information into totals
    totals = day.totals

    # ------- Check if there are totals -------

    # If the totals array is empty, return zero for every value
    if len(totals) == 0:
        day_totals = [{"calories": 0,  'carbohydrates': 0,
                'fat': 0, 'protein': 0, 'sodium': 0, 'sugar': 0}]
    
    # Else, return the totals as an array
    else:
        day_totals = [totals]

    # Return JSON
    return jsonify(day_totals)

# Specific day lookup, get cardio exercise for that day
@app.route('/api/v1/entries/day/exercise/<year>/<month>/<day>')
def entries_specificday_exercise__cardio(year, month, day):

    # Get all the information for the specific day 
    day = client.get_date(year, month, day)

    # Filter all information into cardio exercise
    cardio = day.exercises[0].get_as_list()

    # Return JSON
    return jsonify(cardio)

# Weight lookup since a specific day until now
@app.route('/api/v1/weight/since/<year>/<month>/<day>')
def weight_since_day(year, month, day):

    # Get a start day
    startDay = date(int(year), int(month), int(day))

    # Get all weight measurements since that specific start day
    measurements = client.get_measurements('Weight', startDay)

    # Create object for every item
    measurements = [{'day': day.strftime('%Y-%m-%d'), 'weight': weight} for day, weight in measurements.items()]

    # Return JSON
    return jsonify(measurements)