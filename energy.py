from flask import Flask, render_template
import requests
from datetime import datetime
import csv

# indstring = ""
# current_fuel =[]
# response = requests.get('https://api.carbonintensity.org.uk/regional/scotland')
# pie = response.json()["data"][0]["data"][0]
# for i in pie["generationmix"]:
# 	current_fuel.append(i)
# indstring += "<ul>"
# for i in current_fuel:
# 	indstring = indstring + "<li>" + str(i["fuel"].capitalize()) + ": " + str(i["perc"]) +"%"+ "</li>"
# indstring += "</ul"
# print(indstring)
app = Flask(__name__)
def dataLogger():
	dt = datetime.now()
	new_data =[]
	# get current fuel mix through API
	response = requests.get('https://api.carbonintensity.org.uk/regional/scotland')
	# get relevant data from retrieved data
	pie = response.json()["data"][0]["data"][0]
	for i in pie["generationmix"]:
		dat = []
		dat.append(i["fuel"])
		dat.append(i["perc"])
		new_data.append(dat)
	# # empty list for previously recorded data
	data=[]
	# get data from up data file where previous data is stored.
	with open("updated_data.csv", "r") as f:
		reader = csv.reader(f)
		# add to old_data list
		for i in reader:
			data.append(i)
	# add date time to first row in list
	dt = datetime.now()
	data[0].append(str(dt))
	# Go through new data, and compare with old data, if fuel type matches then adds number to list
	for i in data:
		for x in new_data:
			if i[0] == x[0]:
				i.append(x[1])
	# just finished going through the old and new data, and have now added this to new list.
	# NEXT - need to write new data to csv

	new_file = csv.writer(open("updated_data.csv", "w"))
	for i in data:
		new_file.writerow(i)
	print("Data logged at", dt.time(), "on ", dt.date())
	print(data)
	return new_file

def fuelMix():
	dt = datetime.now()

	indstring = "Date: " + str(dt.strftime("%d %B %Y")) + "<br>Time: " + str(dt.strftime("%H:%M:%S")) + "\n\n\n<ul>\n\t"
	current_fuel =[]
	# perc = []
	response = requests.get('https://api.carbonintensity.org.uk/regional/scotland')
	pie = response.json()["data"][0]["data"][0]
	for i in pie["generationmix"]:
		current_fuel.append(i)
	for i in current_fuel:
		indstring = indstring + "<li>"+str(i["fuel"].capitalize()) + ": \t" + str(i["perc"]) +"%</li>\n\t"
	indstring += "</ul>"
	# for i in current_fuel:
	# 	perc.append(i["perc"])
	# nstring = """
	# 		<div>
	# 			<ul>
	# 			  <li>Biomass: \t{0}%</li>
	# 			  <li>Coal: \t{1}%</li>
	# 			  <li>Imports: \t{2}%</li>
	# 			  <li>Gas: \t{3}%</li>
	# 			  <li>Nuclear: \t{4}%</li>
	# 			  <li>Other: \t{5}%</li>
	# 			  <li>Hydro: \t{6}%</li>
	# 			  <li>Solar: \t{7}%</li>
	# 			  <li>Wind: \t{8}%</li>
	# 			</ul>
	# 			not this
	# 		</div>

	# 		""".format(*perc)
	return indstring



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/fuel")
def fuel():
    return render_template("fuel.html")

@app.route("/fuelmix")
def fuelmix():
    return render_template("fuelmix.html", data = dataLogger(), script = fuelMix())


if __name__ == "__main__":
    app.run(debug=True)
