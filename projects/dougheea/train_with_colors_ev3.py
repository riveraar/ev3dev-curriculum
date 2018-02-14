"""This function will run on the ev3. The ev3 will recieve information from
the pc about what to do in response to the color that it sees
Author: Emily Dougherty"""

import mqtt_remote_method_calls as com
import robot_controller as robo

robot = robo.Snatch3r()


def main():
    while not robot.touch_sensor.is_pressed:    # this code has the  robot
        # listening for information from the pc
        mqtt_client = com.MqttClient(robot)
        mqtt_client.connect_to_pc()
        robot.loop_forever()


main()
