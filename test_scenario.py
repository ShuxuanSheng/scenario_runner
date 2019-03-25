
import carla
from srunner.scenariomanager.carla_data_provider import CarlaActorPool, CarlaDataProvider
from srunner.scenarios.config_parser import ScenarioConfiguration, ActorConfigurationData

from srunner.scenarios.opposite_vehicle_taking_priority import OppositeVehicleRunningRedLight
import time
client = carla.Client('localhost', int(2000))
client.set_timeout(25.0)
world = client.load_world('Town01')
world.wait_for_tick()

CarlaActorPool.set_world(world)
CarlaDataProvider.set_world(world)

ego_transform = carla.Transform(location = carla.Location(x=338.703, y=227.451, z=0.0),
                                rotation = carla.Rotation(roll=0.0, pitch=0.0, yaw=-90.0))

ego_trigger_transform = carla.Transform(location=carla.Location(x=156.42, y=230.16, z=1.0),
                                        rotation = carla.Rotation(roll=0.0, pitch=0.0, yaw=90.0))


ego_vehicle = CarlaActorPool.setup_actor('vehicle.lincoln.mkz2017', ego_transform, True)
world.wait_for_tick()

time.sleep(0.2)

# Build a master first


scenario_configuration = ScenarioConfiguration()
scenario_configuration.other_actors = [ActorConfigurationData('vehicle.lincoln.mkz2017', ego_trigger_transform)]
scenario_configuration.town = 'Town01'
scenario_configuration.ego_vehicle = ActorConfigurationData('vehicle.lincoln.mkz2017', ego_transform)


scenario_instance = OppositeVehicleRunningRedLight(world, ego_vehicle, scenario_configuration)
