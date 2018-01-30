__author__ = 'schneidera'
from flask import Flask, render_template, request, jsonify
import psycopg2
import psqlConfig as config
import sys

app = Flask(__name__)

"""The approute is empty because this is the homepage. The option to search the
entire dataset is available at the homepage and if used it will take you to the
general search option"""
@app.route('/')
def homePage():
	return render_template('mainView.html')

"""This approute takes the user to the README.html page where information about
the site is displayed."""
@app.route('/README')
def readMe():
	return render_template('README.html')

"""This is because I could figure out how to link to a file"""
@app.route('/format')
def format():
	return render_template('format-eva.html')

"""The general search will query the entire dataset and return a list containing
the relevant EVA numbers."""
@app.route('/generalSearch', methods = ['POST'])
def generalSearch():
	if request.method == 'POST':
		query = str(request.form['query'])
		return render_template('resultsView.html', eva = _generalSearch(query), query = query)

def _generalSearch(query):
	try:
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
	except Exception as e:
		print(e)
		exit()
	try:
		cursor = connection.cursor()

		queryBeggining = "SELECT * FROM eva WHERE crew=%s OR vehicle=%s OR country=%s"

		cursor.execute(queryBeggining, (query, query, query))
	except Exception as e:
		print('cursor error: ', e)
		connection.close()
		exit()

	toReturn = []
	for row in cursor:
		toReturn.append(row)

	final = []
	for i in range(len(toReturn)):
		line = toReturn[i]
		final.append({'evanumber': line[0], 'country': line[1], 'crewmembers': line[2], 'vehicle': line[3], 'missiondate': line[4], 'duration': line[5], 'purpose': line[6]})

	connection.close()
	return final

"""given. You could search by crew members, vehicle used, duration, date, and
country. The advanced search method doesn't require any input but it pass input
to one of a few specific search methods."""
@app.route('/advanced')
def advanced():
	return render_template('advancedView.html')

"""This simply searches by the crew category for any instance of the crewMember
parameter. Returns a list of relevant EVA numbers."""
@app.route('/crew', methods = ['POST'])
def getCrew():
	if request.method == 'POST':
		crewMember = str(request.form['crewMember'])
		return render_template('resultsView.html', eva = _getCrew(crewMember), query = crewMember)

def _getCrew(crewMember):
	try:
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
	except Exception as e:
		print(e)
		exit()
	try:
		cursor = connection.cursor()
		queryBeggining = "SELECT * FROM eva WHERE crew=%s"
		cursor.execute(queryBeggining, (crewMember, ))
	except Exception as e:
		print('cursor error: ', e)
		connection.close()
		exit()

	toReturn = []
	for row in cursor:
		toReturn.append(row)

	final = []
	for i in range(len(toReturn)):
		line = toReturn[i]
		final.append({'evanumber': line[0], 'country': line[1], 'crewmembers': line[2], 'vehicle': line[3],
		'missiondate': line[4], 'duration': line[5], 'purpose': line[6]})

	connection.close()

	return final

"""This returns a list of instances of the vehicle parameter in the vehicle column."""
@app.route('/vehicle', methods = ['POST'])
def getVehicle():
	if request.method == 'POST':
		vehicle = str(request.form['vehicle'])
		return render_template('resultsView.html', eva = _getVehicle(vehicle), query = vehicle)

def _getVehicle(vehicle):
	try:
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
	except Exception as e:
		print(e)
		exit()
	try:
		cursor = connection.cursor()
		queryBeggining = "SELECT * FROM eva WHERE vehicle=%s"
		cursor.execute(queryBeggining, (vehicle, ))
	except Exception as e:
		print('cursor error: ', e)
		connection.close()
		exit()

	toReturn = []
	for row in cursor:
		toReturn.append(row)

	final = []
	for i in range(len(toReturn)):
		line = toReturn[i]
		final.append({'evanumber': line[0], 'country': line[1], 'crewmembers': line[2], 'vehicle': line[3],
		'missiondate': line[4], 'duration': line[5], 'purpose': line[6]})

	connection.close()

	return final

"""This returns a list of any instances of the duration parameter."""
@app.route('/duration', methods = ['POST'])
def getDuration():
	if request.method == 'POST':
		duration = str(request.form['duration'])
		if len(duration.split(':')) != 3:
			return render_template('resultsView.html', query = duration, invalid = 'Invalid search query. Please format durations as hours:minutes:seconds.')
		else:
			return render_template('resultsView.html', eva = _getDuration(duration), query = duration)

def _getDuration(duration):
	try:
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
	except Exception as e:
		print(e)
		exit()
	try:
		cursor = connection.cursor()
		queryBeggining = "SELECT * FROM eva WHERE duration=%s"
		cursor.execute(queryBeggining, (duration, ))
	except Exception as e:
		print('cursor error: ', e)
		connection.close()
		exit()

	toReturn = []
	for row in cursor:
		toReturn.append(row)

	final = []
	for i in range(len(toReturn)):
		line = toReturn[i]
		final.append({'evanumber': line[0], 'country': line[1], 'crewmembers': line[2], 'vehicle': line[3],
		'missiondate': line[4], 'duration': line[5], 'purpose': line[6]})

	connection.close()

	return final

