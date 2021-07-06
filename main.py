import time

import dearpygui.dearpygui as dpg
import threading
from io import BytesIO
from gtts import gTTS
import fitz


class ReaderPDF:
    def __init__(self):
        self.main_window = 0
        self.directory_text = 0
        self.progress_bar = 0
        self.combobox = 0
        self.language_list = ["en", "fn", "zh-CN", "pt", "es", "de", "hi", "id", "it", "jv", "ja", "ms"]
        self.output_text = "output.mp3"
        self.input_filename = ""
        self.input_directory = './'

    def pdf_dialog_callback(self, sender, data):
        self.input_filename = data["file_name"]
        dpg.set_value(self.directory_text, data["file_path_name"])
        self.input_directory = data["file_path_name"]

    def pdf_button_callback(self):
        file_dialog = dpg.add_file_dialog(label="PDF", callback=self.pdf_dialog_callback)
        dpg.add_file_extension('.pdf', parent=file_dialog)

    def show_success(self):
        with dpg.window(label="Success", autosize=True, modal=True, pos=[650 // 2, 650 // 2]) as mdl:
            dpg.add_text(f"saved as {self.output_text}", color=[0, 255, 0, 255])
            dpg.add_button(label="Ok", callback=lambda x: dpg.delete_item(mdl))

    def show_error(self, message: str = ""):
        with dpg.window(label="Error", autosize=True, modal=True, pos=[580 // 2, 580 // 2]) as mdl:
            dpg.add_text(f"ERROR {message}\nPlease select file first!", color=[255, 0, 0, 255])
            dpg.add_button(label="Ok", callback=lambda x: dpg.delete_item(mdl))

    def __gTTSFunc__(self, text, lang):
        tts = gTTS(text, lang=lang)
        tts.save(self.output_text)
        # tts.write_to_fp(mp3_fp)

    def process_pdf(self):
        self.status = "Status"
        if self.input_filename == "" or self.input_filename == ".pdf":
            self.show_error("File Not Found")
            return

        try:

            text = ""
            with fitz.open(self.input_directory) as doc:
                for pages in doc:
                    text += pages.getText()
            # print(text)
            # mp3_fp = BytesIO()
            print(f" combobox: {dpg.get_value(self.combobox)}")
            t = threading.Thread(target=self.__gTTSFunc__, args=(text, dpg.get_value(self.combobox)))
            t.start()
            ctr = 0.0
            while t.is_alive():
                dpg.set_value(self.progress_bar, ctr)
                if ctr <= 0.95:
                    ctr += 0.01
                time.sleep(0.01)
            dpg.set_value(self.progress_bar, 1)
            self.show_success()

        except Exception as e:
            self.show_error("Something Error")
            print(e)

    def show(self):
        with dpg.window(label="Main Window", no_close=True, autosize=True, pos=[650 // 2, 650 // 2]) as main_window:
            self.main_window = main_window
            self.directory_text = dpg.add_text("No File Selected")
            dpg.add_button(label="Import PDF", callback=self.pdf_button_callback)
            self.combobox = dpg.add_combo(self.language_list, label="Language", default_value="en")
            self.progress_bar = dpg.add_progress_bar(label="Progress", default_value=0.0)
            dpg.add_button(label="Process File", callback=self.process_pdf)


def main():
    # Class PDF Reader
    PDReader = ReaderPDF()
    PDReader.show()

    # Setup DearPyGUI
    # dpg.set_primary_window(PDReader.main_window, True)
    dpg.setup_viewport()
    dpg.set_viewport_resizable(True)
    dpg.set_viewport_width(800)
    dpg.set_viewport_max_width(800)
    dpg.set_viewport_height(800)
    dpg.set_viewport_max_height(800)
    dpg.set_viewport_clear_color([18, 18, 18, 255])
    dpg.set_viewport_title("PDF READER")
    dpg.show_documentation()
    dpg.start_dearpygui()


if __name__ == '__main__':
    # Invoke main
    main()
