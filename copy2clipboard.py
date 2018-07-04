from io import BytesIO
from time import sleep
import matplotlib as mpl
from PIL import Image
import win32clipboard
#def copy2clipboard(fig=None):
#
#    if not fig:
#        fig = mpl.pyplot.gcf()
#    output = BytesIO()
#    filepath = BytesIO()
#    fig.savefig(filepath)
#    filepath.seek(0)
#    image = Image.open(filepath)
#    image.convert("RGB").save(output, "BMP")
#    data = output.getvalue()[14:]
#    output.close()
#    try:
#        win32clipboard.OpenClipboard()
#        win32clipboard.EmptyClipboard()
#        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
#        win32clipboard.CloseClipboard()
#        return
#    except:
#        pass
    
    
def copy2clipboard(fig=None):
    '''
    copy a matplotlib figure to clipboard as BMP on windows
    http://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
    '''
    for i in range(3):
        if not fig:
            fig = mpl.pyplot.gcf()
        
        output = BytesIO()
        # fig.savefig(output, format='bmp') # bmp not supported
        buf = fig.canvas.buffer_rgba()
        w = int(fig.get_figwidth() * fig.dpi)
        h = int(fig.get_figheight() * fig.dpi)
        im = Image.frombuffer('RGBA', (w,h), buf,"raw", 'RGBA', 0, 1)
        im.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:] # The file header off-set of BMP is 14 bytes
        output.close()
    
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            return
        except:
            sleep(0.2)
#if __name__ == '__main__':
#    
#    from pylab import *
#    fig = figure()
#    ax = subplot(111)
#    ax.plot(range(10))
#    draw()
#
#    copy2clipboard(fig)
