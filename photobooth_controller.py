import pygst
pygst.require("0.10")
import gst
import time
import math
import photo_session
import photo_taker
import photo_printer
import printer_manager
import logging

class PhotoboothController:

	def __init__(self, configuration):
		self.logger = logging.getLogger('photobooth.controller')

		self._apply_configuration(configuration)
		self.printerManager = printer_manager.PrinterManager()
		self.photoPrinter = photo_printer.PhotoPrinter(self.printerManager)

		# Set up the gstreamer pipeline
		self.logger.debug('configuring gstreamer pipeline')
		self.camerabin = gst.element_factory_make("camerabin", "cam")
		self.sink = gst.element_factory_make("xvimagesink", "sink") #TODO is sink being used anywhere?
		src = gst.element_factory_make("v4l2src","src")
		src.set_property("device",self.camera_path)
		self.camerabin.set_property("video-source", src)

		self.cameraEnabled = False

		bus = self.camerabin.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self._on_message)
		bus.connect("sync-message::element", self._on_sync_message)

	def _apply_configuration(self,configuration):
		def check_for_parameter(param):
			if not param in configuration:
				raise exception('required configuration paramater (%s) not found' % param)
			value = configuration[param]
			self.logger.debug('configuration: %s=%s' % (param, str(value)))
			return value
			
		self.camera_path = check_for_parameter('camera-device')
		self._session_root_path = check_for_parameter('output-directory')
		self._number_of_photos = check_for_parameter('number-of-photos')
		self._time_delay = check_for_parameter('time-delay')


	def setViewFinder(self,viewFinder):
		self.logger.info('setting view finder')
		self._viewFinder = viewFinder

	def isCameraEnabled(self):
		return self.cameraEnabled #TODO check status of camerabin instead

	def enableCamera(self):
		self.logger.info('enabling camera')
		self.camerabin.set_state(gst.STATE_PLAYING)
		self.cameraEnabled = True

	def disableCamera(self):
		self.logger.info('disabling camera')
		self.camerabin.set_state(gst.STATE_NULL)
		self.cameraEnabled = False

	def takePictures(self,event_callback = lambda e : None ):
		name = '%012d' % math.floor(time.time())
		self.logger.debug('creating session')
		session = photo_session.PhotoSession(self._session_root_path,name, self._number_of_photos)
		self.logger.info('Taking pictures for %s' % session)
		photoTaker = photo_taker.PhotoTaker(self.camerabin, session, self._time_delay, event_callback)#TODO do I need a new photoTake each time?
		photoTaker.start()
		self.logger.info('Printing pictures')
		self.photoPrinter.printSession(session,event_callback)

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

