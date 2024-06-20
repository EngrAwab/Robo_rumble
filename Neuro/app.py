import logging as log
import time
# import GPIO
import depthai as dai
import object_detector_config as nn_config
import robothub as rh
import car_serial as car
# [business logic]
class BusinessLogic:
    def __init__(self, frame_buffer: rh.FrameBuffer, live_view: rh.DepthaiLiveView, mono_right_view: rh.DepthaiLiveView, mono_left_view: rh.DepthaiLiveView):
        self.live_view: rh.DepthaiLiveView = live_view
        self.mono_right_view: rh.DepthaiLiveView = mono_right_view
        self.mono_left_view: rh.DepthaiLiveView = mono_left_view
        self.frame_buffer: rh.FrameBuffer = frame_buffer

        self.last_image_event_upload_seconds = time.time()
        self.last_video_event_upload_seconds = time.time()

    def process_pipeline_outputs(self, h264_frame: dai.ImgFrame, mjpeg_frame: dai.ImgFrame, object_detections: dai.ImgDetections, mono_right_frame: dai.ImgFrame, mono_left_frame: dai.ImgFrame):
        self.frame_buffer.add_frame(h264_frame)  # Make sure to store every h264 frame
        for detection in object_detections.detections:
            bbox = (detection.xmin, detection.ymin, detection.xmax, detection.ymax)
            self.live_view.add_rectangle(bbox, label=nn_config.labels[detection.label])
        
        self.live_view.publish(h264_frame=h264_frame.getCvFrame())
        self.mono_right_view.publish(h264_frame=mono_right_frame.getCvFrame())
        # self.mono_left_view.publish(h264_frame=mono_left_frame.getCvFrame())


# [/business logic]

# [application]
class Application(rh.BaseDepthAIApplication):

    def __init__(self):
        super().__init__()
        rh.COMMUNICATOR.on_frontend(
            notification=self.on_fe_notification,
            request=self.on_fe_request,
        )
        
        self.live_view = rh.DepthaiLiveView(name="color_stream", unique_key="color_stream", width=1920, height=1080)
        self.mono_right_view = rh.DepthaiLiveView(name="mono_right_stream", unique_key="mono_right_stream", width=1280, height=720)
        self.mono_left_view = rh.DepthaiLiveView(name="mono_left_stream", unique_key="mono_left_stream", width=1280, height=720)
        
        frame_buffer = rh.FrameBuffer(maxlen=rh.CONFIGURATION["fps"] * 60 * 2)  # buffer last 2 minutes
        self.business_logic = BusinessLogic(frame_buffer=frame_buffer, live_view=self.live_view, mono_right_view=self.mono_right_view, mono_left_view=self.mono_left_view)
        self.yolo_num_classes = 1  # Default number of classes
        self.yolo_class_labels = ["Fire"]  
        self.path='/app/tse.blob'
        with open ("/app/object_detector_config.py", 'w') as f :
            f.write(f'labels = {self.yolo_class_labels}')
    def update_yolo_model(self, model_name):
        if model_name == 'Cone':
            num_classes = 2  
            class_labels = ["Cone"]  
            path="/app/tse.blob"
        elif model_name == 'Fall':
            num_classes = 1  
            class_labels = ["Fall"] 
            path="/app/fall.blob"
        else :
            num_classes = 1  
            class_labels = ["Fire"] 
            path="/app/tse.blob"
        with open ("/app/object_detector_config.py", 'w') as f :
            f.write(f'labels = {class_labels}')
        return num_classes, class_labels ,path
    def on_fe_notification(self, session_id, unique_key, payload):
        log.info(f"{payload = } {unique_key=}")

        if unique_key == 'RGB':
            log.info("Saving picture (RGB)")
            self.save_rgb_picture()  # Assuming you have this function
        elif unique_key == 'model_change':
            selected_model = payload.get('model')
            self.yolo_num_classes, self.yolo_class_labels, self.path = self.update_yolo_model(selected_model)
            log.info(f"Model selected: {selected_model}")
            log.info("Restarting pipeline...")
            self.restart_device()
        elif unique_key == 'car_control':
            action = payload.get('action')
            log.info(f"Car control action: {action}")
            if action == "up":
                car.move_motor_forward()
            elif action == "down":
                car.move_motor_backward()
            elif action == "left":
                car.rotate_motor_left()
            elif action == "right":
                car.rotate_motor_right()
        elif unique_key == 'gimbal_control':
            action = payload.get('action')
            log.info(f"Gimbal control action: {action}")
            if action == "up":
                car.cam_up()
            elif action == "down":
                car.cam_bottom()
            elif action == "left":
                car.cam_left()
            elif action == "right":
                car.cam_right()
        else:
            log.warning(f"Unhandled unique_key: {unique_key}")



    def on_fe_request(self, session_id, unique_key, payload):
        log.info(f"FE request: {unique_key = }")

