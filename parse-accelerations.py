import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

SERIAL_PORT = 'COM3'
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Data lists
time_data = []
accel_data = [[], [], []]  # ax, ay, az

def parse_line(line):
    try:
        if not line.startswith("A:") or ";G:" not in line:
            return None

        acc_str = line.split(';')[0][2:]  # Strip "A:"
        ax, ay, az = map(float, acc_str.split(','))
        return ax, ay, az
    except Exception as e:
        print(f"Parse error: {e} -> {line}")
        return None

def update(frame):
    line = ser.readline().decode('utf-8', errors='ignore')
    parsed = parse_line(line)
    if parsed:
        ax, ay, az = parsed
        accel_data[0].append(ax)
        accel_data[1].append(ay)
        accel_data[2].append(az)
        time_data.append(len(time_data))

        for i, line in enumerate(ax_lines):
            line.set_data(time_data, accel_data[i])

        # Auto-scale y-axis based on data
        all_vals = accel_data[0] + accel_data[1] + accel_data[2]
        if all_vals:
            y_min = min(all_vals) - 1
            y_max = max(all_vals) + 1
            ax1.set_ylim(y_min, y_max)

        ax1.set_xlim(max(0, len(time_data) - 200), len(time_data))  # keep 200 samples visible

    return ax_lines

# Plot setup
fig, ax1 = plt.subplots()
ax_lines = [
    ax1.plot([], [], label='Ax')[0],
    ax1.plot([], [], label='Ay')[0],
    ax1.plot([], [], label='Az')[0],
]
ax1.set_ylim(-2, 2)
ax1.set_title("Accelerometer")
ax1.set_xlabel("Sample")
ax1.set_ylabel("Acceleration (g)")
ax1.legend()

ani = FuncAnimation(fig, update, interval=50)
plt.show()
