# This is to display where the pixy camera sees certain colors.

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, canvas, rectangle_tag):
        self.canvas = canvas
        self.rectangle_tag = rectangle_tag

    def on_rectangle_update(self, x, y, width, height):
        self.canvas.coords(self.rqectangle_tag, [x, y, x + width, y + height])


def main():
    root = tkinter.Tk()
    root.title = "Pixy display"

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    # The values from the Pixy range from 0 to 319 for the x and 0 to 199 for the y.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=320, height=200)
    canvas.grid(columnspan=2)

    rect_tag = canvas.create_rectangle(150, 90, 170, 110, fill="blue")

    # Buttons for quit and exit
    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    # Create an MQTT connection
    my_delegate = MyDelegate(canvas, rect_tag)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter event handler
# ----------------------------------------------------------------------
def quit_program(mqtt_client):
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()