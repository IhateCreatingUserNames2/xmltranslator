import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from googletrans import Translator
from googletrans import LANGUAGES


class XMLTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Translator")

        self.create_widgets()

        self.translator = Translator()

    def create_widgets(self):
        # File selection
        self.file_label = tk.Label(self.root, text="No file selected")
        self.file_label.pack()

        self.select_button = tk.Button(self.root, text="Select XML File", command=self.select_file)
        self.select_button.pack()

        # Language selection
        self.from_label = tk.Label(self.root, text="Translate From:")
        self.from_label.pack()

        self.from_lang = tk.StringVar(self.root)
        self.from_lang.set("auto")  # default value
        self.from_menu = tk.OptionMenu(self.root, self.from_lang, *LANGUAGES.values())
        self.from_menu.pack()

        self.to_label = tk.Label(self.root, text="Translate To:")
        self.to_label.pack()

        self.to_lang = tk.StringVar(self.root)
        self.to_lang.set("en")  # default value
        self.to_menu = tk.OptionMenu(self.root, self.to_lang, *LANGUAGES.values())
        self.to_menu.pack()

        # Translate button
        self.translate_button = tk.Button(self.root, text="Translate", command=self.translate)
        self.translate_button.pack()

    def select_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if self.filepath:
            self.file_label.config(text=self.filepath)
        else:
            self.file_label.config(text="No file selected")

    def translate(self):
        if not hasattr(self, 'filepath') or not self.filepath:
            messagebox.showerror("Error", "Please select an XML file first.")
            return

        from_lang = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.from_lang.get())]
        to_lang = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.to_lang.get())]

        tree = ET.parse(self.filepath)
        root = tree.getroot()

        # Translate all text elements
        for elem in root.iter():
            if elem.text and elem.text.strip():  # Check if elem.text is not None and not empty
                try:
                    translated = self.translator.translate(elem.text, src=from_lang, dest=to_lang)
                    elem.text = translated.text
                except Exception as e:
                    messagebox.showerror("Translation Error", str(e))
                    return

        # Save translated XML to new file
        new_filepath = self.filepath.replace(".xml", f"_{to_lang}.xml")
        tree.write(new_filepath, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Success", f"Translation completed and saved to {new_filepath}")


if __name__ == "__main__":
    root = tk.Tk()
    app = XMLTranslatorApp(root)
    root.mainloop()
