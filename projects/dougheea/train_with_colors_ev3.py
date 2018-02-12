

import mqtt_remote_method_calls as com
import robot_controller as robo

robot = robo.Snatch3r()


def main():
    while not robot.touch_sensor.is_pressed:
        mqtt_client = com.MqttClient(robot)
        mqtt_client.connect_to_pc()
        robot.loop_forever()


main()
