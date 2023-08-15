#pip3 install PyMuPDF
import fitz 

def Pdf2Png(pdf):
    doc = fitz.open(pdf)  # open document
    for i, page in enumerate(doc):
        pix = page.get_pixmap()  # render page to an image
        pix.save(f"page_{i}.png")
        
Pdf2Png(r"path")