import RPi.GPIO as io
import paho.mqtt.client as mqtt

io.setwarnings(False)
io.setmode(io.BOARD)

# Pin Configuration
ENA, IN1, IN2 = 11, 16, 18
ENB, IN3, IN4 = 13, 8, 10

# Setup Pins
for pin in [ENA, IN1, IN2, ENB, IN3, IN4]:
    io.setup(pin, io.OUT)

# Create PWM
pwm_a, pwm_b = io.PWM(ENA, 100), io.PWM(ENB, 100)
pwm_a.start(50)  # duty
pwm_b.start(50)

def set_motor_pins(in1, in2, in3, in4):
    io.output(IN1, in1)
    io.output(IN2, in2)
    io.output(IN3, in3)
    io.output(IN4, in4)

def forward():
    set_motor_pins(1, 0, 1, 0)

def backward():
    set_motor_pins(0, 1, 0, 1)

def stopfcn():
    set_motor_pins(0, 0, 0, 0)

def right():
    set_motor_pins(1, 0, 0, 0)

def left():
    set_motor_pins(0, 0, 1, 0)

MQTT_SERVER = "localhost"
MQTT_PATH = "hand"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, message):
    if message.payload == b'5':
        forward()
    elif message.payload == b'0':
        stopfcn()
    elif message.payload == b'4':
        backward()
    elif message.payload == b'1':
        left()
    elif message.payload == b'2':
        right()
    else:
        stopfcn()

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_SERVER, 1883, 60)
    mqtt_client.loop_start()

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
