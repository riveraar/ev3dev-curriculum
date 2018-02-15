"""This code will allow the 'dogbot' to be trained to recognize certain
colors (even though dogs are blind!!) The user will enter a vaild color into
the entry box on the GUI and then the dogbot will know to look for that
color. When the color is found, the dogbot will bark."""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3() #  connected to the robot

    # creating the GUI window:
    root = tkinter.Tk()
    root.title = "Color Training"

    frame1 = ttk.Frame(root, padding=40)
    frame1.grid()

    button_label = ttk.Label(frame1, text=" Enter one of these colors:")
    button_label.grid(row=1, column=1)

    button_label = ttk.Label(frame1, text=" blue, red, or green")
    button_label.grid(row=2, column=1)

    entry = ttk.Entry(frame1)
    entry.grid(row=3, column=1)

    color_entry_button = ttk.Button(frame1, text='Color Entry')
    color_entry_button.grid(row=4, column=1)
    color_entry_button["command"] = lambda: choose_color(mqtt_client, entry)

    root.mainloop()

#  this method calls these functions from the robot library


def choose_color(mqtt_client, entry):
    color_name = entry.get()
    if color_name == 'green':
        mqtt_client.send_message('do_green', [])
    if color_name == 'blue':
        mqtt_client.send_message('do_blue', [])
    if color_name == 'red':
        mqtt_client.send_message('do_red', [])


main()
