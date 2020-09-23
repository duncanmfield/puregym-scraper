import config
from datetime import datetime
import matplotlib.pyplot as plt

show_3d = False
date_fmt = '%Y-%m-%d %H:%M:%S'
counts = []
times = []


def append(date, count):
    counts.append(count)
    times.append(date)


def run():
    with open(config.log_file) as file:
        for raw_line in file:
            line = raw_line.strip('\n')
            [raw_date, raw_count] = line.split(" -> ")
            date = datetime.strptime(raw_date, date_fmt)
            count = int(raw_count)

            append(date, count)

    if show_3d:
        plot_3d()
    else:
        plot_2d()


def plot_3d():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([t.hour + (t.minute / 60) for t in times], [t.weekday() + (t.hour + (t.minute / 60)) / 24 for t in times], counts)
    ax.set_xlim3d(0, 24)
    ax.set_xlabel("Hour of the Day")
    ax.set_ylim3d(1, 7)
    ax.set_ylabel("Day of the Week")
    ax.set_zlim3d(0, max_people)
    ax.set_zlabel("Gym Users")
    plt.show()


def plot_2d():
    plt.scatter([t.hour + (t.minute / 60) for t in times], counts, s=16, color=['#002147'], marker='x')
    plt.xlabel("Hour of the Day")
    plt.ylabel("PureGym Users")
    plt.title("PureGym Users")
    plt.grid(which='major')
    plt.xlim([0, 24])
    plt.show()


run()