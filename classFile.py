import datetime


#Truck class created with speed, miles , locations, departure time and packages, so we can include the package objects
#later on. Added the truck ID parameter to identify trucks upon professor suggestion.
class Truck:
    def __init__(self, ID, speed, miles, current_location, current_time, departure_time, packages):
        self.ID = ID
        self.speed = speed
        self.miles = miles
        self.current_location = current_location
        self.current_time = current_time
        self.departure_time = departure_time
        self.packages = packages

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.ID, self.speed, self.miles, self.current_location, self.departure_time, self.packages)


# Package Object created with appropriate parameters along with status departure and delivery times. Making it return
# as a string valuable information that's easy to read and has relevant information.
#Meeting with the professor to change the return values to reflect what was needed and add a truck id to differentiate
# trucks in the report.
class Packages:
    def __init__(self, ID, address, city, state, zip_code, delivery_deadline, weight, notes, status, departure_time,
                 delivery_time):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departure_time = departure_time
        self.delivery_time = delivery_time
        self.truckNumber = 0

    def __str__(self):
        return ("ID Number: %s, Address: %s, City: %s, State: %s, Zip Code: %s, Deadline: %s, Weight: %s, Notes: %s, "
                "Status: %s, Departure Time: %s, Delivery Time: %s, Truck Number: %s") % (self.ID, self.address, self.city, self.state,
                                                                        self.zipcode, self.delivery_deadline,
                                                                        self.weight, self.notes, self.status,
                                                                        self.departure_time, self.delivery_time, self.truckNumber)

    # Sets status depending on departure time and delivery time to be able to update status per package. Added the
    # Package ID 9 to have its own if statement since information gets corrected at 10:20\
    #Professor suggested adding the truck ID to the report, so we had to add it on the update_status method as well. Also
    #he pointed out how to correctly use f strings instead of the %s method.
    def update_status(self, timeFactor):
        if self.delivery_time == None:
            status = "At hub"
        elif timeFactor < self.departure_time:
            status = "At hub"
        elif timeFactor < self.delivery_time:
            status = "In route"
        else:
            status = f"Delivered @ {self.delivery_time}"
        address = self.address
        zipcode = self.zipcode
        # Needed a condition for package ID 9 to change the address because I couldn't figure it out otherwise. Once
        # the time passes 10:20 it will update it for package delivery/report.
        if self.ID == 9:
            if timeFactor > datetime.timedelta(hours=10, minutes=20):
                address = "410 S State St"
                zipcode = "84111"
            else:
                address = "300 State St"
                zipcode = "84103"
                #TODO leave the %s
        return ("ID Number: %s, Address: %s, City: %s, State: %s, Zip Code: %s, Deadline: %s, Weight: %s, Notes: %s, "
                "Status: %s, Departure Time: %s, Truck Number: %s") % (self.ID, address, self.city, self.state,
                                                                        zipcode, self.delivery_deadline,
                                                                        self.weight, self.notes, status,
                                                                        self.departure_time, self.truckNumber)
