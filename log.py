import time
def log_vehicle(vehicle,logFile):
	logFile.write("time:"+time.asctime(time.localtime(time.time()))+"\n"
            +str(vehicle.location.global_relative_frame)+'\n'
            +"velocity:"+str(vehicle.velocity)+'\n'
            +"system_status:"+str(vehicle.system_status.state)+'\n'
            +"vehicle mode:"+str(vehicle.mode.name)+'\n'
            +"EKF ok?:"+str(vehicle.ekf_ok)+'\n'
            +str(vehicle.attitude)+"\n"
            +str(vehicle.battery)+"\n\n")
