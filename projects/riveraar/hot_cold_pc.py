import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Hot or Cold?")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    direction_label = ttk.Label(main_frame, text='Direction')
    direction_label.grid(row=0, column=0)
    direction_entry = ttk.Entry(main_frame, width=8)
    direction_entry.insert(0, 'Left')
    direction_entry.grid(row=1, column=0)

    distance_label = ttk.Label(main_frame, text="Distance (in)")
    distance_label.grid(row=0, column=2)
    distance_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    distance_entry.insert(0, '5')
    distance_entry.grid(row=1, column=2)

    lit_cold_button = ttk.Button(main_frame, text='Small Cold')
    lit_cold_button.grid(row=3, column=0)
    lit_cold_button['command'] = lambda: small_cold(mqtt_client,
                                                    direction_entry,
                                                    distance_entry)
    root.bind('<c>', lambda event: small_cold(mqtt_client, direction_entry,
                                              distance_entry))

    lit_cold_button = ttk.Button(main_frame, text='Big Cold')
    lit_cold_button.grid(row=5, column=0)
    lit_cold_button['command'] = lambda: big_cold(mqtt_client,
                                                  direction_entry,
                                                  distance_entry)
    root.bind('<d>', lambda event: big_cold(mqtt_client, direction_entry,
                                            distance_entry))

    lit_cold_button = ttk.Button(main_frame, text='Small Hot')
    lit_cold_button.grid(row=3, column=2)
    lit_cold_button['command'] = lambda: small_hot(mqtt_client,
                                                   direction_entry,
                                                   distance_entry)
    root.bind('<h>', lambda event: small_hot(mqtt_client, direction_entry,
                                             distance_entry))

    lit_cold_button = ttk.Button(main_frame, text='Big Hot')
    lit_cold_button.grid(row=5, column=2)
    lit_cold_button['command'] = lambda: big_hot(mqtt_client,
                                                 direction_entry,
                                                 distance_entry)
    root.bind('<y>', lambda event: big_hot(mqtt_client, direction_entry,
                                           distance_entry))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=6, column=1)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=7, column=1)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()

    while not robot.touch_sensor.is_pressed:

        if robot.ir_sensor.proximity < 10:
            grab_object(robot)
            break

        time.sleep(0.05)

    robot.shutdown()
    quit_program(mqtt_client, True)
    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


def small_cold(mqtt_client, direction, distance):
    print("You're a little cold...")
    mqtt_client.send_message('small_cold', [direction.get(),
                                            int(distance.get())])


def big_cold(mqtt_client, direction, distance):
    print("You're ice cold...")
    mqtt_client.send_message('big_cold', [direction.get(),
                                          int(distance.get())])


def small_hot(mqtt_client, direction, distance):
    print("Warmer...")
    mqtt_client.send_message('small_hot', [direction.get(),
                                           int(distance.get())])


def big_hot(mqtt_client, direction, distance):
    print("RED HOT!!!")
    mqtt_client.send_message('small_hot', [direction.get(),
                                           int(distance.get())])


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def grab_object(robot):
    while robot.ir_sensor.proximity > 1:
        robot.forward(500, 500)

    robot.arm_up()

    ev3.Sound.speak("I got the thing. Please be proud of me, dad.").wait()


main()
