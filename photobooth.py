#!/usr/bin/env python

from optparse import OptionParser
import logging
import sys
import printer_manager
import camera_manager
import photobooth_controller
import photobooth_gui


def parse_configuration(arguments, defaults):
	parser = OptionParser(usage='usage: %prog [options]')
	parser.add_option("-c", "--camera",
			  dest="camera-device",
			  default=defaults['camera-device'],
			  help="print debug",
			  metavar="CAMERA-PATH")
	parser.add_option("-t", "--time-between-photos",
			  type='int',
			  dest="time-delay",
			  default=defaults['time-delay'],
			  help="the time between each photo",
			  metavar="SECONDS")
	parser.add_option("-n", "--number-of-photos",
			  type='int',
			  dest="number-of-photos",
			  default=defaults['number-of-photos'],
			  help="the number of photos per session",
			  metavar="NUMBER")
	parser.add_option("-o", "--output-directory",
			  dest="output-directory",
			  default=defaults['output-directory'],
			  help="output directory to store photo sessions",
			  metavar="DIRECTORY")
	parser.add_option("-p", "--printer",
			  dest="printer",
			  default=defaults['printer'],
			  help="the printer to use when printing",
			  metavar="PRINTER")
	parser.add_option("-d", "--debug",
			  dest="logging-level",
			  action="store_const", const=logging.DEBUG,
			  default=defaults['logging-level'],
			  help="print debug")


	(options, args) = parser.parse_args()

	if len(args) > 0:
		parser.error("arguments aren't supported")

	return vars(options)

def main(arguments):
	pm = printer_manager.PrinterManager()

	default_configuration = {
		'camera-device': '/dev/video0',
		'time-delay': 3,
		'number-of-photos' : 4,
		'output-directory' : './sessions/',
		'printer' : pm.get_default_printer_name(),
		'logging-level' : logging.INFO}
	
	configuration = parse_configuration(arguments, default_configuration)

	level = configuration['logging-level']

	logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',level=level)

	logger = logging.getLogger('photobooth')
	logger.debug('configuration: %s' % (configuration))


	logger.info('starting photobooth')

        logger.debug('creating camera manager')
        cm = camera_manager.CameraManager(configuration)

	logger.debug('creating controller')
	controller = photobooth_controller.PhotoboothController(configuration,pm,cm)

	logger.debug('creating gui')
	gui = photobooth_gui.PhotoboothGUI(controller)

	logger.debug('starting gui')
	gui.run()

	logger.info('shutting down photobooth')
	logging.shutdown()


main(sys.argv[1:])
