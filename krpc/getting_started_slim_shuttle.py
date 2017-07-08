import math
import numpy as np
import time
import krpc

turn_end_altitude = 70000.0

#to be used with KSP's slim shuttle
conn = krpc.connect(name='Launch into orbit')
vessel = conn.space_center.active_vessel
print(vessel.name)

# Set up streams for telemetry
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
stage_4_resources = vessel.resources_in_decouple_stage(stage=4, cumulative=False)
stage_3_resources = vessel.resources_in_decouple_stage(stage=3, cumulative=False)
stage_1_resources = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
srb_fuel = conn.add_stream(stage_4_resources.amount, 'SolidFuel')
main_fuel = conn.add_stream(stage_4_resources.amount, 'LiquidFuel')
refframe = vessel.orbit.body.reference_frame
position = conn.add_stream(vessel.position, refframe)
velocity = conn.add_stream(vessel.velocity, refframe)
vehicle_mass = conn.add_stream(getattr, vessel, 'mass')
def cartesian_ref_to_polar():
    pass


# Pre-launch setup
vessel.control.sas = False
vessel.control.rcs = False
vessel.control.throttle = 1.0
#Grab initial data
#INITIAL_POSITION (
INITIAL_POSITION_kcef = np.asarray(position())
INITIAL_VELOCITY_kcef = np.asarray(velocity())
# Countdown...
'''
print('3...')
time.sleep(1)
print('2...')
time.sleep(1)
'''
print('1...')
time.sleep(1)
print('Launch!')
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)
pitch = 90.0
last_dmdt = 0.00001
class Trajectory(object):
    def __init__(self):
        self.ut =
def update():
    ut_now = ut()
    mass_now = vehicle_mass()
    dt = ut_now-last_ut
    if dt != 0.0:
        dm = mass_now-last_mass
        dmdt = dm/dt
        new_pos_kcef = np.asarray(position())
        pos_diff_mag = np.linalg.norm(INITIAL_POSITION_kcef-new_pos_kcef)
        hr = altitude()/turn_end_altitude
        if hr < 0.0:
            hr = 0.0
        pitch = 90*(1.0-hr)**2.0

        print("kcef {}. dt {}. dm {}. dm/dt {}".format(new_pos_kcef,dt,dm, dmdt))
        print ("hr {}. pitch {}.".format(hr,pitch))
        last_ut = ut_now
        last_mass = mass_now
        last_dmdt = dmdt

vessel.auto_pilot.target_pitch_and_heading(pitch,90)
while srb_fuel !=0.0:
    update()
    time.sleep(.1)
vessel.control.activate_next_stage()
while liquid_fuel !=0.0:
    update()
    time.sleep(.1)
vessel.control.activate_next_stage()

