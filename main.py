#Christopher Paulino Hernandez | cpaul78@wgu.edu | Student ID: 006785967
import hashTable
from hashTable import HashTable
import csv
import datetime
import classFile
from classFile import Packages
from classFile import Truck

#lOAD the necessary csv files to have it ready. Was having a problem with taking in the information from the csv
#they kept coming through with leading values but using this encoding fixed it so far no problems. Will keep an eye out
with open('address.csv') as addressesCSV:
    addressData = csv.reader(addressesCSV)
    addressData = list(addressData)
    #testing to see if csv file reads correctly.
    #for lines in addressData:
    #print(lines)
#lOAD the necessary csv files to have it ready. Was having a problem with taking in the information from the csv
#they kept coming through with leading values but using this encoding fixed it so far no problems. Will keep an eye out
with open('distance.csv') as distancesCSV:
    distanceData = csv.reader(distancesCSV)
    distanceData = list(distanceData)
    #for lines in distanceData:
    #print(lines)
#lOAD the necessary csv files to have it ready. Was having a problem with taking in the information from the csv
#they kept coming through with leading values but using this encoding fixed it so far no problems. Will keep an eye out
with open('packages.csv') as packageCSV:
    packagesData = csv.reader(packageCSV)
    packagesData = list(packagesData)
    # for lines in packagesData:
    #     print(lines)


#Creating a method to find the distance between two points and returning the float value.
#Fixed during session with professor
def distance_between(x, y):
    distance = distanceData[x][y]
    # print(x)
    # print(y)
    if distance == '':
        distance = distanceData[y][x]
        # print(distance)
    return float(distance)


#Method to pull address out returns integer value in the beginning row
#-1 Lets us know we didn't find an address
#Fixed during session with professor
def address_puller(address):
    for row in addressData:
        if address in row[2]:
            return int(row[0])
    return -1


#method to load the hash table. Opens the packages file and parses the information to populate the hash table.
#Fixed during session with professor
def hash_loader(filename, hashForPackages):
    with open(filename) as the_packages:
        packageInformation = csv.reader(the_packages, delimiter=',')
        for package in packageInformation:
            packageID = int(package[0])
            packageAddress = package[1]
            packageCity = package[2]
            packageState = package[3]
            packageZip = package[4]
            packageDelivery_deadline = package[5]
            packageWeight = package[6]
            packageSpecialNotes = package[7]
            packageStatus = "Currently at base"
            packageDeparture_Time = None
            packageDelivery_Time = None

            packer = Packages(packageID, packageAddress, packageCity, packageState, packageZip,
                              packageDelivery_deadline, packageWeight, packageSpecialNotes, packageStatus,
                              packageDeparture_Time, packageDelivery_Time)
            hashForPackages.insertion(packageID, packer)
            #print(packer) #Isnt pulling the csv correctly


#Hash being created to prepare for loading
hashForPackages = HashTable()
#Hash loader function
hash_loader("packages.csv", hashForPackages)
#Manually loading the trucks according to what has to go together and time restraints, might move them around a bit and
#mess with departure times
truck_1 = Truck(1, 18, 0.0, "4001 South 700 East", current_time=datetime.timedelta(hours=8),
                departure_time=datetime.timedelta(hours=8),
                packages=[1, 13, 14, 15, 16, 19, 20, 27, 29, 26, 31, 34, 37, 40])

truck_2 = Truck(2, 18, 0.0, "4001 South 700 East", current_time=datetime.timedelta(hours=8),
                departure_time=datetime.timedelta(hours=10, minutes=20),
                packages=[2, 3, 4, 5, 18, 9, 25, 28, 32, 35, 36, 38])

truck_3 = Truck(3, 18, 0.0, "4001 South 700 East", current_time=datetime.timedelta(hours=8),
                departure_time=datetime.timedelta(hours=9, minutes=5),
                packages=[6, 30, 8, 10, 11, 12, 17, 21, 22, 23, 24, 7, 33, 39])


# truck_3 = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
#                 [6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])


# ALGORITHM 2: 109.3 miles passes... This algorithm is a simplified version of the last one since it was giving me
# over 200 miles at EOD which is weird, so I decided to make it as simple as possible. It consists of appending
# packages into the inTransit array and clearing the packages from truck to avoid any double deliveries or anything
# of the sort. Then we declare a  minimum distance and a null/none value of the closest package from the trucks
# current location using the CSV data and go from there. After the delivery algorithm runs we update the packages
# fields and remove the package from the intransit array.
def delivery_algorithm(truck):
    inTransit = []

    for packageID in truck.packages:
        package = hashForPackages.lookup(packageID)
        inTransit.append(package)
    truck.packages.clear()

    while len(inTransit) > 0:
        min_distance = 2000
        closest_package = None
        for package in inTransit:
            d = distance_between(address_puller(truck.current_location),
                                 address_puller(package.address))
            if d <= min_distance:
                min_distance = d
                closest_package = package

        truck.packages.append(closest_package.ID)
        inTransit.remove(closest_package)
        closest_package.status = "Delivered"
        closest_package.departure_time = truck.departure_time
        closest_package.truckNumber = truck.ID
        truck.departure_time += datetime.timedelta(hours=min_distance / 18)
        closest_package.delivery_time = truck.departure_time
        truck.current_location = closest_package.address
        truck.miles += min_distance


#Calling the trucks to go on delivery and making sure truck 2 goes after 10:20 because of package number 9
delivery_algorithm(truck_1)
delivery_algorithm(truck_3)
truck_2.departure_time = datetime.timedelta(hours=10, minutes=20)

delivery_algorithm(truck_2)
# UI: Will open up giving you a summary of the miles for the day. The terminal will ask you to choose an option
# depending on if you want to look at an individual package followed by the time or all packages followed by a request
# for time with the format HH:MM military hours. If type 'Time' then that just goes directly to ask for time to see
# the package status at those times.

print("--------------------------------Western Governors University Parcel Service--------------------------------")
print("WGUPS has concluded the day with", (truck_1.miles + truck_2.miles + truck_3.miles),
      "miles traveled to deliver all packages.")
optionFactor = input(
    "To view an individual package type 'Solo'.\nTo view all packages type 'All'.\nFor packages after a certain time "
    "type 'Time'.\nTo exit just type 'Exit':")

if optionFactor == "Solo":
    time_input = input("Please enter desired time in the format HH:MM...")
    (h, m) = time_input.split(":")
    time_conversion = datetime.timedelta(hours=int(h), minutes=int(m))
    individual_input = input("Enter package ID number:")
    package = hashForPackages.lookup(int(individual_input))
    print(package.update_status(time_conversion))
elif optionFactor == "All":
    time_input = input("Please enter desired time in the format HH:MM...")
    (h, m) = time_input.split(":")
    time_conversion = datetime.timedelta(hours=int(h), minutes=int(m))
    for packageID in range(1, 41):
        package = hashForPackages.lookup(packageID)
        print(package.update_status(time_conversion))
elif optionFactor == "Time":

    time_input = input("Please enter desired time in the format HH:MM...")
    (h, m) = time_input.split(":")
    time_conversion = datetime.timedelta(hours=int(h), minutes=int(m))
    for packageID in range(1, 41):
        package = hashForPackages.lookup(packageID)
        print(package.update_status(time_conversion))


elif optionFactor == "Exit":
    exit()
