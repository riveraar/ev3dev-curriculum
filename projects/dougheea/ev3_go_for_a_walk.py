"""This function will run on the ev3. The ev3 will recieve information from
the pc about how to move around in response to the buttons on the GUI
Author: Emily Dougherty"""

import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    #  the code that connects and recieves information from the pc:
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()


main()
