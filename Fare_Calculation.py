import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

IR_SENSOR1 = 11
IR_SENSOR2 = 13

GPIO.setup(IR_SENSOR1, GPIO.IN)
GPIO.setup(IR_SENSOR2, GPIO.IN)

flag1 = 1
flag2 = 1
parking_time1 = 0
parking_time2 = 0


def fare_calculation(IR1,IR2):
    global parking_time1, parking_time2

    if IR1 == 0:
        total_time1 = time.time() - parking_time1

        if total_time1 < 3600:
            hours1 = 1
        else:
            hours1 = int(total_time1/3600)+1

        rate1 = hours1 * 30.00

        ret1 = "Vehicle Exited 1!\n" \
              "Your Total for " + "{:.2f}".format(hours1) + " hours is Rs" + "{:.2f}".format(rate1)

        return ret1
        

    if IR2 == 0:
        total_time2 = time.time() - parking_time2

        if total_time2 < 3600:
            hours2 = 1
        else:
            hours2 = int(total_time2/3600)+1

        rate2 = hours2 * 30.00

        ret2 = "Vehicle Exited 2!\n" \
              "Your Total for " + "{:.2f}".format(hours2) + " hours is Rs." + "{:.2f}".format(rate2)

        return ret2


def command_handler(command,IR1,IR2):
    global parking_time1, parking_time2
    
    if command == "P":
        if IR1 == 1:
            parking_time1 = time.time()
            print("Time Entered: " + str(time.strftime('%I:%M %p', time.localtime(parking_time1))))

        if IR2 == 1:
            parking_time2 = time.time()
            print("Time Entered: " + str(time.strftime('%I:%M %p', time.localtime(parking_time2))))
    
    elif command == "E":
        print(fare_calculation(IR1,IR2))

    elif command == "Q":
        return

    else:
        print("Error: Invalid Command")
        time.sleep(1)

        
def main():
    global flag1, flag2
    
    command = ""
    while command != "Q":
        
        IR1 = GPIO.input(IR_SENSOR1)
        IR2 = GPIO.input(IR_SENSOR2)
        
        
        if (IR1 == 1 and flag1 == 1):
            command = "P"
            print("Vehicle Parked in Lot 1")
            flag1 = 0
            command_handler(command,IR1,IR2)
        elif (IR1 == 0 and flag1 == 0):
            command = "E"
            print("Vehicle Exiting Lot 1")
            flag1 = 1
            command_handler(command,IR1,IR2)

        if (IR2 == 1 and flag2 == 1):
            command = "P"
            print("Vehicle Parked in Lot 2")
            flag2 = 0
            command_handler(command,IR1,IR2)
        elif (IR2 == 0 and flag2 == 0):
            command = "E"
            print("Vehicle Exiting Lot 2")
            flag2 = 1
            command_handler(command,IR1,IR2)


if __name__ == '__main__':
    main()
