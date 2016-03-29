from flask import Flask, request, render_template, session

import GAService
app = Flask(__name__)

@app.route('/test')
def test():
	try:
		print "------------STARTED-----999-------"
		# service = GAService.googleAuthenticate()
		# print GAService.get_profile_array(service)
		return render_template("test.html")
	except Exception as e:
		print e
		print "-----------ERRRORROROROROR MESSAGE-------------------"

@app.route('/')
def theme_dashboard():
	try:
		print "------------STARTED-----999-------"
		service = GAService.googleAuthenticate()
		if not "profiles" in session:
			session["profiles"] = GAService.get_profile_array(service)
		return render_template("theme_index.html", 
			resultSet = GAService.getDashboardDetails(service, session["profiles"]),
			consolidatedResultSet = GAService.getColumnChartAllControllerPageViews(service, session["profiles"]),
			TimeOnPage = GAService.getTimePerPageForAllControllers(service, session["profiles"]),
			sessionDetails = GAService.getSessionDashboardDetails(service, session["profiles"])
			)
	except Exception as e:
		print e
		print "-----------ERRRORROROROROR MESSAGE-------------------"
@app.route('/controller_dash')
def separate_controller_dashboard():
	try:
		print "------------STARTED-----999-------"
		service = GAService.googleAuthenticate()
		if not "profiles" in session:
			session["profiles"] = GAService.get_profile_array(service)
		return render_template("separate_controller.html", resultSet=GAService.getColumChartSeparateControllerPageViews(service, session["profiles"]))
	except Exception as e:
		print e
		print "-----------ERRRORROROROROR MESSAGE-------------------"

@app.route('/session_dashboard')
def session_dashboard():
	try:
		print "------------STARTED-----999-------"
		service = GAService.googleAuthenticate()
		return render_template("session.html", resultSet = GAService.getSessionDashboardDetails(service))
	except Exception as e:
		print e
		print "-----------ERRRORROROROROR MESSAGE-------------------"

@app.route("/logout")
def logout():
	session.clear()
	return "done"

if __name__ == '__main__':
	app.secret_key = "adfasdftest by aldiua#@F9asdfa/d0asd"
	app.run(host="0.0.0.0", debug=True)