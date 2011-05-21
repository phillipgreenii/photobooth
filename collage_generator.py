import logging
import os.path

from reportlab.pdfgen.canvas import Canvas

class CollageGenerator:
    def __init__(self):
        self.logger = logging.getLogger('collagegenerator')
        self._pagesize = self._create_pagesize(2.2, 8.5) #TODO don't hard code page size

    def _create_pagesize(self,width,height):
        import reportlab.lib.pagesizes as ps
        return ps.portrait( (width * ps.inch, height * ps.inch))        

    def generateCollage(self,session):
        file_name =  'collage.pdf' #TODO image should be created in a temp directory
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

