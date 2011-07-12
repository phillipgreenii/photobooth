import pygtk, gtk, gobject
pygtk.require('2.0')
import logging
import pango

class PhotoboothGUI:

    def __init__(self, controller):
        self.logger = logging.getLogger('photobooth.gui')

        self.controller = controller

        self.in_progress = False

        # create window
        self.logger.debug('creating window')
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Photobooth")
        window.set_default_size(800, 600)
        window.connect("destroy", self.exit, "Photobooth destroy")

        # add key listener
        window.connect('key_press_event', self._on_key_press_event)

        # vertical container to hold everything
        vbox = gtk.VBox()
        window.add(vbox)

        # create tools menu
        self.logger.debug('creating menu')
        tools_menu_item = gtk.MenuItem("_Tools")

        tools_menu = gtk.Menu()
        tools_menu_item_camera_toggle = gtk.MenuItem('_Toggle Camera')
        tools_menu_item_camera_toggle.connect("activate", self.start_stop, 'toggle-camera')
        tools_menu_item_camera_toggle.show()
        tools_menu.append(tools_menu_item_camera_toggle)

        tools_menu_item.set_submenu(tools_menu)
        tools_menu_item.show()

        menu_bar = gtk.MenuBar()
        menu_bar.append(tools_menu_item)
        menu_bar.show()

        #FIXME doesn't always render
        vbox.pack_start(menu_bar, False, False,2 )

        self.logger.debug('creating drawing area')
        self.movie_window = gtk.DrawingArea()
        vbox.add(self.movie_window)

        hbox = gtk.HBox()
        vbox.pack_start(hbox, False)
        hbox.set_border_width(10)
        hbox.pack_start(gtk.Label())

        # create take picture button
        self.logger.debug('creating takePictureButton')
        self.takePictureButton = gtk.Button("Take Picture")
        self.takePictureButton.set_sensitive(False)
        self.takePictureButton.connect("clicked",self.take_picture)
        buttonText = self.takePictureButton.get_children()[0]
        buttonFont = pango.FontDescription("Georgia 32")
        buttonText.modify_font(buttonFont)
        hbox.pack_start(self.takePictureButton, False)

        hbox.add(gtk.Label())

        inprogressBox = gtk.HBox()
        vbox.pack_start(inprogressBox,False)
        inprogressBox.set_border_width(10)
        inprogressBox.pack_start(gtk.Label())
        self.countDownLabel = gtk.Label()
        countDownLabelFont = pango.FontDescription("Georgia 28")
        self.countDownLabel.modify_font(countDownLabelFont)
        inprogressBox.add(self.countDownLabel)
        inprogressBox.pack_start(gtk.Label())

        window.show_all()

        # link to controller
        self.controller.setViewFinder(self.movie_window)


    def start_stop(self, w, string):
        if string == 'toggle-camera':
            if self.controller.isCameraEnabled():
                self.logger.info('disabling camera')
                self.takePictureButton.set_sensitive(False)
                self.controller.disableCamera()
            else:
                self.logger.info('enabling camera')
                self.controller.enableCamera()
                self.takePictureButton.set_sensitive(True)

    def take_picture(self,w):
        if not self.in_progress and self.controller.isCameraEnabled():
            self.in_progress = True
            self.logger.info('take pictures')
            self.controller.takePictures(self._picture_event_handler)
            self.logger.debug('finished taking pictures')

    def _on_key_press_event(self,widget,event):
         keyname = gtk.gdk.keyval_name(event.keyval)
         self.logger.debug('keyname: %s' % keyname)
         if keyname == 'percent' and event.state & gtk.gdk.CONTROL_MASK and event.state & gtk.gdk.MOD1_MASK and event.state & gtk.gdk.SHIFT_MASK:
             self.take_picture(widget)

    def _picture_event_handler(self,event):
        self.logger.debug('handling %s' % event)
        #TODO don't hard code event types or fields
        if event['type'] == 'START':
            self.takePictureButton.set_sensitive(False)
        elif event['type'] == 'TAKE_PICTURE':
            self.countDownLabel.set_text('Taking Picture %d/%d' % (event['current_picture'], event['total_pictures']))
        elif event['type'] == 'TOOK_PICTURE':
            self.countDownLabel.set_text('Took Picture %d/%d' % (event['current_picture'], event['total_pictures']))
        elif event['type'] == 'COUNT_DOWN_UPDATE':
            self.countDownLabel.set_text("%d ..." % event['time_until_picture'])
        elif event['type'] == 'DONE':
            self.countDownLabel.set_text('')
            self.takePictureButton.set_sensitive(True)
            self.in_progress = False
        elif event['type'] == 'ERROR':
            self.in_progress = False
        elif event['type'] == 'PRINTED':
            self.countDownLabel.set_text('Printed Pictures')
        self.flushUpdates()

    def flushUpdates(self):
        while gtk.events_pending():
            gtk.main_iteration()

    def exit(self, widget, data=None):
        self.logger.debug('exiting gui')
        self.controller.disableCamera()
        gtk.main_quit()

    def run(self):
        self.logger.debug('running gui')
        gtk.gdk.threads_init()
        gtk.main()

