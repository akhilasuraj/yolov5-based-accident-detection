from asyncio.windows_events import NULL
from collections import OrderedDict
import math
import numpy as np

coordDict = OrderedDict()
newCoordDict = OrderedDict()


def removeAll():
    global coordDict
    coordDict.clear()


def removeItem(objectID):
    global newCoordDict
    newCoordDict.pop(objectID)


def updateItem(objectID, centroid):
    global newCoordDict
    newCoordDict.update({objectID: centroid})


def addNewItem(objectID, centroid):
    global newCoordDict
    newCoordDict.update({objectID: centroid})


def calculateDistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


def predictDistance(point, prePoint, prePrePoint):
    distance = calculateDistance((point[0], point[1]), prePoint)
    preDistance = calculateDistance(prePoint, prePrePoint)
    predictedDistance = (distance / preDistance) * distance if preDistance != 0 else 0
    return predictedDistance

def validate(point, prePoint, prePrePoint):
    if (point == 0 or prePoint == 0  or prePrePoint == 0):
        return False
    else: 
        return True

# def predictAngle(point, prePoint, prePrePoint):
#     distance = calculateDistance((point[0], point[1]), prePoint)
#     preDistance = calculateDistance(prePoint, prePrePoint)
#     ratio = (distance / preDistance)


def detect(objects):
    global coordDict
    global newCoordDict
    if len(list(objects.keys())) > 0:
        for (objectID, centroid) in objects.items():
            if coordDict.get(objectID):
                point = coordDict.get(objectID)[0]
                prePoint = coordDict.get(objectID)[1]
                prePrePoint = coordDict.get(objectID)[2]
                print(point)
                print(prePoint)
                print(prePrePoint)
                distanceDif = 0
                angleDif = 0
                if validate(point, prePoint, prePrePoint):
                    predictedDistance = predictDistance(point, prePoint, prePrePoint)
                    actualDistance = calculateDistance((centroid[0],centroid[1]), point)
                    distanceDif = abs(predictedDistance - actualDistance)
                    print("distanceDif" , distanceDif)

                    # predictedAnlge = predictAngle(point, prePoint, prePrePoint)
                updateItem(objectID, [(centroid[0], centroid[1]), point, prePoint, distanceDif])
            else:
                updateItem(
                    objectID, [(centroid[0], centroid[1]), NULL, NULL, NULL])

    removeAll()
    coordDict = newCoordDict.copy()
    newCoordDict.clear()
    return coordDict
