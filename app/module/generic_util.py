import os

import sys
import traceback


def show_brief_except(hasReturn = False):
    exc_type, exc_value, exc_tb = sys.exc_info()

    print("(Type) : {} | (Line) : {} | (Msg) : {}\n{}".format(exc_type.__name__, exc_tb.tb_lineno, exc_value, traceback.format_exc()))

    if hasReturn:
        return "(Type) : {} | (Line) : {} | (Msg) : {}\n{}".format(exc_type.__name__, exc_tb.tb_lineno, exc_value, traceback.format_exc())


def ret_path_to_file_info(path: str, returnTo: str):
    base = os.path.basename(path)  # imWaybill_LP00165786832283.pdf
    file = os.path.splitext(base)  # ('imWaybill_LP00165786832283', '.pdf')

    if returnTo == 'filename':
        return file[0]

    elif returnTo == 'ext':
        return file[1]

    return file[0], file[1]