# [setup pipeline]
    def setup_pipeline(self) -> dai.Pipeline:
        """Define the pipeline using DepthAI."""

        log.info(f"App config: {rh.CONFIGURATION}")
        pipeline = dai.Pipeline()
        rgb_sensor = create_rgb_sensor(pipeline=pipeline, preview_resolution=(640, 352))
        rgb_h264_encoder = create_h264_encoder(node_input=rgb_sensor.video, pipeline=pipeline)
        rgb_mjpeg_encoder = create_mjpeg_encoder(node_input=rgb_sensor.video, pipeline=pipeline)
        object_detection_nn = create_yolov7tiny_coco_nn(node_input=rgb_sensor.preview, pipeline=pipeline,
                                                       num_classes=self.yolo_num_classes,
                                                       blob_path=self.path)
        create_output(pipeline=pipeline, node_input=rgb_h264_encoder.bitstream, stream_name="h264_frames")
        create_output(pipeline=pipeline, node_input=rgb_mjpeg_encoder.bitstream, stream_name="mjpeg_frames")
        create_output(pipeline=pipeline, node_input=object_detection_nn.out, stream_name="object_detections")

        # Adding mono cameras
        mono_right = create_mono_camera(pipeline=pipeline, camera_id="right")
        mono_left = create_mono_camera(pipeline=pipeline, camera_id="left")

        mono_right_h264_encoder = create_h264_encoder(node_input=mono_right.out, pipeline=pipeline)
        mono_left_h264_encoder = create_h264_encoder(node_input=mono_left.out, pipeline=pipeline)

        create_output(pipeline=pipeline, node_input=mono_right_h264_encoder.bitstream, stream_name="mono_right_h264")
        create_output(pipeline=pipeline, node_input=mono_left_h264_encoder.bitstream, stream_name="mono_left_h264")

        return pipeline

# [/setup pipeline]

# [main loop]
    def manage_device(self, device: dai.Device):
        log.info(f"{device.getMxId()} creating output queues...")
        h264_frames_queue = device.getOutputQueue(name="h264_frames", maxSize=10, blocking=True)
        mjpeg_frames_queue = device.getOutputQueue(name="mjpeg_frames", maxSize=10, blocking=True)
        object_detections_queue = device.getOutputQueue(name="object_detections", maxSize=10, blocking=True)

        # Mono camera H264 queues
        mono_right_h264_queue = device.getOutputQueue(name="mono_right_h264", maxSize=10, blocking=True)
        mono_left_h264_queue = device.getOutputQueue(name="mono_left_h264", maxSize=10, blocking=True)

        log.info(f"{device.getMxId()} Application started")
        while rh.app_is_running() and self.device_is_running:
            h264_frame = h264_frames_queue.get()
            mjpeg_frame = mjpeg_frames_queue.get()
            object_detections = object_detections_queue.get()
            mono_right_frame = mono_right_h264_queue.get()
            mono_left_frame = mono_left_h264_queue.get()
            self.business_logic.process_pipeline_outputs(h264_frame=h264_frame, mjpeg_frame=mjpeg_frame, object_detections=object_detections, mono_right_frame=mono_right_frame, mono_left_frame=mono_left_frame)
            time.sleep(0.001)

    # [/main loop]

    # [config change listener]
    def on_configuration_changed(self, configuration_changes: dict) -> None:
        log.info(f"CONFIGURATION CHANGES: {configuration_changes}")
        if "fps" in configuration_changes:
            log.info(f"FPS change needs a new pipeline. Restarting OAK device...")
            self.restart_device()

    # [/config change listener]
    # [/application]


