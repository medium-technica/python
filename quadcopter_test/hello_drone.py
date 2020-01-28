import dronekit
import dronekit_sitl
from dronekit import connect, VehicleMode
import socket
import exceptions

print ("Start simulator (SITL)")
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

# Connect to the Vehicle.

try:
	print("Connecting to vehicle on: %s" % (connection_string,))
	vehicle = connect(connection_string, wait_ready=True)

# Bad TCP connection
except socket.error:
    print 'No server exists!'

# Bad TTY connection
except exceptions.OSError as e:
    print 'No serial exists!'

# API Error
except dronekit.APIException:
    print 'Timeout!'

# Other error
except:
    print 'Some other error!'


# Get some vehicle attributes (state)
print ("Get some vehicle attribute values:")
print (" GPS: %s" % vehicle.gps_0)
print (" Battery: %s" % vehicle.battery)
print (" Last Heartbeat: %s" % vehicle.last_heartbeat)
print (" Is Armable?: %s" % vehicle.is_armable)
print (" System status: %s" % vehicle.system_status.state)
print (" Mode: %s" % vehicle.mode.name)    # settable

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
print("Completed")


