"""Chase Tail is a function that will have the robot dog 'chaes it's tail'
until it sees an object in front of it.
Author: Emily Dougherty"""


import ev3dev.ev3 as ev3
import time

import robot_controller as robo


def main():
    print("--------------------------------------------")
    print(" Chase Tail")
    print("--------------------------------------------")
    ev3.Sound.speak("Chase Tail")
    print("Press the touch sensor to exit this program.")

    robot = robo.Snatch3r()

    while not robot.touch_sensor.is_pressed:
        robot.left(300, 300)
        if robot.ir_sensor.proximity < 10:
            robot.stop()
            ev3.Sound.speak("bark bark")
        time.sleep(0.3)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
    robot.stop()


main()
