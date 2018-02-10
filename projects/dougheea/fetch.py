"""This function makes the robot dog play fetch by seeking the beacon and
then returning back to its starting point"""
import traceback

import ev3dev.ev3 as ev3
import time

import robot_controller as robo


def main():
    print("--------------------------------------------")
    print(" Play Fetch")
    print("--------------------------------------------")
    ev3.Sound.speak("Play Fetch").wait()

    robot = robo.Snatch3r()
    try:
        while True:
            found_beacon = robot.seek_beacon()
            if found_beacon:
                ev3.Sound.speak("I got the toy")
                robot.arm_up()
                time.sleep(1)
                robot.turn_degrees(180, 250)
                robot.drive_inches(12, 250)
                robot.arm_down()

            command = input("Hit enter to play fetch again or enter q to "
                            "quit: ")
            if command == "q":
                break
    except:
        traceback.print_exc()
        ev3.Sound.speak("Error")

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


main()



