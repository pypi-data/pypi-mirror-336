from serial import Serial
from serial.tools.list_ports import comports

class SerialLink(object):

    def __init__(self, port, baudrate=115200, start_marker = "<", end_marker = ">") -> None:
        self.serial: Serial = Serial(port, baudrate)
        self.start_marker = start_marker
        self.end_marker = end_marker
        self.new_data = False
        self.data = ""
        self.recv_in_progress = False
    
    def get_data(self):
        if self.new_data:
            self.new_data = False
            return self.data           
        return None
    
    def poll(self):

        while (self.serial.in_waiting > 0 and self.new_data == False):
            data = self.serial.read().decode("utf-8")
            if (self.recv_in_progress == True):
                if (data != self.end_marker):
                    self.data += data
                else:
                    self.recv_in_progress = False
                    self.new_data = True
            elif(data == self.start_marker):
                self.recv_in_progress = True
                self.data = ""            

    def send(self, data):
        data = f"{self.start_marker}{data}{self.end_marker}"
        self.serial.write(data.encode())

    def flush_port(self):
        print("[INFO] -> Flushing serial port")
        self.poll()
        while self.new_data:
            self.getData()
            self.poll()
        print("[INFO] -> Flushing serial port done...")

    def close(self):
        self.serial.close()
    
def get_ports(description=""):
    coms = comports()
    ports = []
    for port, desc, hwid in sorted(coms):
        if description != "":
            if description.lower() in desc.lower() or description.lower() in hwid.lower() :
                ports.append({"port": port, "desc":desc, "hwid": hwid})
        else:
            ports.append({"port": port, "desc":desc, "hwid": hwid})

    return ports