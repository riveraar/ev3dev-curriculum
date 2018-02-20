"""
This is the PC side of the Hot or Cold project.
The purpose of this module is allowing the PC to connect to the EV3 robot
and communicate with it throughout the other module that the Snatcher robot
uses. For this code in particular, I designed a GUI that sends messages to
the robot and follow those instructions as planned, which in this case is
whether or not the robot is closed to the object it is trying to find.

Author: Angel Rivera
"""
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    #   Sets up the Mqtt Client and connects the PC to the EV3 robot
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    #   Creates a window with the title
    root = tkinter.Tk()
    root.title("Hot or Cold?")
    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    #   Labels an entry box, which is for deciding which direction the EV3
    #   robot should move to.
    direction_label = ttk.Label(main_frame, text='Direction')
    direction_label.grid(row=0, column=0)
    direction_entry = ttk.Entry(main_frame, width=8)
    direction_entry.insert(0, 'Left')
    direction_entry.grid(row=1, column=0)

    #   Labels another entry box, this time for deciding how far the EV3
    #   robot will move to
    distance_label = ttk.Label(main_frame, text="Distance (in)")
    distance_label.grid(row=0, column=2)
    distance_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    distance_entry.insert(0, '5')
    distance_entry.grid(row=1, column=2)

    #   Creates a button with a function to it and binding it to a keyboard
    #   button, where it follows the small_cold function and uses the entry
    #   from the direction and distance and adds those values accordingly
    lit_cold_button = ttk.Button(main_frame, text='Small Cold')
    lit_cold_button.grid(row=3, column=0)
    lit_cold_button['command'] = lambda: small_cold(mqtt_client,
                                                    direction_entry,
                                                    distance_entry)
    root.bind('<c>', lambda event: small_cold(mqtt_client, direction_entry,
                                              distance_entry))

    #   The next 3 blocks of code are similar to the one above, just with
    #   different variations of the key bindings and the function attachments
    #   in place of the overall module and GUI
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

    #   Adds a quit button that allows for the user to quit the GUI but not
    #   the entirety of the program itself.
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=6, column=1)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    #   Adds an exit button that allows for the user to exit on both the GUI
    #   and the program itself in its entirety.
    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=7, column=1)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


#  This function sends a message where the robot moves at 45 degrees in either
#  direction given and move a certain distance given in order to reach the 
#  object in question
def small_cold(mqtt_client, direction, distance):
    print("You're a little cold...")
    mqtt_client.send_message('small_cold', [direction.get(),
                                            int(distance.get())])


#  This function sends a message where the robot moves at 90 degrees in either
#  direction given and move a certain distance given in order to reach the 
#  object in question
def big_cold(mqtt_client, direction, distance):
    print("You're ice cold...")
    mqtt_client.send_message('big_cold', [direction.get(),
                                          int(distance.get())])


#  This function sends a message where the robot moves in either
#  direction given and move a certain distance given in order to reach the 
#  object in question
def small_hot(mqtt_client, direction, distance):
    print("Warmer...")
    mqtt_client.send_message('small_hot', [direction.get(),
                                           int(distance.get())])


#  This function sends a message where the robot moves a little bit in either
#  direction given and move a certain distance given in order to reach the 
#  object in question
def big_hot(mqtt_client, direction, distance):
    print("RED HOT!!!")
    mqtt_client.send_message('small_hot', [direction.get(),
                                           int(distance.get())])


# This function sends a message where both the robot and the window screen is
# shutdown based on the input "Exit" on the GUI
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# Begins the main code above
main()
