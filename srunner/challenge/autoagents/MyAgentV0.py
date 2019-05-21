import carla
import matplotlib.pyplot as plt
import json
import pathlib
import numpy as np

from srunner.challenge.autoagents.autonomous_agent import AutonomousAgent


class MyAgentV0(AutonomousAgent):
    def setup(self, path_to_conf_file):
        """
        Initialize everything needed by your agent and set the track attribute to the right type:
            Track.ALL_SENSORS : LIDAR, cameras, GPS and speed sensor allowed
            Track.CAMERAS : Only cameras and GPS allowed
            Track.ALL_SENSORS_HDMAP_WAYPOINTS : All sensors and HD Map and waypoints allowed
            Track.SCENE_LAYOUT : No sensors allowed, the agent receives a high-level representation of the scene.
        """
        path_to_conf_file = pathlib.Path(path_to_conf_file)
        if not path_to_conf_file.exists():
            print("ERROR: not found path_to_conf_file = {}".format(path_to_conf_file))
            exit()
        with open(path_to_conf_file, "r") as config_file:
            config = json.load(config_file)
        # self.track = {Track.ALL_SENSORS, Track.CAMERAS, Track.ALL_SENSORS_HDMAP_WAYPOINTS, Track.SCENE_LAYOUT}
        # self.track = Track.ALL_SENSORS_HDMAP_WAYPOINTS

    def sensors(self):
        """
        Define the sensor suite required by the agent

        :return: a list containing the required sensors in the following format:

        [
            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                      'width': 300, 'height': 200, 'fov': 100, 'id': 'Left'},

            {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                      'width': 300, 'height': 200, 'fov': 100, 'id': 'Right'},

            {'type': 'sensor.lidar.ray_cast', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0,
             'id': 'LIDAR'}


        """
        sensors = [{'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.0, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0,
                    'width': 800, 'height': 600, 'fov': 100, 'id': 'Center'},
                   {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0,
                    'yaw': -45.0, 'width': 800, 'height': 600, 'fov': 100, 'id': 'Left'},
                   {'type': 'sensor.camera.rgb', 'x': 0.7, 'y': 0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0, 'yaw': 45.0,
                    'width': 800, 'height': 600, 'fov': 100, 'id': 'Right'},
                   {'type': 'sensor.lidar.ray_cast', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'roll': 0.0, 'pitch': 0.0,
                    'yaw': -45.0, 'id': 'LIDAR'},
                   {'type': 'sensor.other.gnss', 'x': 0.7, 'y': -0.4, 'z': 1.60, 'id': 'GPS'},
                   {'type': 'sensor.speedometer', 'reading_frequency': 25, 'id': 'speed'},
                   {'type': 'sensor.hd_map', 'reading_frequency': 1, 'id': 'hdmap'}

                   ]

        return sensors

    def run_step(self, input_data):

        print("=====================>")
        for key, val in input_data.items():
            if hasattr(val[1], 'shape'):
                shape = val[1].shape
                print("[{} -- {:06d}] with shape {}".format(key, val[0], shape))
        print("<=====================")

        gps_input = input_data["GPS"]
        gps_coords = list(gps_input[1])
        print(gps_coords)
        print(self.trace_path)
        self.trace_path.append(gps_coords)

        self.x.append(gps_coords[0])
        self.y.append(gps_coords[1])
        # self.sc.set_offsets(np.c_[self.x, self.y])
        # self.sc.set_xdata(self.x)
        # self.sc.set_ydata(self.y)
        # self.fig.canvas.draw_idle()
        self.ax.scatter(self.x, self.y)
        plt.show()
        plt.pause(0.1)

        plt.savefig("temp.png")

        # plt.scatter([e[0]for e in self.trace_path], [e[1]for e in self.trace_path])
        # plt.gca().set_aspect('equal', adjustable="box")
        # plt.grid()

        # DO SOMETHING SMART

        # RETURN CONTROL
        control = carla.VehicleControl()
        control.steer = 0.0
        control.throttle = 1.0
        control.brake = 0.0
        control.hand_brake = False

        return control
