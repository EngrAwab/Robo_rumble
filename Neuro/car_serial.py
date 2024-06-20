import serial
arduino_port = '/dev/ttyACM0'  # Update this based on your system
baud_rate = 9600 
try:
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Wait for the connection to initialize
    print("Serial connection established.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    ser = None
    
def send_command(command):
    """Send a command to the Arduino."""
    if ser:
        ser.write(command.encode())
        print(f"Sent command: {command}")
    else:
        st.error("Serial connection not established.")
def move_motor_forward():
    send_command('3')

def move_motor_backward():
    send_command('4')

def rotate_motor_left():
    send_command('2')

def rotate_motor_right():
    send_command('1')

def cam_left():
    send_command('2')

def cam_right():
    send_command('6')

def cam_up():
    send_command('7')

def cam_bottom():
    send_command('8')
    
    
