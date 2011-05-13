import logging

class PhotoPrinter:
    def __init__(self):
        self.logger = logging.getLogger('photo.printer')
        self._printer = ''

    def printSession(self,session,event_callback=lambda e : None):
        event_callback({'type':'PRINTED'})
        pass

    def __repr__(self):
        return "%s(printer=%s)" % \
               (self.__class__,self._printer)
