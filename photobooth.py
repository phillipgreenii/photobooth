#!/usr/bin/env python

import photobooth_controller
import photobooth_gui
import logging

def main():
	logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',level=logging.DEBUG)

	logger = logging.getLogger('photobooth')

	logger.info('starting photobooth')

	logger.debug('creating configuration')
	configuration = {}

	logger.debug('creating controller')
	controller = photobooth_controller.PhotoboothController(configuration)

	logger.debug('creating gui')
	gui = photobooth_gui.PhotoboothGUI(controller)

	logger.debug('starting gui')
	gui.run()

	logger.info('shutting down photobooth')
	logging.shutdown()


main()
