#!/usr/bin/env python

import photobooth_controller
import photobooth_gui

def main():
	configuration = {}
	controller = photobooth_controller.PhotoboothController(configuration)
	gui = photobooth_gui.PhotoboothGUI(controller)
	gui.run()

main()
