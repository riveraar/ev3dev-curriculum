"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_D)
        self.isStopped = True
        self.leftSpeed = 200
        self.rightSpeed = 200

        assert self.left_motor.connected
        assert self.right_motor.connected

        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert self.arm_motor.connected

        self.touch_sensor = ev3.TouchSensor()
        assert self.touch_sensor

        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor

        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor

        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy



        self.MAX_SPEED = 900

    def drive_inches(self, inches_to_drive, drive_speed_sp):
        self.left_motor.run_to_rel_pos(position_sp=inches_to_drive * 90,
                                       speed_sp=drive_speed_sp,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=inches_to_drive * 90,
                                        speed_sp=drive_speed_sp,
                                        stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        self.left_motor.run_to_rel_pos(position_sp=-degrees_to_turn * 4,
                                       speed_sp=turn_speed_sp,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn * 4,
                                        speed_sp=turn_speed_sp,
                                        stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def forward(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def backward(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def left(self, left_speed_entry, right_speed_entry):
        self.right_motor.run_forever(speed_sp=right_speed_entry)
        self.left_motor.run_forever(speed_sp=-left_speed_entry)

    def right(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.01)

    def shutdown(self):
        self.running = False

    def seek_beacon(self):

        beacon_seeker = ev3.BeaconSeeker(channel=1)

        while not self.touch_sensor.is_pressed:

            current_heading = beacon_seeker.heading  # use the beacon_seeker
            # heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker
            # distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    if current_distance > 1:
                        self.forward(200, 200)
                        print("on current heading, distance =",
                              current_distance)
                if current_distance == 1:
                    print('Z marks the spot!!!')
                    time.sleep(1.0)
                    self.stop()
                    return True
                if math.fabs(current_heading) > 2 and math.fabs(
                        current_distance) < 10:
                    if current_heading < 2:
                        print('wrong way! turning left')
                        self.left(200, 200)
                        time.sleep(.2)
                    if current_heading >= -2:
                        print('wrony way! turning right')
                        self.right(200, 200)
                        time.sleep(.2)
                if math.fabs(current_heading) > 10:
                    print('Heading too far off')
            time.sleep(.5)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False

    def do_green(self):
        self.pixy.mode = "SIG1"  # make green = to sig 1!!!
        while not self.touch_sensor.is_pressed:

            width = self.pixy.value(3)
            print("(X, Y)=({}, {}) Width={} Height={}".format(
                self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                self.pixy.value(4)))
            if width > 0:
                ev3.Sound.speak("woof woof")
                print(' found green')
                time.sleep(.2)

            time.sleep(1)

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

    def do_blue(self):
        self.pixy.mode = "SIG2"  # make blue = to sig 2!!!
        while not self.touch_sensor.is_pressed:

            width = self.pixy.value(3)
            print("(X, Y)=({}, {}) Width={} Height={}".format(
                self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                self.pixy.value(4)))
            if width > 0:
                ev3.Sound.speak("bow wow")
                print('found orange')
                time.sleep(.2)

            time.sleep(1)

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

    def do_red(self):
        self.pixy.mode = "SIG3"  # make red = to sig 3!!!
        while not self.touch_sensor.is_pressed:

            width = self.pixy.value(3)
            print("(X, Y)=({}, {}) Width={} Height={}".format(
                self.pixy.value(1), self.pixy.value(2), self.pixy.value(3),
                self.pixy.value(4)))
            if width > 0:
                ev3.Sound.speak("bark bark bark")
                print('found pink')
                time.sleep(.2)

            time.sleep(1)

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

    def small_cold(self, direction, distance):
        if direction == "Left":
            ev3.Sound.speak('Turning a little to the left...')
            self.turn_degrees(-45, 500)
            self.drive_inches(distance, 500)
        elif direction == "Right":
            ev3.Sound.speak("Turning a little to the right...")
            self.turn_degrees(45, 500)
            self.drive_inches(distance, 500)

    def big_cold(self, direction, distance):
        if direction == "Left":
            ev3.Sound.speak('Turning to the left...')
            self.turn_degrees(-90, 500)
            self.drive_inches(distance, 500)
        elif direction == "Right":
            ev3.Sound.speak("Turning to the right...")
            self.turn_degrees(90, 500)
            self.drive_inches(distance, 500)

    def little_hot(self, direction, distance):
        if direction == "Left":
            ev3.Sound.speak('Turning a litle to the left...')
            self.turn_degrees(-25, 500)
            self.drive_inches(distance, 500)
        elif direction == "Right":
            ev3.Sound.speak("Turning a little to the right...")
            self.turn_degrees(25, 500)
            self.drive_inches(distance, 500)

    def big_hot(self, direction, distance):
        if direction == "Left":
            ev3.Sound.speak('Turning to the left...')
            self.turn_degrees(-10, 500)
            self.drive_inches(distance, 500)
        elif direction == "Right":
            ev3.Sound.speak("Turning to the right...")
            self.turn_degrees(10, 500)
            self.drive_inches(distance, 500)
