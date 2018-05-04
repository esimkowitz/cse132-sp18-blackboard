import json
import datetime
import sys
import dateutil.parser
from constants import Constants

constants = Constants()


class Grade:
    def __init__(self, name, points, kind, timestamp, grader, notes=None, isRegrade=False, isLate=False, isZero=False):
        self.name = name
        self.points = points
        self.kind = kind
        if isinstance(timestamp, datetime.datetime):
            self.timestamp = timestamp
        else:
            try:
                self.timestamp = dateutil.parser.parse(timestamp)
            except ValueError:
                try:
                    self.timestamp = datetime.datetime.strptime(
                        timestamp, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    self.timestamp = datetime.datetime.strptime(
                        timestamp, "%m/%d/%y %H:%M:%S") 
        try:
            self.timestamp = constants.tz.localize(
                self.timestamp)
        except ValueError:
            # The datetime already has a timezone
            pass

        self.isRegrade = isRegrade
        self.grader = grader
        self.notes = notes
        self.history = []
        self.isLate = isLate
        self.isZero = isZero

    def getName(self):
        return self.name

    def getPoints(self):
        return self.points

    def getIsLate(self):
        return self.isLate

    def getTimestamp(self):
        return self.timestamp

    def getIsRegrade(self):
        return self.isRegrade

    def getGrader(self):
        return self.grader

    def getKind(self):
        return self.kind

    def getNotes(self):
        return self.notes

    def getIsZero(self):
        return self.isZero
    
    def getHistory(self):
        return self.history
    
    def setPoints(self, points):
        self.points = points

    def setIsLate(self, isLate):
        self.isLate = isLate

    def setIsZero(self, isZero):
        self.isZero = isZero

    def addHistory(self, old_grade):
        self.history.append(old_grade)

    def output(self):
        history = []
        for grade in self.history:
            history.append(grade.output())
        grade_output = {
            "name": self.name,
            "points": self.points,
            "timestamp": self.timestamp.isoformat(),
            "kind": self.kind,
            "isRegrade": self.isRegrade,
            "grader": self.grader,
            "notes": self.notes,
            "history": history,
            "isLate": self.isLate,
            "isZero": self.isZero
        }
        return grade_output

    def __str__(self):
        return "%s: [points: %i, timestamp: %s, isLate: %r, isZero: %r]"%(self.name, self.points, str(self.timestamp), self.isLate, self.isZero)
