import pyhik.hikvision as hikvision
import logging


class HikCamObject(object):
    def __init__(self, url, port, user, passw):
        self.cam = hikvision.HikCamera(url, port, user, passw)

        self._name = self.cam.get_name
        self.motion = self.cam.current_motion_detection_state

        self.cam.start_stream()

        self._event_states = self.cam.current_event_states
        self._id = self.cam.get_id

        logger = logging.getLogger(__name__)
        logger.debug('NAME: {}'.format(self._name))
        logger.debug('ID: {}'.format(self._id))
        logger.debug('{}'.format(self._event_states))
        logger.debug('Motion Dectect State: {}'.format(self.motion))

    @property
    def sensors(self):
        return self.cam.current_event_states

    def get_attributes(self, sensor, channel):
        return self.cam.fetch_attributes(sensor, channel)

    def stop_hik(self):
        self.cam.disconnect()

    def flip_motion(self, value):
        if value:
            self.cam.enable_motion_detection()
        else:
            self.cam.disable_motion_detection()


class HikSensor(object):
    def __init__(self, sensor, channel, cam, update_callback):
        self._cam = cam
        self._name = "{} {} {}".format(self._cam.cam.name, sensor, channel)
        self._id = "{}.{}.{}".format(self._cam.cam.cam_id, sensor, channel)
        self._sensor = sensor
        self._channel = channel

        self._cam.cam.add_update_callback(update_callback, self._id)

    def _sensor_state(self):
        return self._cam.get_attributes(self._sensor, self._channel)[0]

    def _sensor_last_update(self):
        return self._cam.get_attributes(self._sensor, self._channel)[3]

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return '{}.{}'.format(self.__class__, self._id)

    @property
    def is_on(self):
        return self._sensor_state()
