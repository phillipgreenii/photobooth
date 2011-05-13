import logging
import os.path

from reportlab.pdfgen.canvas import Canvas



class PhotoPrinter:
    def __init__(self):
        self.logger = logging.getLogger('photo.printer')
        self._printer = ''
        self._pagesize = self._create_pagesize(2.2, 8.5)

    def _create_pagesize(self,width,height):
        import reportlab.lib.pagesizes as ps
        return ps.portrait( (width * ps.inch, height * ps.inch))        

    def printSession(self,session,event_callback=lambda e : None):
        event_callback({'type':'GENERATING_PDF'})
        self._generatePdf(session)        
        event_callback({'type':'PRINTING'})
        self._printPdf(session)
        event_callback({'type':'PRINTED'})

    def _generatePdf(self,session):
        file_name =  os.path.join(session.get_storage_directory(), session.get_name() + '.pdf') #TODO should create path or let session handle it?
        pdf = Canvas(file_name,pagesize=self._pagesize)
        pdf.setAuthor('photobooth') #TODO add app version to author
        pdf.setSubject('wedding photos')
        pdf.setTitle('pictures for session %s' % session.get_name())
        pdf.setKeywords(('wedding', 'pictures','photobooth'))
        
        pdf.showPage()
        pdf.save()

    def _printPdf(self,pdfLocation):
        pass

    def __repr__(self):
        return "%s(printer=%s)" % \
               (self.__class__,self._printer)
