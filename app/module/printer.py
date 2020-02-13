import logging
import time

import win32api
import win32con
import win32print
import win32ui
from PIL import Image, ImageWin

from win32con import SW_SHOWNORMAL

"""
http://timgolden.me.uk/pywin32-docs/contents.html
http://timgolden.me.uk/pywin32-docs/win32print.html
"""


def get_label_size(key):
    """ Size in real world """
    size = {
        # Width, Height
        'SF_PRINTER' : (720, 1500),
        'ICB_PRINTER': (720, 1500),
        'IN_PRINTER' : (200, 100),
        'OUT_PRINTER': (700, 1000),
    }

    return size[key]


def get_printer_list():
    resultList = []
    pList = win32print.EnumPrinters(2)

    for p in pList:
        # print(p)
        resultList.append({
            'id'       : p[0],
            'name'     : p[2],
            'long_name': p[1],
            'remark'   : p[3],
        })

    return resultList


def get_printer_info(name):
    printer = win32print.OpenPrinter(name)
    try:
        printer_info = win32print.GetPrinter(printer)
    finally:
        win32print.ClosePrinter(printer)

    return printer_info


def set_default_printer(name):
    win32print.SetDefaultPrinter(name)
    print('Changed default printer : ' + str(win32print.GetDefaultPrinter()))


def open_url_window(url = 'http://www.google.com', programName = 'chrome'):
    win32api.ShellExecute(
        0,
        'open',
        programName,
        url,
        ".",
        SW_SHOWNORMAL
    )


##############################################################################################################################

def print_png_list(pngList, dirPath, printerName):
    hDC = win32ui.CreateDC()

    for filename in pngList:
        try:
            hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
            printer_size = hDC.GetDeviceCaps(win32con.PHYSICALWIDTH), hDC.GetDeviceCaps(win32con.PHYSICALHEIGHT)
            logging.debug(printer_size)

            bmp = Image.open(dirPath + '/' + filename)
            # if bmp.size[0] < bmp.size[1]:
            #     bmp = bmp.rotate(90)

            hDC.StartDoc(dirPath + '/' + filename)
            hDC.StartPage()

            dib = ImageWin.Dib(bmp)
            labelSize = get_label_size(printerName)
            dib.draw(hDC.GetHandleOutput(), (0, 0, labelSize[0], labelSize[1]))
            hDC.EndPage()

            time.sleep(1)

        except BaseException as e:
            raise e

        finally:
            hDC.EndDoc()


##############################################################################################################################
"""
이하 프린트 샘플 소스
"""


def sample_print_string():
    str1 = "Sample Print String"
    hDC = win32ui.CreateDC()
    print(win32print.GetDefaultPrinter())  # test
    hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
    hDC.StartDoc("Test doc")
    hDC.StartPage()
    hDC.SetMapMode(win32con.MM_TWIPS)
    # draws text within a box (assume about 1400 dots per inch for typical HP printer)
    ulc_x = 1000  # give a left margin
    ulc_y = -1000  # give a top margin
    lrc_x = 11500  # width of text area-margin, close to right edge of page
    lrc_y = -15000  # height of text area-margin, close to bottom of the page
    hDC.DrawText(str1, (ulc_x, ulc_y, lrc_x, lrc_y), win32con.DT_LEFT)
    hDC.EndPage()
    hDC.EndDoc()


def sample_print_image():
    sampleFileName = './sample_waybill.png'

    hDC = win32ui.CreateDC()
    try:
        hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
        printer_size = hDC.GetDeviceCaps(win32con.PHYSICALWIDTH), hDC.GetDeviceCaps(win32con.PHYSICALHEIGHT)
        logging.debug(printer_size)

        bmp = Image.open(sampleFileName)
        # if bmp.size[0] < bmp.size[1]:
        #     bmp = bmp.rotate(90)

        hDC.StartDoc(sampleFileName)
        hDC.StartPage()

        dib = ImageWin.Dib(bmp)
        # dib.draw(hDC.GetHandleOutput(), (0, 0, printer_size[0] - 100, printer_size[1]))
        dib.draw(hDC.GetHandleOutput(), (0, 0, LabelSize.SF_WIDTH, LabelSize.SF_HEIGHT))

    except BaseException as e:
        raise e

    finally:
        hDC.EndPage()
        hDC.EndDoc()
