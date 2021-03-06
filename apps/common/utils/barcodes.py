from django.conf import settings

from reportlab.lib.units import mm
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing, String

class BarcodeFromString(Drawing):
    def __init__(self, text, *args, **kwargs):
        barcode = createBarcodeDrawing(
            'Code128', value=text, barHeight=10*mm, humanReadable=True)
        Drawing.__init__(
            self, barcode.width,barcode.height,*args,**kwargs)
        self.add(barcode, text)
        # using default storage helps mantaining consistent environments
        from django.core.files.storage import default_storage as storage
        # ContentFile is a string array, represented as file
        from django.core.files.base import ContentFile
        # pushing the barcode into the content file
        barcode_png = ContentFile(self.asString('png'))
        # naming the content file
        name = '%s/%s.png' %('coupons', text)
        # saving the barcode file
        storage.save(name, barcode_png)

