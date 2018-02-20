"""
This is the EV3 side of the Hot or Cold project.
The purpose for this module is for the EV3 robot to connect the PC and its
GUI functions in order for the robot to follow its commands. In particular,
the robot has the IR sensor that is continously active while the rest of the
code is running. This is because if at any point the Snatcher robot ever
comes across the object it is trying to find, it'll automatically go to and
pick it up, ending the overall use of the program.

Author: Angel Rivera
"""
import mqtt_remote_method_calls as com
import robot_controller as robo
import time


def main():
    #   Attaches the robot and connects the robot to the PC
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    #   Throughout the use of the robot, if at any point before the touch
    #   sensor is pressed, the robot detects something, it'll start to go
    #   towards and eventually grab the object
    while not robot.touch_sensor.is_pressed:

        if robot.ir_sensor.proximity < 20:
            robot.grab_object()
            break

        time.sleep(0.1)

    # After the loop is broken, the program will shut off and end for good
    robot.shutdown()
    print("Goodbye!")


#   Starts the program
main()
