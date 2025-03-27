import subprocess
import threading
import argparse
import time
import sys
import re
import os

class cli:
    def __init__(self, file):
        self.current_dir = os.getcwd()

        self.file = file
        self.visuals = self.visual(self)
        self.exec_gen = self.exec_gen_(self)
        self.find_imports = self.find_import(self)

    def clean_terminal(self):
        if self.exec_gen.error == 1 \
        or self.find_imports.error == 1:
            print("\033[J", end='', flush=True)

        if self.exec_gen.descerror: print(f"\n {self.visuals.DK_ORANGE}>{self.visuals.RESET} {self.exec_gen.descerror}")
        if self.find_imports.descerror: print(f"\n {self.visuals.DK_ORANGE}>{self.visuals.RESET} {self.find_imports.descerror}")

    class visual:
        def __init__(self, self_cli):
            self.cli = self_cli
            self.RESET = "\033[0m"
            self.DK_ORANGE = "\033[38;5;130m"
            self.Neg = "\033[1m"
            self.hue = 0

        def hsl_to_rgb(self, h, s, l):
            h = h % 360
            c = (1 - abs(2 * l - 1)) * s
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = l - c / 2

            if 0 <= h < 60: r, g, b = c, x, 0
            elif 60 <= h < 120: r, g, b = x, c, 0
            elif 120 <= h < 180: r, g, b = 0, c, x
            elif 180 <= h < 240: r, g, b = 0, x, c
            elif 240 <= h < 300: r, g, b = x, 0, c
            elif 300 <= h < 360: r, g, b = c, 0, x

            r = int((r + m) * 255) ; g = int((g + m) * 255) ; b = int((b + m) * 255)
            return r, g, b

        def rgb_text(self, text, r, g, b): return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

        def animate_rgb_text(self, text, delay=0.01):
            r, g, b = self.hsl_to_rgb(self.hue, s=1.0, l=0.5)
            self.hue = (self.hue + 1) % 360
            time.sleep(delay)
            return f"    \033[1m{self.rgb_text(text, r, g, b)}\033[0m"

    class exec_gen_:
        def __init__(self, self_cli):
            self.cli = self_cli
            self.current_dir = None
            self.target_file = None
            self.file_name = None
            self.error = 0
            self.descerror = ""
            self.visuals = self.cli.visuals

        def preparations(self):
            self.current_dir = os.getcwd()

            parser = argparse.ArgumentParser(description="Script to generate .exe and preventing bugs")
            parser.add_argument("file", type=str, help="Put the name of file after the command (with the extension '.py')")

            # args = parser.parse_args()  #TODO
            # self.file_name = args.file  #TODO
            # self.target_file = os.path.join(self.current_dir, self.file_name)  #TODO
            self.target_file = self.cli.file  #FIX

            if not os.path.exists(self.target_file):
                self.descerror = f"Error: File '{self.target_file}' does not exist."
                self.error = 1
                return

        def run_pyinstaller(self):
            global process_finished

            def print_footer():
                """Função que mantém a mensagem 'Aguarde download' na última linha."""
                while not process_finished:
                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"   {self.visuals.Neg}| Gerando executável do '{self.file_name}', aguarde finalização. |{self.visuals.RESET}")}\n\033[F")
                    sys.stdout.flush()

            process_finished = False
            command = ["pyinstaller", self.target_file]
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            footer_thread = threading.Thread(target=print_footer)
            footer_thread.start()

            # Lê a saída do PyInstaller em tempo real
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    sys.stdout.write(f"\033[F\r\033[K{output.strip()}\033[K\n\n")
                    sys.stdout.flush()

            process_finished = True
            footer_thread.join()

            print(f"\r \033[F\r\033[K\033[f\r\033[K\033[2E{self.visuals.Neg}{self.visuals.DK_ORANGE}>{self.visuals.RESET}{self.visuals.Neg} Executável gerado com sucesso!\n{self.visuals.RESET}\033[3E")

        def main(self):
            script = self.cli.exec_gen
            script.preparations()
            script.run_pyinstaller()


    class find_import:
        def __init__(self, self_cli):
            self.cli = self_cli
            self.visuals = self.cli.visuals

            self.error = 0
            self.descerror = ""

            self.imports = None

        def hsl_to_rgb(self, h, s, l):
            h = h % 360
            c = (1 - abs(2 * l - 1)) * s
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = l - c / 2

            if 0 <= h < 60: r, g, b = c, x, 0
            elif 60 <= h < 120: r, g, b = x, c, 0
            elif 120 <= h < 180: r, g, b = 0, c, x
            elif 180 <= h < 240: r, g, b = 0, x, c
            elif 240 <= h < 300: r, g, b = x, 0, c
            elif 300 <= h < 360: r, g, b = c, 0, x

            r = int((r + m) * 255) ; g = int((g + m) * 255) ; b = int((b + m) * 255)
            return r, g, b

        def rgb_text(self, text, r, g, b): return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

        def animate_rgb_text(self, text, delay=0.01):
            import time
            from bcpkgfox import DK_ORANGE
            hue = 0
            print(f" {DK_ORANGE}>{self.visuals.RESET} Dependências do arquivo {self.visuals.DK_ORANGE}'{self.target_file}'{self.visuals.RESET} identificadas com sucesso")
            time.sleep(2)
            print(f"{DK_ORANGE} PIP:{self.visuals.RESET}\033[s")
            while True:
                r, g, b = self.hsl_to_rgb(hue, s=1.0, l=0.5)
                terminal_width = shutil.get_terminal_size().columns
                num_lines = len(text) // terminal_width + 1
                print(f"\033[u\033[0J ---> \033[1m{self.rgb_text(text, r, g, b)}\033[0m (CTRL + C)", end="\r")
                hue = (hue + 1) % 360
                time.sleep(delay)

        def main(self):
            current_dir = os.getcwd()

            parser = argparse.ArgumentParser(description="A CLI tool to find imports.")
            parser.add_argument("file", type=str, help="The target .py file to process")

            # args = parser.parse_args()  #TODO
            # self.file_name = args.file  #TODO
            # self.target_file = os.path.join(self.current_dir, self.file_name)  #TODO
            self.target_file = self.cli.file  #FIX

            if not os.path.exists(self.target_file):
                self.descerror = f"Error: File '{self.target_file}' does not exist."
                self.error = 1
                return

            try:
                with open(self.target_file, "r", encoding="utf-8", errors="replace") as file:
                    file_content = file.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                return

            if not file_content:
                print(f"Erro: Não foi possível ler o arquivo '{self.target_file}' com nenhuma codificação testada.")
                return

            self.imports = []
            import_data = {
                "extract_pdf": "PyMuPDF",
                "import requests": "requests",
                "import pyautogui": "pyautogui",
                "import cv2": "opencv-python",
                "from PIL": "Pillow",
                "from reportlab.lib import utils": "reportlab",
                "from PyPDF2 import PdfMerger": "PyPDF2",
                "import PyPDF2": "PyPDF2",
                "invoke_api_": "requests",
                "wait_for": "pygetwindow",
                "from selenium_stealth import stealth": "selenium-stealth",
                "import undetected_chromedriver": "undetected-chromedriver",
                "from webdriver_manager.chrome import ChromeDriverManager": "webdriver-manager",
                "move_to_image": ["pyscreeze", "pyautogui", "Pillow", "opencv-python"],
                "move_mouse_smoothly": ["pyscreeze", "pyautogui", "Pillow"],
                "initialize_driver": ["webdriver-manager", "undetected-chromedriver", "pyautogui", "psutil"],
                "stealth max": ["webdriver-manager", "undetected-chromedriver", "fake-useragent"]
            }

            for name, import_name in import_data.items():
                if re.search(fr"\b{name}\b", file_content):
                    if isinstance(import_name, list):
                        self.imports.extend(import_name)
                    else: self.imports.append(import_name)

            self.imports = list(set(self.imports))
            import pyperclip
            pyperclip.copy(f"pip install {' '.join(self.imports)}")

            from bcpkgfox import DK_ORANGE, ORANGE, RESET
            if self.imports:

                # try: self.animate_rgb_text(f'pip install {" ".join(self.imports)}', delay=0.002)
                try: self.animate_rgb_text(f'pip install testetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetestetesteteste', delay=0.002)
                except KeyboardInterrupt: print(f" {DK_ORANGE}--->{RESET} {ORANGE}pip install {' '.join(self.imports)}{RESET}                   \n\n {DK_ORANGE}>{RESET} Copiado para sua área de transferencia. \n(obs: só identifica as libs que são pertencentes da bibliotca bcfox) \n")
            else: print("No libraries from the list were found in the script.")

code = cli("bcpkgfox//cli.py")
code.find_imports.main()
code.clean_terminal()
print()