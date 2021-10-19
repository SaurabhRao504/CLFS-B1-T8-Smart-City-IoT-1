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
        total_time = time.time() - parking_time1
    if IR2 == 0:
        total_time = time.time() - parking_time2
        
    if total_time < 3600:
        hours = 1
    else:
        hours = int(total_time / 3600)+1

   
    rate = hours * 30.00

    ret = "Vehicle Exited!\n Your Total for " + "{:.2f}".format(hours) + " hours is " + "{:.2f} " + "Rupees".format(rate)

    print(ret)


def command_handler(command,IR1,IR2):
    global parking_time1, parking_time2
    
    if command == "P":
        if IR1 == 1:
            print("Time Entered: " + str(time.strftime('%I:%M %p',time.localtime(parking_time1))))
        if IR2 == 1:
            str("Time Entered: " + time.strftime('%I:%M %p',time.localtime(parking_time2)))
    
    elif command == "E":
        fare_calculation(IR1,IR2)

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
            print("Parking Started 1")
            flag1 = 0
            command_handler(command)
        elif (IR1 == 0 and flag1 == 0):
            command = "E"
            print("Exiting the Lot 1")
            flag1 = 1
            command_handler(command)

        if (IR2 == 1 and flag2 == 1):
            command = "P"
            print("Parking Started 2")
            flag2 = 0
            command_handler(command)
        elif (IR2 == 0 and flag2 == 0):
            command = "E"
            print("Exiting the Lot 2")
            flag2 = 1
            command_handler(command,IR1,IR2)


if __name__ == '__main__':
    main()
