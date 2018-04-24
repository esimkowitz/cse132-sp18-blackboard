from datetime import datetime, timedelta
from pytz import timezone
import sys, os, traceback

                
class Constants:

    #Section 1 cutoff at 2:40pm on lab due day, extra 10 min for leeway
    #Section 2 cutoff at 4:10pm on lab due day, extra 10 min for leeway
    #Section 3 cutoff at 5:40pm on lab due day, extra 10 min for leeway

    tz = timezone("US/Central")

    labCutoffs = {
        "a": {
            "Assignment 0"	:	datetime.strptime("Aug 01 2030 17:45:00", "%b %d %Y %H:%M:%S"),
            "Assignment 1"	:	datetime.strptime("Jan 31 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 2"	:	datetime.strptime("Feb 07 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 3"	:	datetime.strptime("Feb 21 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 5"	:	datetime.strptime("Feb 28 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 6"	:	datetime.strptime("Mar 07 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 7"	:	datetime.strptime("Mar 21 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 8"	:	datetime.strptime("Apr 04 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 10"	:	datetime.strptime("Apr 11 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 11":   datetime.strptime("Apr 18 2018 14:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 12":   datetime.strptime("Apr 25 2018 14:40:00", "%b %d %Y %H:%M:%S")
        },
        "b": {
            "Assignment 0"	:	datetime.strptime("Aug 01 2030 17:45:00", "%b %d %Y %H:%M:%S"),
            "Assignment 1"	:	datetime.strptime("Jan 31 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 2"	:	datetime.strptime("Feb 07 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 3"	:	datetime.strptime("Feb 21 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 5"	:	datetime.strptime("Feb 28 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 6"	:	datetime.strptime("Mar 07 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 7"	:	datetime.strptime("Mar 21 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 8"	:	datetime.strptime("Apr 04 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 10"	:	datetime.strptime("Apr 11 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 11":   datetime.strptime("Apr 18 2018 16:10:00", "%b %d %Y %H:%M:%S"),
            "Assignment 12":   datetime.strptime("Apr 25 2018 16:10:00", "%b %d %Y %H:%M:%S")
        }, 
        "c": {
            "Assignment 0"	:	datetime.strptime("Aug 01 2030 17:45:00", "%b %d %Y %H:%M:%S"),
            "Assignment 1"	:	datetime.strptime("Jan 31 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 2"	:	datetime.strptime("Feb 07 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 3"	:	datetime.strptime("Feb 21 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 5"	:	datetime.strptime("Feb 28 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 6"	:	datetime.strptime("Mar 07 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 7"	:	datetime.strptime("Mar 21 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 8"	:	datetime.strptime("Apr 04 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 10"	:	datetime.strptime("Apr 11 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 11":   datetime.strptime("Apr 18 2018 17:40:00", "%b %d %Y %H:%M:%S"),
            "Assignment 12":   datetime.strptime("Apr 25 2018 17:40:00", "%b %d %Y %H:%M:%S")
        }
    }

    # Uncomment below if it's after daylight savings 
    for period in labCutoffs:
        for k in labCutoffs[period].iterkeys():
            labCutoffs[period][k] = tz.localize(labCutoffs[period][k])
        # labCutoffs[period] = handleDST(labCutoffs[period])
    
    labNumLateDays = {
        "Assignment 1"	:	7,
        "Assignment 2"	:	7,
        "Assignment 3"	:	7,
        "Assignment 5"	:	7,
        "Assignment 6"	:	14,
        "Assignment 7"	:	7,
        "Assignment 8"	:	7,
        "Assignment 10"	:	7,
        "Assignment 11"	:	7,
        "Assignment 12":   7,
        "Assignment 0":   7
    }


    column_ids = {
        "Assignment 1"	:	"Assignment 1 [Total Pts: 100.00000 Score] |1271854",
        "Assignment 2"	:	"Assignment 2 [Total Pts: 100.00000 Score] |1271872",
        "Assignment 3"	:	"Assignment 3 [Total Pts: 100.00000 Score] |1271871",
        "Assignment 5"	:	"Assignment 5 [Total Pts: 100.00000 Score] |1271870",
        "Assignment 6"	:	"Assignment 6 [Total Pts: 100.00000 Score] |1271869",
        "Assignment 7"	:	"Assignment 7 [Total Pts: 100.00000 Score] |1271868",
        "Assignment 8"	:	"Assignment 8 [Total Pts: 100.00000 Score] |1271867",
        "Assignment 10"	:	"Assignment 10 [Total Pts: 100.00000 Score] |1271866",
        "Assignment 11"	:	"Assignment 11 [Total Pts: 100.00000 Score] |1271865",
        "Assignment 12" :   "Assignment 12 [Total Pts: 100.00000 Score] |1271864",
        "Assignment 0"  :   "0000000",
        "Studio 0"      :   "Studio 0 [Total Pts: 1.00000 Score] |1272336",
        "Studio 1"      :   "Studio 1 [Total Pts: 1.00000 Score] |1272335",
        "Studio 2"      :   "Studio 2 [Total Pts: 1.00000 Score] |1272334",
        "Studio 3"      :   "Studio 3 [Total Pts: 1.00000 Score] |1272333",
        "Studio 4"      :   "Studio 4 [Total Pts: 1.00000 Score] |1272332",
        "Studio 5"      :   "Studio 5 [Total Pts: 1.00000 Score] |1272331",
        "Studio 6"      :   "Studio 6 [Total Pts: 1.00000 Score] |1272330",
        "Studio 7"      :   "Studio 7 [Total Pts: 1.00000 Score] |1272329",
        "Studio 8"      :   "Studio 8 [Total Pts: 1.00000 Score] |1272328",
        "Studio 10"     :   "Studio 10 [Total Pts: 1.00000 Score] |1272327",
        "Studio 11"     :   "Studio 11 [Total Pts: 1.00000 Score] |1272326",
        "Studio 12"     :   "Studio 12 [Total Pts: 1.00000 Score] |1272325",
        "Lates"         :   "Late Assignments [Total Pts: 15.00000 Score] |1288165"
    }

    maxScore = {
        "Assignment 1"	:	100.0,
        "Assignment 2"	:	100.0,
        "Assignment 3"	:	100.0,
        "Assignment 5"	:	100.0,
        "Assignment 6"	:	100.0,
        "Assignment 7"	:	100.0,
        "Assignment 8"	:	100.0,
        "Assignment 10"	:	100.0,
        "Assignment 11"	:	100.0,
        "Assignment 12" :   100.0,
        "Assignment 0"  :   0.0
    }


    # Constants relating to parsing lab grade submissions
    labNames = [
        "Assignment 0",
        "Assignment 1",
        "Assignment 2",
        "Assignment 3",
        "Assignment 5",
        "Assignment 6",
        "Assignment 7",
        "Assignment 8",
        "Assignment 10",
        "Assignment 11",
        "Assignment 12"
    ]
    labRubricUpToDate = {
        "Assignment 0": False,
        "Assignment 1": True,
        "Assignment 2": True,
        "Assignment 3": True,
        "Assignment 5": True,
        "Assignment 6": True,
        "Assignment 7": True,
        "Assignment 8": True,
        "Assignment 10": True,
        "Assignment 11": False,
        "Assignment 12": False
    }
    labPartnerFields = {
        "Assignment 1"	:	["Partner 1 WUSTL ID (the 6 digit number)", "Partner 2 WUSTL ID (the 6-digit number)"],
        "Assignment 2"	:	["Partner 1 WUSTL ID (the 6 digit number)", "Partner 2 WUSTL ID (the 6-digit number)"],
        "Assignment 3"	:	["Partner 1 WUSTL ID (the 6 digit number)", "Partner 2 WUSTL ID (the 6 digit number)"],
        "Assignment 5"	:	["Partner 1 WUSTL ID (the 6 digit number)", "Partner 2 WUSTL ID (the 6 digit number)"],
        "Assignment 6"	:	["Partner 1 WUSTL ID (the 6 digit number)", "Partner 2 WUSTL ID (the 6 digit number)"],
        "Assignment 7"	:	["Partner 1 WUSTL ID (the 6 digit number)", "Partner 2 WUSTL ID (the 6 digit number)"],
        "Assignment 8"	:	["Partner 1 WUSTL ID (the 6 digit number)", "Partner 2 WUSTL ID (the 6 digit number)"],
        "Assignment 10"	:	["Partner 1 WUSTL ID (the 6 digit number)", "Partner 2 WUSTL ID (the 6 digit number)"],
        "Assignment 11"	:	["", ""],
        "Assignment 12" :   ["", ""],
        "Assignment 0"  :   ["", ""]
    }
    labWorkingWithPartner = {
        "Assignment 1"	:	"Are they working with a partner?",
        "Assignment 2"	:	"Are they working with a partner?",
        "Assignment 3"	:	"Are they working with a partner?",
        "Assignment 5"	:	"Are they working with a partner?",
        "Assignment 6"	:	"Are they working with a partner?",
        "Assignment 7"	:	"Are they working with a partner?",
        "Assignment 8"	:	"Are they working with a partner?",
        "Assignment 10"	:	"Are they working with a partner?",
        "Assignment 11"	:	"",
        "Assignment 12" :   "",
        "Assignment 0"  :   ""
    }
    labCommitToGithub = {
        "Assignment 1"	:	"Commit to Github",
        "Assignment 2"	:	"Committed to Github before demo",
        "Assignment 3"	:	"Committed to Github before demo",
        "Assignment 5"	:	"Committed to Github before demo",
        "Assignment 6"	:	"Committed to Github before demo",
        "Assignment 7"	:	"Committed to Github before demo",
        "Assignment 8"	:	"Committed to Github before demo",
        "Assignment 10"	:	"Committed to Github before demo",
        "Assignment 11"	:	"",
        "Assignment 12" :   "",
        "Assignment 0"  :   ""
    }
    labTAName = {
        "Assignment 1"	:	"Name",
        "Assignment 2"	:	"Name",
        "Assignment 3"	:	"Name",
        "Assignment 5"	:	"Name",
        "Assignment 6"	:	"Name",
        "Assignment 7"	:	"Name",
        "Assignment 8"	:	"Name",
        "Assignment 10"	:	"Name",
        "Assignment 11"	:	"Name",
        "Assignment 12" :   "Name",
        "Assignment 0"  :   "Name"
    }
    labStartTime = {
        "Assignment 1"	:	"Start time",
        "Assignment 2"	:	"Start time",
        "Assignment 3"	:	"Start time",
        "Assignment 5"	:	"Start time",
        "Assignment 6"	:	"Start time",
        "Assignment 7"	:	"Start time",
        "Assignment 8"	:	"Start time",
        "Assignment 10"	:	"Start time",
        "Assignment 11"	:	"Start time",
        "Assignment 12" :   "Start time",
        "Assignment 0"  :   "Start time"
    }
    labNotes = {
        "Assignment 1"	:	"",
        "Assignment 2"	:	"Comments/Notes",
        "Assignment 3"	:	"Comments/Notes",
        "Assignment 5"	:	"Comments/Notes",
        "Assignment 6"	:	"Comments/Notes",
        "Assignment 7"	:	"Comments/Notes",
        "Assignment 8"	:	"Comments/Notes",
        "Assignment 10"	:	"Comments/Notes",
        "Assignment 11"	:	"",
        "Assignment 12" :   "",
        "Assignment 0"  :   ""
    }
    labIsRegrade = {
        "Assignment 1"	:	"Is this a regrade?",
        "Assignment 2"	:	"Is this a regrade?",
        "Assignment 3"	:	"Is this a regrade?",
        "Assignment 5"	:	"",
        "Assignment 6"	:	"",
        "Assignment 7"	:	"",
        "Assignment 8"	:	"",
        "Assignment 10"	:	"",
        "Assignment 11"	:	"",
        "Assignment 12" :   "",
        "Assignment 0"  :   ""
    }
    labNonGradingFields = {
        "TA Name",
        "Start time",
        "Completion time",
        "Email",
        "Name"
    }
    for key in labNames:
        labNonGradingFields.add(labPartnerFields[key][0])        
        labNonGradingFields.add(labPartnerFields[key][1])
        labNonGradingFields.add(labWorkingWithPartner[key])
        labNonGradingFields.add(labCommitToGithub[key])
        labNonGradingFields.add(labTAName[key])
        labNonGradingFields.add(labStartTime[key])
        labNonGradingFields.add(labNotes[key])
        labNonGradingFields.add(labIsRegrade[key])


    # Constants relating to parsing studio submissions
    studioNames = [
        "Studio 0",
        "Studio 1",
        "Studio 2",
        "Studio 3",
        "Studio 4",
        "Studio 5",
        "Studio 6",
        "Studio 7",
        "Studio 8",
        "Studio 10",
        "Studio 11",
        "Studio 12"
    ]
    studioRubricUpToDate = {
        "Studio 0"  : True,
        "Studio 1"  : True,
        "Studio 2"  : True,
        "Studio 3"  : True,
        "Studio 4"  : False,
        "Studio 5"  : True,
        "Studio 6"  : True,
        "Studio 7"  : True,
        "Studio 8"  : True,
        "Studio 10" : True,
        "Studio 11" : True,
        "Studio 12" : True
    }
    studioPartnerIDFields = {
        "Studio 0": ["Student One Student ID (6 Digit Number)",
                     "Student Two Student ID (6 Digit Number)",
                     "Student Three Student ID (6 Digit Number)",
                     "Student Four Student ID (6 Digit Number)"
                     ],
        "Studio 1": ["Student 1 Student ID (6 Digit num)",
                     "Student 2 Student ID (6 Digit num)",
                     "Student 3 Student ID (6 Digit num)",
                     "Student 4 Student ID (6 Digit num)"
                     ],
        "Studio 2": ["Student 1 6 Digit Student ID",
                     "Student 2 6 Digit Student ID",
                     "Student 3 6 Digit Student ID",
                     "Student 4 6 Digit Student Id"
                     ],
        "Studio 3": ["Student 1 6 digit Student ID",
                     "Student 2 6 Digit Student ID",
                     "Student 3 6 Digit Student ID",
                     "Student 4 6 Digit Student ID"
                     ],
        "Studio 4": ["",
                     "",
                     "",
                     ""
                     ],
        "Studio 5": ["Student 1 6 digit Student ID",
                     "Student 2 6 Digit Student ID",
                     "Student 3 6 Digit Student ID",
                     "Student 4 6 Digit Student ID"
                     ],
        "Studio 6": ["Student 1 6 digit Student ID",
                     "Student 2 6 Digit Student ID",
                     "Student 3 6 Digit Student ID",
                     "Student 4 6 Digit Student ID"
                     ],
        "Studio 7": ["Student 1 6 digit Student ID",
                     "Student 2 6 Digit Student ID",
                     "Student 3 6 Digit Student ID",
                     "Student 4 6 Digit Student ID"
                     ],
        "Studio 8": ["Student 1 6 digit Student ID",
                     "Student 2 6 Digit Student ID",
                     "Student 3 6 Digit Student ID",
                     "Student 4 6 Digit Student ID"
                     ],
        "Studio 10": ["Student 1 6 digit Student ID",
                      "Student 2 6 Digit Student ID",
                      "Student 3 6 Digit Student ID",
                      "Student 4 6 Digit Student ID"
                      ],
        "Studio 11": ["Student 1 6 digit Student ID",
                      "Student 2 6 Digit Student ID",
                      "Student 3 6 Digit Student ID",
                      "Student 4 6 Digit Student ID"
                      ],
        "Studio 12": ["Student 1 6 digit Student ID",
                      "Student 2 6 Digit Student ID",
                      "Student 3 6 Digit Student ID",
                      "Student 4 6 Digit Student ID"
                      ]
    }
    studioPartnerWKeyFields = {
         "Studio 0": ["",
                      "",
                      "",
                      ""
                      ],
         "Studio 1": ["",
                      "",
                      "",
                      ""
                      ],
         "Studio 2": ["Student 1 Wustl Key",
                      "Student 2 Wustl Key",
                      "Student 3 Wustl Key",
                      "Student 4 Wustl Key"
                      ],
         "Studio 3": ["Student 1 wustl key",
                      "Student 2 Wustl Key",
                      "Student 3 Wustl Key",
                      "Student 4 Wustl Key"
                      ],
         "Studio 4": ["",
                      "",
                      "",
                      ""
                      ],
         "Studio 5": ["",
                      "",
                      "",
                      ""
                      ],
         "Studio 6": ["",
                      "",
                      "",
                      ""
                      ],
         "Studio 7": ["",
                      "",
                      "",
                      ""
                      ],
         "Studio 8": ["",
                      "",
                      "",
                      ""
                      ],
         "Studio 10": ["",
                       "",
                       "",
                       ""
                       ],
         "Studio 11": ["",
                       "",
                       "",
                       ""
                       ],
         "Studio 12": ["",
                       "",
                       "",
                       ""
                       ]
     }
    studioTAName = {
        "Studio 0": "TA Name",
        "Studio 1": "TA Name",
        "Studio 2": "TA Name",
        "Studio 3": "TA Name",
        "Studio 4": "",
        "Studio 5": "Name",
        "Studio 6": "Name",
        "Studio 7": "Name",
        "Studio 8": "Name",
        "Studio 10": "Name",
        "Studio 11": "Name",
        "Studio 12": "Name"
    }
    studioStartTime = {
        "Studio 0": "Start time",
        "Studio 1": "Start time",
        "Studio 2": "Start time",
        "Studio 3": "Start time",
        "Studio 4": "",
        "Studio 5": "Start time",
        "Studio 6": "Start time",
        "Studio 7": "Start time",
        "Studio 8": "Start time",
        "Studio 10": "Start time",
        "Studio 11": "Start time",
        "Studio 12": "Start time"
    }