# [pipeline]
# [rgb sensor]
def create_rgb_sensor(pipeline: dai.Pipeline,
                      fps: int = 30,
                      resolution: dai.ColorCameraProperties.SensorResolution = dai.ColorCameraProperties.SensorResolution.THE_1080_P,
                      preview_resolution: tuple = (1280, 720),
                      ) -> dai.node.ColorCamera:
    node = pipeline.createColorCamera()
    node.setBoardSocket(dai.CameraBoardSocket.RGB)
    node.setInterleaved(False)
    node.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
    node.setPreviewNumFramesPool(4)
    node.setPreviewSize(*preview_resolution)
    node.setVideoSize(1920, 1080)
    node.setResolution(resolution)
    node.setFps(fps)
    return node
# [/rgb sensor]

# [mono camera]
def create_mono_camera(pipeline: dai.Pipeline, camera_id: str, fps: int = 30) -> dai.node.MonoCamera:
    node = pipeline.createMonoCamera()
    if camera_id == "right":
        node.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    elif camera_id == "left":
        node.setBoardSocket(dai.CameraBoardSocket.LEFT)
    node.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    node.setFps(fps)
    return node
# [/mono camera]

# [encoders]
# [h encoder]
def create_h264_encoder(node_input: dai.Node.Output, pipeline: dai.Pipeline, fps: int = 30):
    rh_encoder = pipeline.createVideoEncoder()
    rh_encoder_profile = dai.VideoEncoderProperties.Profile.H264_MAIN
    rh_encoder.setDefaultProfilePreset(fps, rh_encoder_profile)
    rh_encoder.input.setQueueSize(2)
    rh_encoder.input.setBlocking(False)
    rh_encoder.setKeyframeFrequency(fps)
    rh_encoder.setRateControlMode(dai.VideoEncoderProperties.RateControlMode.CBR)
    rh_encoder.setNumFramesPool(3)
    node_input.link(rh_encoder.input)
    return rh_encoder
# [/h encoder]

# [mjpeg encoder]
def create_mjpeg_encoder(node_input: dai.Node.Output, pipeline: dai.Pipeline, fps: int = 30, quality: int = 100):
    encoder = pipeline.createVideoEncoder()
    encoder_profile = dai.VideoEncoderProperties.Profile.MJPEG
    encoder.setDefaultProfilePreset(fps, encoder_profile)
    encoder.setQuality(quality)
    node_input.link(encoder.input)
    return encoder
# [/mjpeg encoder]
# [/encoders]

# [yolo nn]
def create_yolov7tiny_coco_nn(node_input: dai.Node.Output, pipeline: dai.Pipeline,num_classes=1, blob_path=None) -> dai.node.YoloDetectionNetwork:
    model = "yolov7tiny_coco_640x352"
    log.info(f'THe model is {blob_path}')
    
    node = pipeline.createYoloDetectionNetwork()
    node.setConfidenceThreshold(0.4)
    node.setNumClasses(num_classes)
    node.setCoordinateSize(4)
    node.setAnchors([
                10.0,
                13.0,
                16.0,
                30.0,
                33.0,
                23.0,
                30.0,
                61.0,
                62.0,
                45.0,
                59.0,
                119.0,
                116.0,
                90.0,
                156.0,
                198.0,
                373.0,
                326.0
            ])
    node.setAnchorMasks({
                "side80": [
                    0,
                    1,
                    2
                ],
                "side40": [
                    3,
                    4,
                    5
                ],
                "side20": [
                    6,
                    7,
                    8
                ]
            })
    node.setIouThreshold(0.5)
    node.setBlobPath(blob_path)
    node.setNumInferenceThreads(2)
    node_input.link(node.input)
    node.input.setBlocking(False)
    return node
# [/yolo nn]

# [xlink out]
def create_output(pipeline, node_input: dai.Node.Output, stream_name: str):
    xout = pipeline.createXLinkOut()
    xout.setStreamName(stream_name)
    node_input.link(xout.input)
# [/xlink out]
# [/pipeline]

# [local development]
if __name__ == "__main__":
    app = Application()
    app.run()
# [/local development]

