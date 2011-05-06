import pygtk, gtk, gobject

class PhotoboothGUI:

	def __init__(self, controller):
		self.controller = controller
		
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Webcam-Viewer")
		window.set_default_size(500, 400)
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		hbox = gtk.HBox()
		vbox.pack_start(hbox, False)
		hbox.set_border_width(10)
		hbox.pack_start(gtk.Label())
		self.takePictureButton = gtk.Button("Take Picture")
		self.takePictureButton.set_sensitive(False)
		self.takePictureButton.connect("clicked",self.take_picture)
		hbox.pack_start(self.takePictureButton, False)
		self.button = gtk.Button("Start")
		self.button.connect("clicked", self.start_stop)
		hbox.pack_start(self.button, False)
		self.button2 = gtk.Button("Quit")
		self.button2.connect("clicked", self.exit)
		hbox.pack_start(self.button2, False)
		hbox.add(gtk.Label())
		window.show_all()

		# link to controller
		self.controller.setViewFinder(self.movie_window)


	def start_stop(self, w):
		if self.button.get_label() == "Start":
			self.button.set_label("Stop")			
			self.controller.enableCamera()
			self.takePictureButton.set_sensitive(True)
		else:
			self.takePictureButton.set_sensitive(False)
			self.controller.disableCamera()
			self.button.set_label("Start")

	def take_picture(self,w):
		self.takePictureButton.set_sensitive(False)
		self.controller.takePictures(lambda : self.takePictureButton.set_sensitive(True))		

	def exit(self, widget, data=None):
		self.controller.disableCamera()
		gtk.main_quit()

	def run(self):
		gtk.gdk.threads_init()
		gtk.main()

