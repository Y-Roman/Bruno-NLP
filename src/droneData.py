import math

#DroneSDK
import dronekit_sitl
import time, sys

from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil


MAV_MODE_AUTO   = 4
const = 180/math.pi

sitl = dronekit_sitl.start_default()
#connection_string = '127.0.0.1:14540'
connection_string = 'COM3'

# Import DroneKit-Python
from dronekit import connect, VehicleMode

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=False)

####################################
#   Takefoff and Land Functions    #
####################################

def PX4setMode(mavMode):
    vehicle._master.mav.command_long_send(vehicle._master.target_system, vehicle._master.target_component,
                                               mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
                                               mavMode,
                                               0, 0, 0, 0, 0, 0)

def get_location_offset_meters(original_location, dNorth, dEast, alt):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
    specified `original_location`. The returned Location adds the entered `alt` value to the altitude of the `original_location`.
    The function is useful when you want to move the vehicle around specifying locations relative to
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt+alt)

home_position_set = False

def takeoff_land():
    #Create a message listener for home position fix
    @vehicle.on_message('HOME_POSITION')
    def listener(self, name, home_position):
        global home_position_set
        home_position_set = True

    # wait for a home position lock
    while not home_position_set:
        print ("Waiting for home position...")
        time.sleep(1)

    # Change to AUTO mode
    PX4setMode(MAV_MODE_AUTO)
    time.sleep(1)

    # Load commands
    cmds = vehicle.commands
    cmds.clear()

    home = vehicle.location.global_relative_frame

    # takeoff to 10 meters
    wp = get_location_offset_meters(home, 0, 0, 10);
    cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
    cmds.add(cmd)

    # land
    wp = get_location_offset_meters(home, 0, 0, 10);
    cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
    cmds.add(cmd)

    # Upload mission
    cmds.upload()
    time.sleep(2)

    # Arm vehicle
    vehicle.armed = True

    # monitor mission execution
    nextwaypoint = vehicle.commands.next
    while nextwaypoint < len(vehicle.commands):
        if vehicle.commands.next > nextwaypoint:
            display_seq = vehicle.commands.next+1
            print ("Moving to waypoint %s" % display_seq)
            nextwaypoint = vehicle.commands.next
        time.sleep(1)

    # wait for the vehicle to land
    while vehicle.commands.next > 0:
        time.sleep(1)

def get_droneInfo():
  version = vehicle.version
  print(version)
  lhb = vehicle.last_heartbeat
  print(lhb)
  isArmable = vehicle.is_armable
  print(isArmable)
  status = vehicle.system_status.state
  print(status)
  mode = vehicle.mode.name
  print(mode)
  armed = vehicle.armed
  print(armed)
  if(connection_string == 'COM9'):
    droneInfo = {"version": "Holybro Dev Kit", "lhb": lhb,"isArmable": isArmable, "status": "Standby", "mode": "Manual", "armed": armed}
  else:
    droneInfo = {"version": "PX4Copter-1.13.0-alpha0", "lhb": lhb,"isArmable": isArmable, "status": "Standby", "mode": "loiter", "armed": armed}
  #droneInfo = json.dumps({'version': 2, 'lhb': 3})
  return jsonify(droneInfo)
  

def get_drones():
  alt =vehicle.location.global_frame.alt
  #print(" Alt: %s" % alt)
  battLevel = vehicle.battery.level
  battVoltage = vehicle.battery.voltage
  print(" Battery Level: %s" % battLevel)
  print(" Battery Voltage: %s" % battVoltage)
  
  if(connection_string == 'COM9'):
    #print("Rangefinder: %s" % vehicle.rangefinder)
    #print ("Rangefinder distance: %s" % vehicle.rangefinder.distance)
    #print ("Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
    #print ("Rangefinder distance: %s" % vehicle.distance_sensor)
    lat = 'na'
    lon = 'na'
  else:
      lat = round(vehicle.location.global_frame.lat,3)
      lon = round(vehicle.location.global_frame.lon,3)
  
  print(" Lattitude: %s" % lat)
  print(" Longitude: %s" % lon)
  pitch = round((vehicle.attitude.pitch)*const,3)
  roll = round((vehicle.attitude.roll)*const,3)
  yaw = round((vehicle.attitude.yaw)*const,3)
  #print(" Pitch: %s" % pitch)
  #print(" Roll : %s" % roll)
  #print(" Yaw: %s" % yaw)
  
  sensor = {"id": 1, "name": "SOTI Vision Kit", "altitude": alt, "battVoltage": battVoltage,"battLevel": battLevel, "pitch": pitch, "roll": roll,"yaw": yaw, "lat": lat, "lon": lon}
  return jsonify(sensor)

def takeoff():
    print("Drone Takeoff Activated")
    takeoff_land()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


def isReadyToTakeOff():
    AngleThreshold = 15
    pitch = vehicle.attitude.pitch
    pitch = pitch*const
    roll = vehicle.attitude.roll
    roll = roll*const
    print("pitch: ", pitch)
    print("Roll : ", roll)
    if(abs(pitch) > AngleThreshold):
        return False
    elif(abs(roll) > AngleThreshold):
        print("False")
        return False
    else:
        print("True")
        return True
        
#if __name__ == '__main__':
#    while(1):
#        isReadyToTakeOff()
#        time.sleep(2)
    
    