import serial, time, threading, serial.tools.list_ports, socket
from flask import Flask, render_template_string, jsonify
from pathlib import Path
from vlc import MediaPlayer

THUNDER_PATH = Path("./thunder.mp3")
BACH_PATH = Path("./bach.mp3")
BAUD_RATE = 9600
SERIAL_PORT = ""

# Time delays in seconds
time_delays = [3, 2, 2, 5, 1, 4]

def get_serial_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        raise Exception("No serial ports found")
    for port in ports:
        print(f"Found port: {port.device} - {port.description}")
        if "IOUSBHostDevice" in port.description:
            return port.device
    raise Exception("No Arduino Uno found")

def queue_lightning_serial_commands():
    with serial.Serial(SERIAL_PORT, BAUD_RATE) as ser:
        for delay in time_delays:
            time.sleep(delay)
            ser.write(b'1')

def send_stop_strobe_command():
    with serial.Serial(SERIAL_PORT, BAUD_RATE) as ser:
        ser.write(b'2')

def play_thunder():
    process = MediaPlayer(THUNDER_PATH)
    process.play()

def play_bach(seconds=16):
    process = MediaPlayer(BACH_PATH)
    process.play()
    threading.Timer(seconds, process.stop).start()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

SERIAL_PORT = get_serial_port()

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    local_ip = get_local_ip()
    return render_template_string(open('static/index.html').read(), local_ip=local_ip)

@app.route("/play")
def haunted_house():
    send_stop_strobe_command()
    time.sleep(1)
    play_thunder()
    play_bach()

    threading.Thread(target=queue_lightning_serial_commands).start()

    return jsonify({"status": "done"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)