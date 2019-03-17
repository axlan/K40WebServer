from threading import Thread
import traceback
import os.path

import remi.gui as gui
from remi import start, App
from k40nano import PngPlotter
from .EgvParser import parse_egv
from .EgvSend import send_egv

class K40WebServer(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
        working_path = os.getcwd()
        super(K40WebServer, self).__init__(*args, static_file_path={'my_resources':res_path, 'output':working_path})
        self.selected_file = None
        self.print_thread = None
        self.stop = False


    def main(self):
        container = gui.VBox(width=500, height=500)
        self.status_lbl = gui.Label('First Upload EGV')

        upload_box = gui.VBox()
        upload_lbl = gui.Label('Upload EGV')
        self.upload_bt = gui.FileUploader('./', width=200, height=30, margin='10px')
        upload_box.append(upload_lbl)
        upload_box.append(self.upload_bt)
        self.upload_bt.onsuccess.connect(self.fileupload_on_success)
        self.upload_bt.onfailed.connect(self.fileupload_on_failed)

        self.preview = gui.Image('/my_resources:empty-image.png', width=200, height=200)

        self.print_bt = gui.Button('Print Uploaded Design')
        self.print_bt.onclick.connect(self.print_button_pressed)
        self.print_bt.set_enabled(False)
    
        self.stop_bt = gui.Button('Stop Printing')
        self.stop_bt.onclick.connect(self.stop_button_pressed)
        self.stop_bt.set_enabled(False)

        # appending a widget to another
        container.append(self.status_lbl)
        container.append(upload_box)
        container.append(self.preview)
        container.append(self.print_bt)
        container.append(self.stop_bt)

        # returning the root widget
        return container

    def clear_selected_file(self):
        self.preview.set_image('/my_resources:empty-image.png')
        self.selected_file = None
        self.print_bt.set_enabled(False)
        self.stop_bt.set_enabled(False)
        self.upload_bt.set_enabled(True)


    # listener function
    def fileupload_on_success(self, widget, filename):
        try:
            plotter = PngPlotter(filename + '.png')
            parse_egv(filename, plotter)
            plotter.close()
            self.preview.set_image('/output:{}.png'.format(filename))
        except:
            print(traceback.format_exc())
            self.status_lbl.set_text('Invalid EGV: ' + filename)
            self.clear_selected_file()
            return
        self.status_lbl.set_text('Ready to Print: ' + filename)
        self.selected_file = filename
        self.print_bt.set_enabled(True)

    def fileupload_on_failed(self, widget, filename):
        self.status_lbl.set_text('Upload Failed: ' + filename)
        self.clear_selected_file()

    def print_button_pressed(self, widget):
        self.status_lbl.set_text('Printing: ' + self.selected_file)
        self.print_bt.set_enabled(False)
        self.upload_bt.set_enabled(False)
        self.stop_bt.set_enabled(True)
        self.stop = False
        self.print_thread = Thread(target=self.print_job)
        self.print_thread.start()

    def stop_button_pressed(self, widget):
        pass

    def print_job(self):
        try:
            send_egv(self.selected_file)
            self.status_lbl.set_text('Print Completed: ' + self.selected_file)
        except Exception as e:
            print(traceback.format_exc())
            inputDialog = gui.GenericDialog('Print Error', str(e))
            inputDialog.show(self)
            self.status_lbl.set_text('Print Error: ' + self.selected_file)
        self.clear_selected_file()

if __name__ == '__main__':
    # starts the web server
    start(K40WebServer, debug=True, address='0.0.0.0', port=8081, start_browser=False, multiple_instance=False)
