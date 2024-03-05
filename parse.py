import csv
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt

class Car:
    make = ""
    model = ""
    type = ""
    range = 0
    CAFV = 0 #0 for no, 1 for yes, 2 for unknown
    year = 0

cars = []

numBEV = 0
numPHEV = 0
numCompliant = 0
meanRange = 0
medianRange = 0
modeRange = 0

def readFile():
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                tmpType = "BEV"
                if(row['Type'] == "Plug-in Hybrid Electric Vehicle (PHEV)"):
                    tmpType = "PHEV"

                tmpCAFV = 1
                if(row['CAFV'] == "Not eligible due to low battery range"):
                    tmpCAFV = 0
                elif(row['CAFV'] == "Eligibility unknown as battery range has not been researched"):
                    tmpCAFV = 2

                tmpCar = Car()
                tmpCar.make = row['Make']
                tmpCar.model = row['Model']
                tmpCar.year = int(row['Year'])
                tmpCar.range = int(row['Range'])
                tmpCar.type = tmpType
                tmpCar.CAFV = tmpCAFV

                cars.append(tmpCar)
            except:
                print("Invalid row")

def findAvgRanges():
    global meanRange, medianRange, modeRange
    ranges = []
    for car in cars:
        if(car.range != 0):
            ranges.append(car.range)
    
    meanRange = statistics.mean(ranges)
    medianRange = statistics.median(ranges)
    modeRange = statistics.mode(ranges)

def findMaxRange():
    tmpCar = cars[0]
    for car in cars:
        if(car.range > tmpCar.range):
            tmpCar = car

    return tmpCar

def findMinRange():
    tmpCar = cars[0]
    for car in cars:
        if(car.range < tmpCar.range and car.range > 0):
            tmpCar = car

    return tmpCar

def countType():
    global numPHEV
    global numBEV
    for car in cars:
        if(car.type == "BEV"):
            numBEV += 1
        else:
            numPHEV += 1

def CAFVCompliance():
    global numCompliant
    for car in cars:
        if(car.CAFV == 1):
            numCompliant += 1

def printVals():
    print("Total number of cars:", len(cars))
    print("numBEV:", numBEV, "%", numBEV / len(cars) * 100)
    print("numPHEV:", numPHEV, "%", numPHEV / len(cars) * 100)
    print("num CAFV Compliant:", numCompliant, "%", numCompliant / len(cars) * 100)
    print("Mean range:", meanRange)
    print("Median range:", medianRange)
    print("Mode range:", modeRange)
    print("Min range:", minRangeCar.year, minRangeCar.make, minRangeCar.model, minRangeCar.range, "Miles")
    print("Max range:", maxRangeCar.year, maxRangeCar.make, maxRangeCar.model, maxRangeCar.range, "Miles")
    print("\n")

def countYears():
    years = defaultdict(int)
    for car in cars:
        years[car.year] += 1

    # Sort makes from largest to smallest based on their counts
    years = sorted(years.items(), key=lambda x: x[0], reverse=True)

    for year in years:
        print(f"{year[0]}: {year[1]}")

    print("\n")

def countMakes():
    makes = defaultdict(int)
    for car in cars:
        makes[car.make] += 1

    # Sort makes from largest to smallest based on their counts
    makes = sorted(makes.items(), key=lambda x: x[1], reverse=True)

    for make in makes:
        print(f"{make[0]}: {make[1]:.2f} | {make[1] / len(cars) * 100:.2f}%")

    print("\n")

def countModels():
    models = defaultdict(int)
    for car in cars:
        models[car.model] += 1

    # Sort makes from largest to smallest based on their counts
    models = sorted(models.items(), key=lambda x: x[1], reverse=True)

    for model in models:
        print(f"{model[0]}: {model[1]}")

    print("\n")

def carsBeforeYear(year):
    for car in cars:
        if(car.year == year):
            print(car.make, car.model)

def rangeChart():
    global meanRange, medianRange, modeRange
    y = [medianRange, meanRange, modeRange]

    x = ['Median', 'Mean', 'Mode']

    fig, ax = plt.subplots()
    ax.barh(x, y, color='#060E2E')

    # Remove box around the graph
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set background color
    fig.set_facecolor('#cdd4da')
    ax.set_facecolor('#cdd4da')

    plt.title('Range Graph')
    plt.xlabel('Range (miles)')
    plt.ylabel('Type of average')
    plt.show()

def brandPie():
    makes = defaultdict(int)
    for car in cars:
        makes[car.make] += 1

    # Sort makes from largest to smallest based on their counts
    makes_sorted = sorted(makes.items(), key=lambda x: x[1], reverse=True)

    # Keep only the top 9 makes and group the rest into 'Other'
    top_makes = makes_sorted[:9]
    other_count = sum(count for _, count in makes_sorted[9:])
    top_makes.append(('Other', other_count))

    labels, counts = zip(*top_makes)

    # Create a figure and set background color
    fig, ax = plt.subplots()
    fig.set_facecolor('#cdd4da')  # Set the background color to 'cdd4da'

    # Plotting the pie chart
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title('Top EV Manufacturers')
    plt.show()


def evGraph():
    years = defaultdict(int)
    for car in cars:
        if car.year != 2024:
            years[car.year] += 1

    # Extracting data for plotting
    x_values = list(years.keys())
    y_values = list(years.values())

    # Sorting data by years
    sorted_years = sorted(zip(x_values, y_values))

    x_values_sorted, y_values_sorted = zip(*sorted_years)

    # Create a figure and set background color
    fig, ax = plt.subplots()
    fig.set_facecolor('#cdd4da')  # Set the background color to 'cdd4da'
    ax.set_facecolor('#cdd4da')

    # Plotting the line graph
    ax.plot(x_values_sorted, y_values_sorted, marker='o', linestyle='-', color = '#060e2e')
    ax.set_title('Electric Vehicles Adoption')
    ax.set_xlabel('Year')
    ax.set_ylabel('')
    
    # Remove box around the graph
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Move y-axis ticks and labels to the right side
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")

    plt.show()

readFile()

countType()

CAFVCompliance()

findAvgRanges()

maxRangeCar = findMaxRange()

minRangeCar = findMinRange()

printVals()

countMakes()

countYears()

countModels()

rangeChart()

brandPie()

evGraph()

#carsBeforeYear(2000)