"""This returns a lists of all instances of the duration parameter between durationOne and
durationTwo."""
@app.route('/twoDurations', methods = ['POST'])
def getBetweenDurations():
	if request.method == 'POST':
		durationOne = str(request.form['durationOne'])
		durationTwo = str(request.form['durationTwo'])
		if len(durationOne.split(":")) != 3 or len(durationTwo.split(":")) != 3:
			return render_template('twoResultsView.html', query = durationOne, invalid = 'Invalid search query. Please format durations as hours:minutes:seconds.')
		else:
			return render_template('twoResultsView.html', eva = _getBetweenDurations(durationOne, durationTwo),
					       query = durationOne, queryTwo = durationTwo)

def _getBetweenDurations(durationOne, durationTwo):
	try:
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
	except Exception as e:
		print(e)
		exit()
	try:
		cursor = connection.cursor()
		queryBeggining = 'SELECT * FROM eva WHERE duration BETWEEN %s AND %s'
		cursor.execute(queryBeggining, (durationOne, durationTwo))
	except Exception as e:
		print('cursor error: ', e)
		connection.close()
		exit()

	toReturn = []
	for row in cursor:
		toReturn.append(row)

	final = []
	for i in range(len(toReturn)):
		line = toReturn[i]
		final.append({'evanumber': line[0], 'country': line[1], 'crewmembers': line[2], 'vehicle': line[3],
		'missiondate': line[4], 'duration': line[5], 'purpose': line[6]})

	connection.close()

	return final


"""This returns a list of any instances of the date parameter."""
@app.route('/date', methods = ['POST'])
def getDate():
	if request.method == 'POST':
		date = str(request.form['date'])
		if len(date.split('/')) != 3 and len(date.split('-')) != 3:
			return render_template('resultsView.html', query = date, invalid = 'Invalid search query. Please format dates as month/day/year or year-month-day.')
		else:
			return render_template('resultsView.html', eva = _getDate(date), query = date)

def _getDate(date):
	try:
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
	except Exception as e:
		print(e)
		exit()
	try:
		cursor = connection.cursor()
		queryBeggining = "SELECT * FROM eva WHERE missiondate=%s"
		cursor.execute(queryBeggining, (date, ))
	except Exception as e:
		print('cursor error: ', e)
		connection.close()
		exit()

	toReturn = []
	for row in cursor:
		toReturn.append(row)

	final = []
	for i in range(len(toReturn)):
		line = toReturn[i]
		final.append({'evanumber': line[0], 'country': line[1], 'crewmembers': line[2], 'vehicle': line[3],
		'missiondate': line[4], 'duration': line[5], 'purpose': line[6]})

	connection.close()

	return final

"""This returns a list of all instances of the date parameter between dateOne and
dateTwo."""
@app.route('/twoDates', methods = ['POST'])
def getBetweenDates():
	if request.method == 'POST':
		dateOne = str(request.form['dateOne'])
		dateTwo = str(request.form['dateTwo'])
		if len(dateOne.split('/')) != 3 and len(dateOne.split('-')) != 3 or len(dateTwo.split('/')) != 3 and len(dateTwo.split('-')) != 3:
			return render_template('twoResultsView.html', query = dateOne, queryTwo = dateTwo,
					       invalid = 'Invalid search query. Please format dates as month/day/year or year-month-day.')
		else:
			return render_template('twoResultsView.html', eva = _getBetweenDates(dateOne, dateTwo),
					       query = dateOne, queryTwo = dateTwo)

def _getBetweenDates(dateOne, dateTwo):
	try:
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
	except Exception as e:
		print(e)
		exit()
	try:
		cursor = connection.cursor()
		queryBeggining = "SELECT * FROM eva WHERE missiondate BETWEEN %s AND %s"
		cursor.execute(queryBeggining, (dateOne, dateTwo))
	except Exception as e:
		print('cursor error: ', e)
		connection.close()
		exit()

	toReturn = []
	for row in cursor:
		toReturn.append(row)

	final = []
	for i in range(len(toReturn)):
		line = toReturn[i]
		final.append({'evanumber': line[0], 'country': line[1], 'crewmembers': line[2], 'vehicle': line[3],
		'missiondate': line[4], 'duration': line[5], 'purpose': line[6]})

	connection.close()

	return final


"""This returns a list of any instances of the country parameter. This is arguably the
least useful search option because the only two options are Russia and the USA
but we thought it should be included for completeness."""
@app.route('/country', methods = ['POST'])
def getCountry():
	if request.method == 'POST':
		country = request.form['country']
		return render_template('resultsView.html', eva = _getCountry(country), query = country)

def _getCountry(country):
	try:
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
	except Exception as e:
		print(e)
		exit()
	try:
		cursor = connection.cursor()
		queryBeggining = 'SELECT * FROM eva WHERE country=%s'
		cursor.execute(queryBeggining, (country, ))
	except Exception as e:
		print('cursor error: ', e)
		connection.close()
		exit()

	toReturn = []
	for row in cursor:
		toReturn.append(row)

	final = []
	for i in range(len(toReturn)):
		line = toReturn[i]
		final.append({'evanumber': line[0], 'country': line[1], 'crewmembers': line[2], 'vehicle': line[3],
		'missiondate': line[4], 'duration': line[5], 'purpose': line[6]})

	connection.close()

	return final

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
