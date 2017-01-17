from action import Action
import sys
import sqlite3
import time
from datetime import datetime

# ACTION HANDLER FUNCTIONS
def helpHandler(actions):
	for a in actions:
		print ("name: ", a.name, "\n\tshortcut: ", a.shortcut, "\n\tdescription: ", a.description)

def exitHandler(args):
	sys.exit(0)





CLOCKEDFILE = "clocked_in_status"

# ACTION HANDLER CLASS
class ActionHandler:
	def __init__(self, job):
		# self.connection = sqlite3.connect("trackedHours.db", detect_types=sqlite3.PARSE_DECLTYPES)
		self.connection = sqlite3.connect("trackedHours.db", detect_types=sqlite3.PARSE_DECLTYPES)

		self.cursor = self.connection.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY NOT NULL, employer VARCHAR(255) UNIQUE, totalHours timestamp, position VARCHAR(255) DEFAULT 'Awesome Person')")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS hours (id INTEGER  PRIMARY KEY NOT NULL, clockIn timestamp UNIQUE, clockOut timestamp, hours timestamp, job_id INTEGER NOT NULL, FOREIGN KEY (job_id) REFERENCES JOBS(id))")
		self.connection.commit()
		self.cursor.execute("SELECT id FROM jobs WHERE employer=?", (job,))
		inputtedJob = self.cursor.fetchone()
		if inputtedJob is None:
			self.cursor.execute("INSERT INTO jobs (employer) VALUES (?)", (job,))
			self.connection.commit()
			self.cursor.execute("SELECT id FROM jobs WHERE employer=?", (job,))
			self.job = self.cursor.fetchone()[0]
			# print("this sis the new job: ", self.job)
		else:
			# print("this is the inputted job_id", inputtedJob)
			self.job = inputtedJob[0]
		# print(self.job)
		self.getClockedinStatus()
		self.actions = []
		self.actions.append(Action("help", "-h", "gives a description of each action you can take", helpHandler))
		self.actions.append(Action("exit", "-ex", "exits program", exitHandler))
		self.actions.append(Action("clockin", "-ci", "Inserts a new hour and sets the starting time. Uses the current employer", self.clockInHandler))
		self.actions.append(Action("clockout", "-co", "Udates the current clockedin hour and resets it, or sends an error if there isn't a current clocked in session", self.clockOutHandler))

	def __del__(self):
		self.connection.close()

	def getClockedinStatus(self):
		status = ""
		try:
			with open(CLOCKEDFILE, "r") as clockedInFile:
				status = clockedInFile.read()
		except Exception as e:
			pass

		# print(status)
		if status != "":
			 self.clockedIn = status
		else:
			self.clockedIn = None
		# print(self.clockedIn)


	def callAction(self, args):
		actionCalled = False
		for a in self.actions:
			#print(a.name, a.shortcut)
			if args[0] == a.name or args[0] == a.shortcut:
				if a.name == "help":
					args = self.actions
				a.action(args)
				actionCalled = True
				break
		if not actionCalled:
			print("ERROR: ", args[0], " is not a valid command")

	def clockInHandler(self, args):
		if self.clockedIn is None:
				if self.job is not None:
					# now = datetime.now()
					# print(now)
					self.cursor.execute("INSERT INTO hours (clockIn, job_id) VALUES (?,?)", (datetime.now(), self.job))
					self.connection.commit()

					self.clockedIn = self.cursor.lastrowid
					with open(CLOCKEDFILE, "w") as statusFile:
						statusFile.write(str(self.clockedIn))
				else:
					print("ERROR: you are currently don't have an employer set. please set an employer and try again.")
		else:
			print("ERROR: You are already clocked in")

	def clockOutHandler(self, args):
		if self.clockedIn is not None:
			self.cursor.execute("UPDATE hours SET clockOut=? where id=?",  (datetime.now(), self.clockedIn))
			self.connection.commit()
			self.clockedIn = None
			with open(CLOCKEDFILE, "w") as statusFile:
				statusFile.write("")
		else:
			print("ERROR: you haven't clocked in yet.")
