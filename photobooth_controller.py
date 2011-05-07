import pygst
pygst.require("0.10")
import gst
import time
import math
import photo_session
import photo_taker
import logging

class PhotoboothController:

	def __init__(self, configuration):
		self.logger = logging.getLogger('photobooth.controller')
		
		# Set up the gstreamer pipeline
		self.logger.debug('configuring gstreamer pipeline')
		self.camerabin = gst.element_factory_make("camerabin", "cam")
		self.sink = gst.element_factory_make("xvimagesink", "sink")
		src = gst.element_factory_make("v4l2src","src")
		src.set_property("device","/dev/video0")
		self.camerabin.set_property("video-source", src)

		self.cameraEnabled = False
		
		bus = self.camerabin.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self._on_message)
		bus.connect("sync-message::element", self._on_sync_message)

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
		session = photo_session.PhotoSession('./tmp',name) #TODO don't hardcode path
		self.logger.info('Taking pictures for %s' % session)
		photoTaker = photo_taker.PhotoTaker(self.camerabin, session, 4, event_callback)
		photoTaker.start()

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

