import time
import serial
import serial.tools.list_ports

TRIES = 100


def get_port():
    port_list = [i.device for i in list(serial.tools.list_ports.comports())]
    ports = sorted(port_list, reverse=True)
    if len(ports) == 1:
        return ports[0]
    else:
        print("Available ports:")
        for idx, port in enumerate(ports):
            print(f"{idx+1: <3} : {port}")
        selection = 0
        while selection not in range(1, len(ports) + 1):
            try:
                selection = int(input("Please select a serial device: "))
            except ValueError:
                pass
        return ports[selection - 1]


def main():
    try:
        device = serial.Serial(port=get_port(), baudrate=115200)
    except serial.serialutil.SerialException:
        print('Unable to open serial port')
    else:
        error_count = 0
        device.reset_input_buffer()
        device.reset_output_buffer()
        time.sleep(0.010)
        for i in range(TRIES):
            send_bytes = f"Hello world ({i})".encode('utf-8')
            recv_bytes = device.read(device.write(send_bytes))
            print(f"Send: {send_bytes}\tReceived: {recv_bytes}")
            if recv_bytes != send_bytes:
                error_count += 1
        print(f"tries = {TRIES}")
        print(f"error_count = {error_count}")
        print(f"error_rate = {100 * (error_count/TRIES)}%")


if __name__ == "__main__":
    main()
