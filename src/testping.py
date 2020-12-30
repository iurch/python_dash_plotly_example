import subprocess
import platform

operating_sys = platform.system()
nas = '142.250.81.100' #google.com

ping_command = ['ping',nas,'-c 1']

ping_output = subprocess.run(ping_command,shell=False,stdout=subprocess.PIPE)

print(ping_output.stdout)