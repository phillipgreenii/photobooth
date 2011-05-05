import pygst
pygst.require("0.10")
import gst
import time
import math
import photo_session

class PhotoboothController:

	def __init__(self, configuration):		
		# Set up the gstreamer pipeline
		self.camerabin = gst.element_factory_make("camerabin", "cam")
		self.sink = gst.element_factory_make("xvimagesink", "sink")
		src = gst.element_factory_make("v4l2src","src")
		src.set_property("device","/dev/video0")
		self.camerabin.set_property("video-source", src)
		
		bus = self.camerabin.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self._on_message)
		bus.connect("sync-message::element", self._on_sync_message)

	def setViewFinder(self,viewFinder):
		self._viewFinder = viewFinder

	def enableCamera(self):
		self.camerabin.set_state(gst.STATE_PLAYING)
		None

	def disableCamera(self):
		self.camerabin.set_state(gst.STATE_NULL)
		None

	def takePictures(self):
		name = '%012d' % math.floor(time.time())		
		session = photo_session.PhotoSession('./tmp',name) #TODO don't hardcode path
		print "Taking a Picture"
		self.camerabin.connect("image-done",lambda c, filename: session.addPhoto(filename))
		picture_filename = '%012d' % math.floor(time.time()) + ".jpg"
		self.camerabin.set_property("filename", picture_filename)
		self.camerabin.emit("capture-start")
		self.camerabin.connect("image-done",lambda c, filename: None) #FIXME error should occur

	def _on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.disableCamera()
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.disableCamera()

	def _on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			if self._viewFinder == None:
				raise Exception("no viewFinder set")
			# Assign the viewport
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			imagesink.set_xwindow_id(self._viewFinder.window.xid)

