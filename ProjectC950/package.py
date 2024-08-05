import datetime
#Creates class for packages
class Package:
    def __init__(self,ID,address,city,state,zipcode,Delivery_deadline,weight,status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Delivery_deadline = Delivery_deadline
        self.weight = weight
        self.status = status
        self.delivery_time = None
        self.leave_hub = None

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                self.Delivery_deadline, self.weight, self.status)

    #Takes the User's time input and updates the package's status accordingly
    def update_status(self,convert_timedelta):
        car = 0
        if self.ID in {2,3,9,18,36,38,39,7,8,10,11,12,23,24}:
            self.leave_hub = datetime.timedelta(hours=11,minutes=0, seconds=0)
            car = 2
        if self.ID in {13,1,14,19,16,15,20,40,29,30,31,34,37,17}:
            self.leave_hub = datetime.timedelta(hours=8,minutes=0, seconds=0)
            car=1
        if self.ID in {4,5,6,28,32,33,21,22,35,27,25,26,24}:
            self.leave_hub = datetime.timedelta(hours=9,minutes=6, seconds=0)
            car=3
        if convert_timedelta < datetime.timedelta(hours=10,minutes=20, seconds=0) and self.ID == 9:
            self.address = "300 State St"
            self.zipcode = '84103'
        if self.delivery_time <= convert_timedelta:
            self.status = "Delivered at "+ str(self.delivery_time)+" by Truck "+str(car)
        elif self.leave_hub <= convert_timedelta < self.delivery_time:
            self.status = "En route by Truck "+str(car)
        elif self.leave_hub > convert_timedelta:
            self.status = "At Hub"
