import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- CONFIG ---
SERIAL_PORT = 'COM3'     # Change to your port (e.g., '/dev/ttyUSB0' on Linux)
BAUD_RATE = 115200
MAX_POINTS = 200         # Number of samples shown in the plot

# --- Set up serial ---
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# --- Data containers ---
time_data = []
accel_data = [[], [], []]  # Ax, Ay, Az
gyro_data = [[], [], []]   # Gx, Gy, Gz

# --- Parse incoming line ---
def parse_line(line):
    try:
        if not line.startswith("A:") or ";G:" not in line:
            return None
        acc_str, gyro_str = line.strip().split(';')
        ax, ay, az = map(float, acc_str[2:].split(','))
        gx, gy, gz = map(float, gyro_str[2:].split(','))
        return (ax, ay, az), (gx, gy, gz)
    except Exception as e:
        print(f"Parse error: {e} -> {line.strip()}")
        return None

# --- Set up plots ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle("MPU6050 Real-Time Data")

ax_lines = [ax1.plot([], [], label='Ax')[0],
            ax1.plot([], [], label='Ay')[0],
            ax1.plot([], [], label='Az')[0]]

gx_lines = [ax2.plot([], [], label='Gx')[0],
            ax2.plot([], [], label='Gy')[0],
            ax2.plot([], [], label='Gz')[0]]

for ax in (ax1, ax2):
    ax.set_xlim(0, MAX_POINTS)
    ax.set_ylim(-20, 20)
    ax.legend()
    ax.grid(True)

ax1.set_ylabel("Acceleration (g)")
ax2.set_ylabel("Gyro (rad/s)")
ax2.set_xlabel("Sample")

# --- Animation update function ---
def update(frame):
    line = ser.readline().decode('utf-8', errors='ignore')
    parsed = parse_line(line)
    if parsed:
        (ax, ay, az), (gx, gy, gz) = parsed

        time_data.append(len(time_data))
        accel_data[0].append(ax)
        accel_data[1].append(ay)
        accel_data[2].append(az)
        gyro_data[0].append(gx)
        gyro_data[1].append(gy)
        gyro_data[2].append(gz)

        # Limit data to MAX_POINTS
        for data_list in [time_data] + accel_data + gyro_data:
            if len(data_list) > MAX_POINTS:
                data_list.pop(0)

        # Update plot data
        for i in range(3):
            ax_lines[i].set_data(range(len(time_data)), accel_data[i])
            gx_lines[i].set_data(range(len(time_data)), gyro_data[i])

        ax1.set_xlim(0, len(time_data))
        ax2.set_xlim(0, len(time_data))

    return ax_lines + gx_lines

ani = FuncAnimation(fig, update, interval=50, cache_frame_data=False)
plt.tight_layout()
plt.show()
