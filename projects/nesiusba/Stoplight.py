# My project is going to consist of a single robot utilizing a pixy camera and color sensor, and a IR sensor.
# I will have the advanced track or just a regular circle track.
# The robot will follow the line around.
# Next the robot will use the IR sensor to stop anytime an object is in front of it.

# I will have 3 color signatures
# 1. Red = robot stops
# 2. green = robot goes forward
# 3. yellow = robot slows down.

# The color sensor will be used to make sure the robot follows the line

# My GUI will consist of a few different buttons
# Basically just all the buttons needed to control all the functions of the robot manually



import ev3dev.ev3 as ev3
import mqtt_remote_method_calls as com
import time
import robot_controller as robo

def main():
    print("--------------------------------------------")
    print("Stoplight")
    print("--------------------------------------------")

    white_level = 40
    black_level = 39
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)


    while not robot.touch_sensor.is_pressed:
        command_to_run = input("Enter a (autopilot), or q (for quit): ")
        if command_to_run == 'a':
            print("Follow the line until the touch sensor is pressed.")
            follow_the_line(robot, white_level, black_level)
        elif command_to_run == 'q':
            break
        else:
            print(command_to_run, "is not a known command. Please enter a valid choice.")

    mqtt_client.connect_to_pc()
    robot.loop_forever()
    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
    mqtt_client.close()

def follow_the_line(robot, white_level, black_level):
    """
    The robot follows the black line until the touch sensor is pressed.
    You will need a black line track to test your code
    When the touch sensor is pressed, line following ends, the robot stops, and control is returned to main.
    """
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    while not robot.touch_sensor.is_pressed:
        robot.stop()


        robot.pixy.mode = "SIG1"
        mqtt_client.send_message('on_rectangle_update', [robot.pixy.value(1), robot.pixy.value(2), robot.pixy.value(3),
                                                         robot.pixy.value(4)])
        if robot.pixy.value(3) > 50:
            print('STOP! Red Light')
            print("(X, Y)=({}, {}) Width={} Height={}".format(
                    robot.pixy.value(1), robot.pixy.value(2), robot.pixy.value(3),
                    robot.pixy.value(4)))
            robot.isStopped = True

        robot.pixy.mode = "SIG2"
        mqtt_client.send_message('on_rectangle_update', [robot.pixy.value(1), robot.pixy.value(2), robot.pixy.value(3),
                                                         robot.pixy.value(4)])
        if robot.pixy.value(3) > 50:
            print('GO! Green Light')
            robot.isStopped = False
            robot.leftSpeed = 200
            robot.rightSpeed = 200

        robot.pixy.mode = "SIG3"
        mqtt_client.send_message('on_rectangle_update', [robot.pixy.value(1), robot.pixy.value(2), robot.pixy.value(3),
                                                         robot.pixy.value(4)])
        if robot.pixy.value(3) > 50:
            robot.isStopped = False
            robot.leftSpeed = 100
            robot.rightSpeed = 100
        print("(X, Y)=({}, {}) Width={} Height={}".format(
            robot.pixy.value(1), robot.pixy.value(2), robot.pixy.value(3),
            robot.pixy.value(4)))
        mqtt_client.send_message('on_rectangle_update', [robot.pixy.value(1), robot.pixy.value(2), robot.pixy.value(3),
                                                         robot.pixy.value(4)])

        if robot.isStopped:
            robot.stop()
        else:
            if robot.color_sensor.reflected_light_intensity <= black_level:
                robot.forward(robot.leftSpeed, robot.rightSpeed)
            if robot.color_sensor.reflected_light_intensity >= white_level:
                robot.right(300, 200)
                time.sleep(.1)

    robot.stop()
    ev3.Sound.speak("Done")

main()