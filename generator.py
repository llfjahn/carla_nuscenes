from client import Client
from dataset import Dataset
import traceback
import random

class Generator:
    def __init__(self,config):
        self.config = config
        self.collect_client = Client(self.config["client"])

    def generate_new_dataset(self):
        print("generate new dataset!")
        self.dataset = Dataset(**self.config["dataset"])
        self.dataset.save()
        for sensor in self.config["sensors"]:
            self.dataset.update_sensor(sensor["name"],sensor["modality"])
        for category in self.config["categories"]:
            self.dataset.update_category(category["name"],category["description"])
        for attribute in self.config["attributes"]:
            self.dataset.update_attribute(attribute["name"],category["description"])
        for visibility in self.config["visibility"]:
            self.dataset.update_visibility(visibility["description"],visibility["level"])

        for world_config in self.config["worlds"]:
            try:
                self.collect_client.generate_world(world_config)
                map_token = self.dataset.update_map(world_config["map_name"],world_config["map_category"])
                for capture_config in world_config["captures"]:
                    log_token = self.dataset.update_log(map_token,capture_config["date"],capture_config["time"],
                                            capture_config["timezone"],capture_config["capture_vehicle"],capture_config["location"])
                    for scene_id,scene_config in enumerate(capture_config["scenes"]):
                        print("current_scene_count:",self.dataset.data["current_scene_count"])
                        scene_token = self.add_one_scene(log_token,scene_id,scene_config)
                        self.dataset.update_scene_count()
                        self.dataset.save()
            except:
                traceback.print_exc()
            finally:
                self.collect_client.destroy_world()

    def continue_generating_dataset(self):
        print("continue generating!")
        scene_count=0
        self.dataset = Dataset(**self.config["dataset"],load=True)
        for sensor in self.config["sensors"]:
            self.dataset.update_sensor(sensor["name"],sensor["modality"],False)
        for category in self.config["categories"]:
            self.dataset.update_category(category["name"],category["description"],False)
        for attribute in self.config["attributes"]:
            self.dataset.update_attribute(attribute["name"],category["description"],False)
        for visibility in self.config["visibility"]:
            self.dataset.update_visibility(visibility["description"],visibility["level"],False)

        for world_config in self.config["worlds"]:
            try:
                self.collect_client.generate_world(world_config)
                map_token = self.dataset.update_map(world_config["map_name"],world_config["map_category"],False)
                for capture_config in world_config["captures"]:
                    log_token = self.dataset.update_log(map_token,capture_config["date"],capture_config["time"],
                                            capture_config["timezone"],capture_config["capture_vehicle"],capture_config["location"],False)
                    for scene_id,scene_config in enumerate(capture_config["scenes"]):
                        scene_count+=1
                        if scene_count>self.dataset.data["current_scene_count"]:
                            print("current_scene_count:",self.dataset.data["current_scene_count"])
                            scene_token = self.add_one_scene(log_token,scene_id,scene_config)
                            self.dataset.update_scene_count()
                            self.dataset.save()
            except:
                traceback.print_exc()
            finally:
                self.collect_client.destroy_world()

    def generate_new_random_dataset(self):
        print("generate new dataset!")
        self.dataset = Dataset(**self.config["dataset"])
        self.dataset.save()
        for sensor in self.config["sensors"]:
            self.dataset.update_sensor(sensor["name"],sensor["modality"])
        for category in self.config["categories"]:
            self.dataset.update_category(category["name"],category["description"])
        for attribute in self.config["attributes"]:
            self.dataset.update_attribute(attribute["name"],category["description"])
        for visibility in self.config["visibility"]:
            self.dataset.update_visibility(visibility["description"],visibility["level"])
        i = 0
        for world_config in self.config["worlds"]:
            for scene_id in range(self.config["scene_count"]):
                # world_config = random.choice(self.config["worlds"])
                try:
                    self.collect_client.generate_world(world_config)
                    map_token = self.dataset.update_map(world_config["map_name"],world_config["map_category"])
                    capture_config = random.choice(world_config["captures"])
                    log_token = self.dataset.update_log(map_token,capture_config["date"],capture_config["time"],
                                            capture_config["timezone"],capture_config["capture_vehicle"],capture_config["location"])
                    scene_config = random.choice(capture_config["scenes"])
                    scene_config["description"] += str(scene_id)
                    print("current_scene_count:",self.dataset.data["current_scene_count"])
                    scene_token = self.add_one_scene(log_token,scene_id,scene_config)
                    self.dataset.update_scene_count()
                    self.dataset.save()
                except:
                    traceback.print_exc()
                finally:
                    self.collect_client.destroy_world()

    def continue_generating_random_dataset(self):
        print("continue generating!")

        self.dataset = Dataset(**self.config["dataset"],load=True)
        for sensor in self.config["sensors"]:
            self.dataset.update_sensor(sensor["name"],sensor["modality"],False)
        for category in self.config["categories"]:
            self.dataset.update_category(category["name"],category["description"],False)
        for attribute in self.config["attributes"]:
            self.dataset.update_attribute(attribute["name"],category["description"],False)
        for visibility in self.config["visibility"]:
            self.dataset.update_visibility(visibility["description"],visibility["level"],False)


        for world_config in self.config["worlds"]:

            # for scene_id in range(self.dataset.data["current_scene_count"],self.config["scene_count"]):
            for scene_id in range(0,self.config["scene_count"]):
                # world_config = random.choice(self.config["worlds"])
                try:
                    self.collect_client.generate_world(world_config)
                    map_token = self.dataset.update_map(world_config["map_name"],world_config["map_category"])
                    capture_config = random.choice(world_config["captures"])
                    log_token = self.dataset.update_log(map_token,capture_config["date"],capture_config["time"],
                                            capture_config["timezone"],capture_config["capture_vehicle"],capture_config["location"])
                    scene_config = random.choice(capture_config["scenes"])
                    scene_config["description"] += str(scene_id)
                    print("current_scene_count:",self.dataset.data["current_scene_count"])
                    scene_token = self.add_one_scene(log_token,scene_id,scene_config)
                    self.dataset.update_scene_count()
                    self.dataset.save()
                except:
                    traceback.print_exc()
                finally:
                    self.collect_client.destroy_world()

    def add_one_scene(self,log_token,scene_id,scene_config):
        try:
            calibrated_sensors_token = {}
            samples_data_token = {}
            instances_token = {}
            samples_annotation_token = {}

            self.collect_client.generate_scene(scene_config)
            scene_token = self.dataset.update_scene(log_token,scene_id,scene_config["description"])

            for instance in self.collect_client.walkers+self.collect_client.vehicles:
                instance_token = self.dataset.update_instance(*self.collect_client.get_instance(scene_id,instance))
                instances_token[instance.get_actor().id] = instance_token
                samples_annotation_token[instance.get_actor().id] = ""
            
            for sensor in self.collect_client.sensors:
                calibrated_sensor_token = self.dataset.update_calibrated_sensor(scene_token,*self.collect_client.get_calibrated_sensor(sensor))
                calibrated_sensors_token[sensor.name] = calibrated_sensor_token
                samples_data_token[sensor.name] = ""




            sample_token = ""
            for frame_count in range(int(scene_config["collect_time"]/self.collect_client.settings.fixed_delta_seconds)):
                print("frame count:",frame_count)
                self.collect_client.tick()
                if (frame_count+1)%int(scene_config["keyframe_time"]/self.collect_client.settings.fixed_delta_seconds) == 0:
                    sample_token = self.dataset.update_sample(sample_token,scene_token,*self.collect_client.get_sample())
                    for sensor in self.collect_client.sensors:
                        if sensor.bp_name in ['sensor.camera.rgb','sensor.other.radar','sensor.lidar.ray_cast']:
                            for idx,sample_data in enumerate(sensor.get_data_list()):
                                ego_pose_token = self.dataset.update_ego_pose(scene_token,calibrated_sensors_token[sensor.name],*self.collect_client.get_ego_pose(sample_data))
                                is_key_frame = False
                                print(idx)
                                print(len(sensor.get_data_list())-1)
                                if idx == len(sensor.get_data_list())-1:
                                    is_key_frame = True
                                if is_key_frame:
                                    samples_data_token[sensor.name] = self.dataset.update_sample_data(samples_data_token[sensor.name],calibrated_sensors_token[sensor.name],sample_token,ego_pose_token,is_key_frame,*self.collect_client.get_sample_data(sample_data))

                    for instance in self.collect_client.walkers+self.collect_client.vehicles:
                        if self.collect_client.get_visibility(instance) > 0:
                            samples_annotation_token[instance.get_actor().id]  = self.dataset.update_sample_annotation(samples_annotation_token[instance.get_actor().id],sample_token,*self.collect_client.get_sample_annotation(scene_id,instance))
                    
                    for sensor in self.collect_client.sensors:
                        sensor.get_data_list().clear()
        finally:
            self.collect_client.destroy_scene()