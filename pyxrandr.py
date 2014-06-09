import subprocess

class pyxrandr():
    def __init__(self):
        prog = subprocess.Popen('xrandr',stdout=subprocess.PIPE)
        (output, err) = prog.communicate()
        self.devices = dict()
        output = output.splitlines()
        for line in output:
            if line.find('connected') == -1:
                continue
            self.devices[line.split()[0]] = line.split()[1]
    def getConnectedDevices(self):
        connected = list()
        for dev in self.devices.keys():
            if self.devices[dev]=='connected':
                connected.append(dev)
        return connected

