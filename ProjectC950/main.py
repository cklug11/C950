#Student:Caroline Klug, Student ID: 010148356
import csv
import datetime
from cmath import inf

from CreateHashTable import ChainingHashTable
import Truck
from package import Package

#Reads the file with distance information
with open("Distance_File.csv") as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)

#reads the file with address information
with open("Address_File1 copy 2.csv", encoding='utf-8-sig') as csvfile1:
    CSV_Address = csv.reader(csvfile1)
    CSV_Address = list(CSV_Address)


#Loads package data into hash table
def loadPackageData(fileName):
    with open(fileName) as Package_File:
        packageData = csv.reader(Package_File, delimiter=',')
        next(packageData)
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDelivery_deadline = package[5]
            pWeight = package[6]
            pStatus = "At Hub"


            #package object
            p = Package(pID, pAddress, pCity, pState,pZipcode,pDelivery_deadline,pWeight,pStatus)

            # inserts package data into the hash table
            myHash.insert(pID, p)


#Finds distance between two addresses
def distance_between(location1,location2):
    distance = CSV_Distance[location1][location2]
    if distance == '':
        distance = CSV_Distance[location2][location1]

    return float(distance)

#Finds address number from address string
def find_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])

#Calculates the total mileage driven by the delivery trucks
def total_mileage(truck1,truck2,truck3):
    total = truck1.mileage + truck2.mileage + truck3.mileage
    return total

#Creates truck object: truck1
truck1 = Truck.Truck(16,18,[13,1,14,19,16,15,20,40,29,30,31,34,37],0,
                     '4001 South 700 East', datetime.timedelta(hours=8,minutes=0, seconds=0))

#Creates truck object: truck2
truck2 = Truck.Truck(16,18,[2,3,9,18,36,38,39,7,8,10,11,12,23,24,17],0,
                     '4001 South 700 East', datetime.timedelta(hours=11,minutes=0, seconds=0))

#Creates truck object: truck3
truck3 = Truck.Truck(16,18,[4,5,6,28,32,33,21,22,35,27,25,26],0,
                     '4001 South 700 East', datetime.timedelta(hours=9,minutes=6, seconds=0))

#Arranges the packages on each truck based on the Nearest Neighbor Algorithm and calculates the truck's route's mileage
def deliver_packages(truck):
    not_delivered=[] #creates an empty list called not_delivered
    for packageID in truck.packages:
        package = myHash.lookup(packageID)
        not_delivered.append(package) #Adds packages to not_delivered list
    truck.packages.clear() #Clears truck's package list,packages will be placed back on truck later based on Nearest
    #Neighbor Algorithm

    #Goes through not_delivered list until no packages remain
    #Adds the nearest package to the truck package list one by one
    while len(not_delivered)>0:
        next_address = float(inf)
        next_package = None
        for package in not_delivered:
            if distance_between(find_address(truck.address),find_address(package.address)) <= next_address:
                next_address = distance_between(find_address(truck.address),find_address(package.address))
                next_package = package
        truck.packages.append(next_package.ID) #Adds the next closest package to truck package list
        not_delivered.remove(next_package) #Removes the same package to truck package list
        truck.mileage += next_address #Adds the miles driven to deliver this package to the truck's mileage
        truck.address = next_package.address #Updates the truck's address to the address of the just delivered package
        time_traveled = (next_address / 18) * 60 #Calculates the amount of time it took to travel to the package
        time_traveled_timedelta = datetime.timedelta(minutes=time_traveled)
        truck.depart_time += time_traveled_timedelta #Adds the travel time to the depart time
        next_package.delivery_time = truck.depart_time


#Creates Hash Table
myHash = ChainingHashTable()

#Loads packages into Hash Table
loadPackageData('Package_File.csv')


#Loads Truck 1 and calculates its mileage
deliver_packages(truck1)

#Loads Truck 2 and calculates its mileage
deliver_packages(truck2)

#Loads Truck 3 and calculates its mileage
deliver_packages(truck3)


#Calculates the total mileage of all three trucks
total = total_mileage(truck1,truck2,truck3)


