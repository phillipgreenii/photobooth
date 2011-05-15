import logging
import os.path

from reportlab.pdfgen.canvas import Canvas



class PhotoPrinter:
    def __init__(self, printer_manager, printer_name):
        self.logger = logging.getLogger('photo.printer')
        self._printer_manager = printer_manager
        self._printer_name = printer_name
        self._pagesize = self._create_pagesize(2.2, 8.5) #TODO don't hard code page size

    def _create_pagesize(self,width,height):
        import reportlab.lib.pagesizes as ps
        return ps.portrait( (width * ps.inch, height * ps.inch))        

    def printSession(self,session,event_callback=lambda e : None):
        event_callback({'type':'GENERATING_PDF'})
        file_name = self._generatePdf(session)        
        event_callback({'type':'PRINTING'})
        self._printPdf(file_name)
        event_callback({'type':'PRINTED'})

    def _generatePdf(self,session):
        file_name =  os.path.join(session.get_storage_directory(), session.get_name() + '.pdf') #TODO create local image and let sessin move it
        pdf = Canvas(file_name,pagesize=self._pagesize)
        # add metadata
        pdf.setAuthor('photobooth') #TODO add app version to author
        pdf.setSubject('wedding photos')
        pdf.setTitle('pictures for session %s' % session.get_name())
        pdf.setKeywords(('wedding', 'pictures','photobooth'))

        # add pictures
        #TODO add padding
        (total_width, total_height) = self._pagesize
        (image_width, image_height) = (total_width, total_height / len(session.get_photos()))        
        for (i,photo) in enumerate(session.get_photos()):
            pdf.drawInlineImage(photo,0,i * image_height, image_width, image_height, preserveAspectRatio=True, anchor='n')
        
        pdf.showPage()
        pdf.save()
        return file_name

    def _printPdf(self,pdfLocation):
        self._printer_manager.printFile(pdfLocation, self._printer_name)

    def __repr__(self):
        return "%s(printer=%s)" % \
               (self.__class__,self._printer)
