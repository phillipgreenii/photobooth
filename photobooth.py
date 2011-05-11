#!/usr/bin/env python

from optparse import OptionParser
import logging
import sys
import photobooth_controller
import photobooth_gui


def parse_configuration(arguments):
	parser = OptionParser(usage='usage: %prog [options]')
	parser.add_option("-c", "--camera",
			  dest="camera-device",
			  default='/dev/video0',
			  help="print debug",
			  metavar="CAMERA-PATH")
	parser.add_option("-t", "--time-between-photos",
			  type='int',
			  dest="time-delay", default=3,
			  help="the time between each photo",
			  metavar="SECONDS")
	parser.add_option("-n", "--number-of-photos",
			  type='int',
			  dest="number-of-photos", default=4,
			  help="the number of photos per session",
			  metavar="NUMBER")
	parser.add_option("-o", "--output-directory",
			  dest="output-directory",
			  default="./sessions/",
			  help="output directory to store photo sessions",
			  metavar="DIRECTORY")
	parser.add_option("-d", "--debug",
			  dest="logging-level",
			  action="store_const", const=logging.DEBUG,
			  default=logging.INFO,
			  help="print debug")


	(options, args) = parser.parse_args()

	if len(args) > 0:
		parser.error("arguments aren't supported")

	return vars(options)

def main(arguments):
	configuration = parse_configuration(arguments)

	level = configuration['logging-level']

	logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',level=level)

	logger = logging.getLogger('photobooth')
	logger.debug('configuration: %s' % (configuration))


	logger.info('starting photobooth')


	logger.debug('creating controller')
	controller = photobooth_controller.PhotoboothController(configuration)

	logger.debug('creating gui')
	gui = photobooth_gui.PhotoboothGUI(controller)

	logger.debug('starting gui')
	gui.run()

	logger.info('shutting down photobooth')
	logging.shutdown()


main(sys.argv[1:])