#User Interface
print("Welcome to the Western Governors University Parcel Service(WGUPS)")

print("Select from the options below:")
print("1. Display the Status of All Packages and the Route's Total Mileage")
print("2. Display the Status of An Individual Package at a Particular Time")
print("3. Display the Status of All Packages at a Particular time")
print("4. Exit Program")
while True:
    choice=int(input("Enter your choice: ")) #Get User Input

    if choice==1:
        #Display total mileage of the route and status of all the packages
        print("The existing route covers a total distance of",total,"miles for package delivery\n")
        for packageID in range(1, 41):
            package = myHash.lookup(packageID)
            if packageID in {2,3,9,18,36,38,39,7,8,10,11,12,23,24}:
                print("Package ",str(package.ID) + ": " + package.address, " ",package.city," ",package.state," ",
                      str(package.zipcode)," ",package.Delivery_deadline," ",package.weight,
                      " Delivered at",package.delivery_time,"by Truck 2")

            elif packageID in {13,1,14,19,16,15,20,40,29,30,31,34,37,17}:
                print("Package ",str(package.ID) + ": " + package.address, " ",package.city," ",package.state," ",
                      str(package.zipcode)," ",package.Delivery_deadline," ",package.weight," Delivered at",
                      package.delivery_time,"by Truck 1")

            elif packageID in {4,5,6,28,32,33,21,22,35,27,25,26,24}:
                print("Package ",str(package.ID) + ": " + package.address, " ",package.city," ",package.state," ",
                      str(package.zipcode),
                  " ",package.Delivery_deadline," ",package.weight," Delivered at",package.delivery_time,"by Truck 3")

    elif choice==2:
        #Display the status of a specific package at a specific time
        while True:
            #Prompts User to input package ID
            chosen = int(input("Enter a Package ID: "))
            if chosen <1 or chosen>40:
                    print("Invalid Package ID. Please Enter a Number between 1 and 40")
                    continue #Prompts User to enter a valid package ID
            break
        while True:
            #Prompts User to input time in a particular format
            print("Please enter a time for checking the status of the packages") #Prompts user to input a time
            print("Enter in the format of HH:MM:SS.")  #Prompts user to input a time in a certain format
            print("For Example: 8:30 AM would be 08:30:00 & 2:30 pm would be 14:30:00 ")

            user_time = input("Your time?: ")
            try:
                h, m, s = map(int, user_time.split(":"))
                convert_timedelta = datetime.timedelta(hours=h, minutes=m, seconds=s)
                break
            except ValueError: #Prompts User to enter a time again,but in the correct format
                print("Invalid time format. Please enter the time in HH:MM:SS format.")
        package = myHash.lookup(chosen) #Updates package status and displays output
        package.update_status(convert_timedelta)
        print("Package",str(package.ID) + ": " + package.address,"",package.city,"",package.state,"",
              str(package.zipcode),"",package.Delivery_deadline,"",package.weight,"",package.status)

    elif choice==3:
        #Displays the status of all packages at a certain time
        while True:
            print("Please enter a time for checking the status of the packages") #Prompts user to input a time
            print("Enter in the format of HH:MM:SS.")  #Prompts user to input a time in a certain format
            print("For Example: 8:30 AM would be 08:30:00 & 2:30 pm would be 14:30:00 ")

            user_time = input("Your time?: ")
            try:
                h, m, s = map(int, user_time.split(":"))
                convert_timedelta = datetime.timedelta(hours=h, minutes=m, seconds=s)
                break
            except ValueError: #Prompts User to enter a time again,but in the correct format
                print("Invalid time format. Please enter the time in HH:MM:SS format.")

        #Updates status of all packages and displays output
        for packageID in range(1, 41):
            package = myHash.lookup(packageID)
            package.update_status(convert_timedelta)
            print("Package ",str(package.ID) + ": " + package.address, " ",package.city," ",package.state," ",str(package.zipcode),
            " ",package.Delivery_deadline," ",package.weight," ",package.status)
    elif choice==4:
        #Exits program
        print("Exiting Program")
        break
    else:
        #Handles invalid choice input
        print("Invalid Choice. Please Try Again")