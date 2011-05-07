import pygtk, gtk, gobject
pygtk.require('2.0')

class PhotoboothGUI:

	def __init__(self, controller):
		self.controller = controller
		
		# create window
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Webcam-Viewer")
		window.set_default_size(500, 400)
		window.connect("destroy", self.exit, "WM destroy")

		# vertical container to hold everything
		vbox = gtk.VBox()
		window.add(vbox)
	
		# create tools menu
		tools_menu_item = gtk.MenuItem("Tools")


		tools_menu = gtk.Menu()
		tools_menu_item_camera_toggle = gtk.MenuItem('Toggle Camera')
		tools_menu_item_camera_toggle.connect("activate", self.start_stop, 'toggle-camera')
		tools_menu_item_camera_toggle.show()
		tools_menu.append(tools_menu_item_camera_toggle)

		tools_menu_item.set_submenu(tools_menu)
		tools_menu_item.show()
		
		menu_bar = gtk.MenuBar()
		menu_bar.append(tools_menu_item)
		menu_bar.show()

		#FIXME needs packed better
		#FIXME doesn't always render
		vbox.pack_start(menu_bar)#, False, False,2 ) 
		
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
		hbox.add(gtk.Label())
		window.show_all()

		# link to controller
		self.controller.setViewFinder(self.movie_window)


	def start_stop(self, w, string):
		if string == 'toggle-camera':
			if self.controller.isCameraEnabled():
				self.takePictureButton.set_sensitive(False)
				self.controller.disableCamera()
			else:
				self.controller.enableCamera()
				self.takePictureButton.set_sensitive(True)

	def take_picture(self,w):
		self.takePictureButton.set_sensitive(False)
		self.controller.takePictures(lambda : self.takePictureButton.set_sensitive(True))		

	def exit(self, widget, data=None):
		self.controller.disableCamera()
		gtk.main_quit()

	def run(self):
		gtk.gdk.threads_init()
		gtk.main()

