import logging
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QGroupBox, QTextEdit, QGridLayout, QPushButton, QLineEdit, QBoxLayout, QFileDialog

from app.module.generic_util import ret_path_to_file_info, show_brief_except
from app.module.printer import get_printer_list, set_default_printer, get_printer_info, print_png_list
from app.settings import APP_NAME, ICON_PATH, TARGET_PRINTER_NAMES, DESKTOP_DIR


class AppWindow(QWidget):

    def __init__(self):
        super().__init__()

        self._default_config()
        self._layout()

        self.show()

    def _default_config(self):
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(1000, 700)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _layout(self):
        self._layout_path()
        self._layout_progress()
        self._layout_control()

        layout = QGridLayout()
        layout.addWidget(self._path_group, 0, 0)
        layout.addWidget(self._control_group, 1, 0)
        layout.addWidget(self._progress_group, 2, 0)

        self.setLayout(layout)

    ##############################################################################################################################

    def _layout_path(self):
        self._path_group = QGroupBox('Path')
        self._path_lineEdit = QLineEdit()
        # self._path_lineEdit.setDisabled(True)

        self._path_btn = QPushButton('Select Path', self)
        self._path_btn.clicked.connect(self.click_select_path)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self._path_lineEdit, 0, 0)
        grid_layout.addWidget(self._path_btn, 0, 1)
        self._path_group.setLayout(grid_layout)

    def click_select_path(self):
        path = QFileDialog.getExistingDirectory(self, caption = 'Select the path', directory = DESKTOP_DIR)
        print('Select Path : ' + path)
        self._path_lineEdit.setText(path)
        self.set_progress_text('[+] Selected path : ' + path)

        self._pngList = []
        files = os.listdir(path)

        self.set_progress_text('[+] Load png files')
        for f in files:
            if os.path.isfile(os.path.join(path, f)) and ret_path_to_file_info(f, 'ext') == '.png':
                self._pngList.append(f)
                self.set_progress_text(path + '/' + f)

        logging.debug(files)
        logging.info(self._pngList)

    ##############################################################################################################################

    def _layout_control(self):
        self._control_group = QGroupBox('Control')

        self._control_lineEdit = QLineEdit()
        self._control_lineEdit.setDisabled(True)

        self._control_btn_start = QPushButton('Start', self)
        self._control_btn_start.clicked.connect(self.click_start)

        self._control_btn_stop = QPushButton('Stop', self)
        self._control_btn_stop.clicked.connect(self.click_stop)
        self._control_btn_stop.setDisabled(True)

        topBox = QBoxLayout(QBoxLayout.LeftToRight)
        topBox.addWidget(self._control_lineEdit)

        self.set_progress_text('[+] Load printers connected currently')
        pList = get_printer_list()
        if not pList:
            self.set_progress_text('[+] Connected nothing')

        else:
            self._printer_btn = { }

            for p in pList:
                self.set_progress_text(p.__str__())
                if p['name'] in TARGET_PRINTER_NAMES:
                    self._printer_btn[p['name']] = QPushButton(p['name'], self)
                    self._printer_btn[p['name']].clicked.connect(getattr(self, "click_pbtn_" + p['name']))
                    topBox.addWidget(self._printer_btn[p['name']])

            self.set_progress_text('[+] Create meaningful printer buttons')

        bottomBox = QBoxLayout(QBoxLayout.LeftToRight)
        bottomBox.addStretch(1)
        bottomBox.addWidget(self._control_btn_start)
        bottomBox.addWidget(self._control_btn_stop)
        bottomBox.addStretch(1)

        box = QBoxLayout(QBoxLayout.TopToBottom)
        box.addLayout(topBox)
        box.addLayout(bottomBox)

        self._control_group.setLayout(box)

    def select_printer(self, name):
        print('Select Printer :', name)
        self._control_lineEdit.setText(name)
        printerInfo = get_printer_info(name)
        self.set_progress_text('[+] User Selected : ' + name + ' will be Windows default Printer\n{}'.format(printerInfo))
        set_default_printer(name)

    def click_pbtn_ICB_PRINTER(self):
        self.select_printer('ICB_PRINTER')

    def click_pbtn_OUT_PRINTER(self):
        self.select_printer('OUT_PRINTER')

    def click_pbtn_IN_PRINTER(self):
        self.select_printer('IN_PRINTER')

    def click_pbtn_SF_PRINTER(self):
        self.select_printer('SF_PRINTER')

    def click_pbtn_YTO_PRINTER(self):
        self.select_printer('YTO_PRINTER')

    ##############################################################################################################################

    def click_start(self):
        if not self._path_lineEdit.text():
            self.set_progress_text('[!!] Please, Select Directory which you print')
            return

        if not self._control_lineEdit.text():
            self.set_progress_text('[!!] Please, Select Windows Printer which you use')
            return

        print('Start')
        self.set_progress_text('[+] Start Printer to be printing')

        try:
            print_png_list(self._pngList, self._path_lineEdit.text(), self._control_lineEdit.text())

        except:
            self.set_progress_text('[!!] Error Occurred\n' + show_brief_except(True))

        self.set_progress_text('[+] Done')

    def click_stop(self):
        print('Stop')

    ##############################################################################################################################

    def _layout_progress(self):
        self._progress_group = QGroupBox('Progress')
        self._progress_textEdit = QTextEdit()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self._progress_textEdit, 0, 0)
        self._progress_group.setLayout(grid_layout)

    def set_progress_text(self, msg = ''):
        current_text = self._progress_textEdit.toPlainText()

        if current_text:
            self._progress_textEdit.setText(current_text + '\n' + msg + '.')
        else:
            self._progress_textEdit.setText(msg + '.')

    ##############################################################################################################################


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)

    app = QApplication([])
    window = AppWindow()
    sys.exit(app.exec_())
