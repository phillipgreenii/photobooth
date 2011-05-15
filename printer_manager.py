import logging
import subprocess
import re

class PrinterManager:
    def __init__(self):
        self.logger = logging.getLogger('printer.manager')
        self.refresh()

    def get_printer_names(self):
        return self._printer_names

    def get_default_printer_name(self):
        return self._default_printer_name

    def printFile(self,file,printer_name=None):
        actual_printer_name = printer_name if printer_name is not None else self._default_printer_name 
        self.logger.debug('printing %s to %s' % (file, actual_printer_name))
        return 0 == subprocess.call(('lpr','-P',actual_printer_name,file))

    def refresh(self):
        self._printer_names = self._retrieve_printer_names()
        self._default_printer_name = self._retrieve_default_printer_name()

    def _retrieve_printer_names(self):
        p = subprocess.Popen(('lpstat','-a'),stdout=subprocess.PIPE)
        r = re.compile('(.*) accepting requests')
        printer_names = []
        for line in p.stdout:
            m = r.match(line)
            if m :
                printer_names.append(m.group(1))
        return printer_names

    def _retrieve_default_printer_name(self):
        p = subprocess.Popen(('lpstat','-d'),stdout=subprocess.PIPE)
        r = re.compile('system default destination: (.*)$')
        line = p.stdout.read()
        m = r.match(line)
        if m:
            return m.group(1)
        else:
            raise exception("unparsible result: %s" % line)
