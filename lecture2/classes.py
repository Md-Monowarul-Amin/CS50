from operator import le


class Point():
    def __init__(self,input1, input2):
        self.x = input1
        self.y = input2


class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passangers = []
    


    def add_passenger(self, name):
        # print(self.open_seats())
        if not self.open_seats():
            # print(self.open_seats)
            return False
        else:
            self.passangers.append(name)
            return True

    def open_seats(self):
        # print(self.capacity - len(self.passangers))
        return(self.capacity - len(self.passangers))

        

flight_1 = Flight(3)
peoples = ["Harry", "Ron", "Hermione", "Ginny", "Randy"]
for person in peoples:
    success = flight_1.add_passenger(person)
    # print (success)
    if success == True:
        print(f"{person} Added to flight_1 successfully..." )
    else:
        print(f"No available seats for {person}")

# print(flight_1.passangers)
