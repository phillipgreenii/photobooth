import pygst
pygst.require("0.10")
import gst
import time
import logging

class CameraManager:

    def __init__(self, configuration):
        self.logger = logging.getLogger('camerabin.manager')

        # Set up the gstreamer pipeline
        self.logger.debug('configuring gstreamer pipeline')
        self.camerabin = gst.element_factory_make("camerabin", "cam")
        self.sink = gst.element_factory_make("xvimagesink", "sink") #TODO is sink being used anywhere?
        src = gst.element_factory_make("v4l2src","src")
        src.set_property("device",configuration['camera-device'])
        self.camerabin.set_property("video-source", src)

        self.cameraEnabled = False
        self.current_handler_id = None

        bus = self.camerabin.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self._on_message)
        bus.connect("sync-message::element", self._on_sync_message)

    def setViewFinder(self,viewFinder):
        self.logger.info('setting view finder')
        self._viewFinder = viewFinder

    def _photo_handler(self,c,photo):
        self.logger.debug('handling (%s)' % str(photo))

    def take_photo(self):
        photo_filename = '%012d.jpg' % time.time()  
        self.logger.debug('taking photo')
        if self.current_handler_id is None:
            #TODO this should probably throw an exception
            self.logger.warning('no photo handler set')
            return None
        self.camerabin.set_property("filename", photo_filename)
        self.camerabin.set_property('block-after-capture', True)
        self.camerabin.emit("capture-start")
        self.logger.debug('waiting for picture')
        time.sleep(1)
        self.logger.debug('waited for picture')
        self.camerabin.set_property('block-after-capture', False)
        return photo_filename

    def isCameraEnabled(self):
        return self.cameraEnabled #TODO check status of camerabin instead

    def enableCamera(self):
        self.logger.info('enabling camera')
        self.camerabin.set_state(gst.STATE_PLAYING)
        self.cameraEnabled = True
        self.current_handler_id = self.camerabin.connect("image-done",self._photo_handler)

    def disableCamera(self):
        self.logger.info('disabling camera')
        self.camerabin.set_state(gst.STATE_NULL)
        if self.current_handler_id is not None:
            self.camerabin.disconnect(self.current_handler_id)
            self.current_handler_id = None
        self.cameraEnabled = False

    def _on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.logger.warning('received MESSAGE_EOS')
            self.disableCamera()
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            self.logger.warning('%s' % err,debug)
            self.disableCamera()

    def _on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            if self._viewFinder == None:
                self.logger.error('no viewFinder set')
                raise Exception("no viewFinder set")
            # Assign the viewport
            self.logger.info('assigning viewport')
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(self._viewFinder.window.xid)

