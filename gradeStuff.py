#!/usr/bin/env python
import sys, os, csv, json, re, httplib2, xlrd
sys.path.insert(0, 'xlsx-to-json')

from xlstojson import xlstojson
from datetime import datetime as dt
from datetime import date
from student import Student
from constants import Constants
from grade import Grade

#Load constants from constants.py
constants = Constants()
extsMap = constants.pointsMap
labCutoffs = constants.labCutoffs
gradebook_columns = {}

# FIXME: we just want to map WUSTL Key to WUSTL Key
def getKeyToUUID():
	#Load dictionary mapping WUSTL key to Schoology UUID
	with open( 'roster.json' ) as roster_file:
		roster = json.load(roster_file)
        # mapLines = map( lambda x: tuple( x.split( ',' ) ), mapLines )
        UUIDmap = {}
        for key in roster:
            UUIDmap[key.lower()] = key.lower()
        
        return UUIDmap

def readWriteData( fileName ):
	#Turn CSV file into JSON file
	try:
		with open(fileName, 'r') as grades:
			with open("jsontemp", 'w') as jsonfile:
				reader = csv.DictReader(grades)
				for row in reader:
					json.dump(row, jsonfile)
					jsonfile.write("\n")
				return jsonfile.name
	except:
		print "Invalid file name"
		sys.exit( 0 )

def readWriteDataExcel( fileName ):
	#Turn xls file into JSON file
    file_path = os.path.realpath(fileName)
	return xlstojson(file_path)
	

def process( thing, fileName ):
	#Initialize empty dict of students, to be filled from JSON file
	count = 0
	studentDict = {}
	uuidMap = getKeyToUUID()
	#Open JSON file
    jsonFile = readWriteDataExcel(fileName)["sheet1"]
	# jsonFile = readWriteData( fileName )
	print "Building initial data structure"
	with open( jsonFile, 'r' ) as f:

		for row in f:
			#Get data from JSON encoded file created by readWriteData
			data = json.loads( row )
			typeOfDemo = data["What are you demoing?"]
			if thing.lower()[0::-1] not in typeOfDemo.lower():
				continue
			#Format time properly
			dateString = data["Timestamp"].split( " " )[0]
			timeString = data["Timestamp"].split( " " )[1]
			dateSplit = dateString.split( "/" )
			if len(dateSplit[2]) < 4:
				dateSplit[2] = "20" + dateSplit[2]
			dateObject = date( int( dateSplit[2] ), int( dateSplit[0] ), int( dateSplit[1] ) ).strftime( "%b %d %Y" )
			try:
				timestamp = dt.strptime( str( dateObject ) + " " + timeString, "%b %d %Y %H:%M:%S" )
			except:
				timestamp = dt.strptime( str( dateObject ) + " " + timeString, "%b %d %Y %H:%M" )
			#Assign other variables
			if typeOfDemo == "Lab":
				typeOfDemo = "Assignment"
			#Fill student dictionary - generalized to handle studio input as well as exts/labs
			wustlKeys = [ str(v) for k, v in data.iteritems() if "Key" in k and not v == "" ]
			assignment = map( lambda x: str( x.split( " - " )[0] ), data[str(typeOfDemo) + " Being Demoed"].split(", ") )
			for wk in wustlKeys:
				if not wk in studentDict.iterkeys():
					try:
						studentDict[wk] = Student( wk, uuidMap[wk] )
					except:
						pass
			#Add all assignments to students
			points = -1
			if typeOfDemo == "Assignment" or typeOfDemo == "Studio":
				points = 1
				for wk in wustlKeys:
					if not wk == "":
						if typeOfDemo == "Assignment":
							typeOfDemo = "Lab"
						g = Grade( assignment[0], points, typeOfDemo, timestamp )
						try:
							print str(g)
							studentDict[wk].addGrade( g )
						except:
							pass
	os.remove( jsonFile )
	#Do grading for right thing
	if thing == "labs":
		print "Doing labs"
		doLabs( studentDict )
	elif thing == "studios":
		print "Doing studios"
		doStudios( studentDict )
	else:
		print "Invalid assignment type."
		sys.exit( 0 )

def doLabs( studentDict ):
	#Calculate late coupon usage
	for k in studentDict.iterkeys():
		curStudent = studentDict[k]
		numLates = curStudent.getLates()
		labs = curStudent.getLabs()
		for lab in labs:
			labDeadline = labCutoffs[lab]
			labSubTime = curStudent.getGrades()[lab].getTimestamp()
			if labSubTime > labDeadline:
				if ( labSubTime - labDeadline ).days > 7:
					studentDict[k].grades[lab].setPoints( 0 )
				else:
					if numLates < 3:
						numLates += 1
					else:
						numLates += 1
						studentDict[k].grades[lab].setPoints( 0 )
		studentDict[k].setLates( numLates )
	#Build lab CSV file for writing
	csvData = []
	headers = [ "WUSTL Key", "Unique User ID" ] + list( labCutoffs.iterkeys() ) + [ "LateLabs" ]
	csvData.append( headers )
	for k in studentDict.iterkeys():
		studentDataRow = []
		curStudent = studentDict[k]
		studentLabs = curStudent.getLabs()
		studentDataRow.append( curStudent.getInfo()[0] )
		studentDataRow.append( curStudent.getInfo()[1] )
		for assignment in headers[2:len( headers )-1]:
			if assignment in studentLabs.iterkeys():
				studentDataRow.append( studentLabs[assignment].getPoints() )
			else:
				studentDataRow.append( 0 )
		studentDataRow.append( curStudent.getLates() )
		csvData.append( studentDataRow )
	#Write lab CSV file
	with open( "labgrades.csv", "w" ) as f:
		print "Writing labgrades.csv"
		csvWriter = csv.writer( f, delimiter="," )
		csvWriter.writerows( csvData )
		print "Done writing labgrades.csv"

def doStudios( studentDict ):
	#Build studio CSV file
	csvData = []
	headers = [ "Unique User ID" ] + [ "Studio " + str(k) for k in range( 1, 11 ) ]
	csvData.append( headers )
	for k in studentDict.iterkeys():
		curStudent = studentDict[k]
		studentDataRow = []
		studentDataRow.append( curStudent.getInfo()[1] )
		studentStudios = curStudent.getStudios()
		for assignment in headers[1::]:
			if assignment in studentStudios.iterkeys():
				studentDataRow.append( studentStudios[assignment].getPoints() )
			else:
				studentDataRow.append( 0 )
		csvData.append( studentDataRow )
	#Write studio CSV file
	with open( "studiogrades.csv", "w" ) as f:
		print "Writing studiogrades.csv"
		csvWriter = csv.writer( f, delimiter="," )
		csvWriter.writerows( csvData )
		print "Done writing studiogrades.csv"

if __name__ == "__main__":
	print "Running"
	# readWriteDataExcel("Studio0(1-61).xlsx")

	args = sys.argv[1::]
	if not len( args ) is 2:
		print "Use two arguments"
		sys.exit( 0 )
	process( args[0], args[1] ) #arg 0 = studio | lab | ext | blah, arg 1 = file to be processed

def doQuizzes( studentDict ):
	pass
