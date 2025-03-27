import subprocess
import threading
import argparse
import shutil
import math
import time
import sys
import re
import os

class cli:
    def __init__(self):
        self.current_dir = os.getcwd()

        self.visuals = self.visual(self)
        self.exec_gen = self.exec_gen_(self)
        self.find_imports = self.find_import(self)
        self.venv_managment = self.venv_mangt(self)

        self.parser = argparse.ArgumentParser(
            add_help=False
        )
        args = self.parser.parse_args()
        self.file = args.filename
        self._setup_arguments()

    def _setup_arguments(self):
        """Configure all CLI arguments"""
        venv_group = self.parser.add_argument_group('virtual environment options')
        venv_group.add_argument(
            '-v', '--venv',
            action='store_true',
            help="Creates a virtual environment with all dependencies installed"
        )

        venv_group.add_argument(
            '-vc', '--venv-clean',
            action='store_true',
            help="Creates a virtual environment without dependencies"
        )

        venv_group.add_argument(
            '-rv', '--recreate-venv',
            action='store_true',
            help="Recreates venv (without dependencies)"
        )

        venv_group.add_argument(
            '-dv', '--delete-venv',
            action='store_true',
            help="Deletes venv"
        )

        self.parser.add_argument(
            '-fi', '--find-imports',
            action='store_true',
            help="Finds all imports necessary for the lib to work"
        )

        self.parser.add_argument(
            'filename',
            type=str,
            nargs='?',
            help="Input file to process"
        )

        self.parser.add_argument(
            '-h', '--help',
            action='help',
            default=argparse.SUPPRESS,
            help="Salveeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        )

    def main(self):
        args = self.parser.parse_args()

        if args.venv:
            self.venv_manager.main()
        elif args.venv_clean:
            self.venv_manager.create_venv()
        elif args.recreate_venv:
            self.venv_manager.recreate_venv()
        elif args.delete_venv:
            self.venv_manager.delete_venv()

        if args.find_imports:
            self.imports_finder.main()

        if args.filename:
            self._process_file(args.filename)

    def clean_terminal(self):
        if self.exec_gen.error == 1 \
        or self.find_imports.error == 1 \
        or self.venv_managment.error == 1:
            print("\033[J", end='', flush=True)

        if self.exec_gen.descerror: print(f"\n {self.visuals.DK_ORANGE}>{self.visuals.RESET} {self.exec_gen.descerror}")
        if self.find_imports.descerror: print(f"\n {self.visuals.DK_ORANGE}>{self.visuals.RESET} {self.find_imports.descerror}")
        if self.venv_managment.descerror: print(f"\n {self.visuals.DK_ORANGE}>{self.visuals.RESET} {self.venv_managment.descerror}")

    class visual:
        def __init__(self, self_cli):
            self.cli = self_cli

            self.DK_ORANGE = "\033[38;5;130m"
            self.ORANGE = "\033[38;5;214m"
            self.RD = "\033[38;5;196m"
            self.GR = "\033[38;5;34m"
            self.RESET = "\033[0m"
            self.bold = "\033[1m"

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
            self.current_dir = self.cli.current_dir
            self.target_file = self.cli.file
            self.error = 0
            self.descerror = ""
            self.visuals = self.cli.visuals

        def preparations(self):
            self.current_dir = os.getcwd()

            parser = argparse.ArgumentParser(description="Script to generate .exe and preventing bugs")
            parser.add_argument("file", type=str, help="Put the name of file after the command (with the extension '.py')")

            # args = parser.parse_args()  #TODO
            # self.file_name = args.file  #TODO
            self.target_file = os.path.join(self.current_dir, self.file_name)  #TODO
            # self.target_file = self.cli.file  #FIX

            if not os.path.exists(self.target_file):
                self.descerror = f"Error: File '{self.target_file}' does not exist."
                self.error = 1
                return

        def run_pyinstaller(self):
            global process_finished

            braille_spinner = [
                '\u280B',  # ⠋
                '\u2809',  # ⠙
                '\u2839',  # ⠹
                '\u2838',  # ⠸
                '\u283C',  # ⠼
                '\u2834',  # ⠴
                '\u2826',  # ⠦
                '\u2827',  # ⠧
                '\u2807',  # ⠇
                '\u280F'   # ⠏
            ]

            retro_computer_style = [
            '\u23BA',  # ⎺
            '\u23BB',  # ⎻
            '\u23BC',  # ⎼
            '\u23BD',  # ⎽
            ]

            def print_footer():
                s = 0
                n = 0
                while not process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(braille_spinner): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"  {self.visuals.bold} {braille_spinner[n]} Gerando executável do '{self.target_file}', aguarde finalização. {braille_spinner[n]} {self.visuals.RESET}")} \n\033[F")
                    sys.stdout.flush()
                    s += 1

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

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    sys.stdout.write(f"\033[F\r\033[K{output.strip()}\033[K\n\n")
                    sys.stdout.flush()

            process_finished = True
            footer_thread.join()

            print(f"\r \033[F\r\033[K\033[f\r\033[K\033[2E{self.visuals.bold}{self.visuals.DK_ORANGE}>{self.visuals.RESET}{self.visuals.bold} Executável gerado com sucesso!\n{self.visuals.RESET}\033[3E")

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
            print(f"{DK_ORANGE} PIP:{self.visuals.RESET}\n\n\033[s")
            while True:
                r, g, b = self.hsl_to_rgb(hue, s=1.0, l=0.5)
                terminal_width = shutil.get_terminal_size().columns
                num_lines = math.floor(len(text) / terminal_width)
                if num_lines == 0: print("\033[1B", end="\r")
                print(f"\033[{num_lines}A\033[0J {DK_ORANGE}---> \033[1m{self.rgb_text(text, r, g, b)}\033[0m (CTRL + C)", end="\r")
                hue = (hue + 1) % 360
                time.sleep(delay)

        def main(self, return_=False):
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

            from bcpkgfox import DK_ORANGE, ORANGE, RESET
            if self.imports:
                if not return_:
                    pyperclip.copy(f"pip install {' '.join(self.imports)}")

                    # try: self.animate_rgb_text(f'pip install {" ".join(self.imports)}', delay=0.002)
                    text = f"pip install {' '.join(self.imports)}"
                    terminal_width = shutil.get_terminal_size().columns
                    num_lines = math.floor(len(text) / terminal_width)

                    try: self.animate_rgb_text(text, delay=0.002)
                    except KeyboardInterrupt: print(f"\033[{num_lines}A\033[0J {DK_ORANGE}--->{RESET} {ORANGE}pip install {' '.join(self.imports)}{RESET}                   \n\n {DK_ORANGE}>{RESET} Copiado para sua área de transferencia. \n(obs: só identifica as libs que são pertencentes da bibliotca bcfox) \n")
                else: return self.imports
            else: print("No libraries from the list were found in the script.")



    class venv_mangt:
        def __init__(self, self_cli):
            self.cli = self_cli
            self.current_dir = self.cli.current_dir
            self.target_file = self.cli.file
            self.error = 0
            self.descerror = ""
            self.visuals = self.cli.visuals

        def delete_venv(self):

            braille_spinner = [
                '\u280B',
                '\u2809',
                '\u2839',
                '\u2838',
                '\u283C',
                '\u2834',
                '\u2826',
                '\u2827',
                '\u2807',
                '\u280F'
            ]

            retro_computer_style = [
            '\u23BA',  # ⎺
            '\u23BB',  # ⎻
            '\u23BC',  # ⎼
            '\u23BD',  # ⎽
            ]

            process_finished = False
            def print_footer():
                s = 0
                n = 0
                while not process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(braille_spinner): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"  {self.visuals.bold} {braille_spinner[n]} Deleting virtual environment {braille_spinner[n]} {self.visuals.RESET}")} \n\033[F")
                    sys.stdout.flush()
                    s += 1

            footer_thread = threading.Thread(target=print_footer)
            footer_thread.start()

            if os.path.exists(os.path.join(self.current_dir, ".venv")):
                try:
                    shutil.rmtree(".venv")
                except Exception as e:
                    print(f"{self.visuals.RD} > Failed to remove venv: {e} {self.visuals.RESET}")
                    return False
            process_finished = True
            footer_thread.join()

            print(f"{self.visuals.bold}{self.visuals.GR} > Oldest virtual environment deleted with sucessfuly {self.visuals.RESET}\n")


        def create_venv(self):

            braille_spinner = [
                '\u280B',
                '\u2809',
                '\u2839',
                '\u2838',
                '\u283C',
                '\u2834',
                '\u2826',
                '\u2827',
                '\u2807',
                '\u280F'
            ]

            retro_computer_style = [
            '\u23BA',  # ⎺
            '\u23BB',  # ⎻
            '\u23BC',  # ⎼
            '\u23BD',  # ⎽
            ]

            process_finished = False
            def print_footer():
                s = 0
                n = 0
                while not process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(braille_spinner): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"  {self.visuals.bold} {braille_spinner[n]} Generating virtual environment {braille_spinner[n]} {self.visuals.RESET}")} \n\033[F")
                    sys.stdout.flush()
                    s += 1

            process_finished = False
            command = [sys.executable, '-m', 'venv', ".venv"]
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            footer_thread = threading.Thread(target=print_footer)
            footer_thread.start()

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    sys.stdout.write(f"\033[F\r\033[K{output.strip()}\033[K\n\n")
                    sys.stdout.flush()

            process_finished = True
            footer_thread.join()

            print(f"{self.visuals.bold}{self.visuals.GR} > Virtual environment created successfully {self.visuals.RESET}", end="\r")

        def install_imports(self):
            pip_path = os.path.join(".venv", 'Scripts' if os.name == 'nt' else 'bin', 'pip')
            librarys = self.cli.find_imports.main(return_=True)

            braille_spinner = [
                '\u280B',
                '\u2809',
                '\u2839',
                '\u2838',
                '\u283C',
                '\u2834',
                '\u2826',
                '\u2827',
                '\u2807',
                '\u280F'
            ]

            retro_computer_style = [
            '\u23BA',  # ⎺
            '\u23BB',  # ⎻
            '\u23BC',  # ⎼
            '\u23BD',  # ⎽
            ]

            process_finished = False
            def print_footer():
                s = 0
                n = 0
                while not process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(braille_spinner): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"  {self.visuals.bold} {braille_spinner[n]} Installing all dependencies {braille_spinner[n]} {self.visuals.RESET}")} \n\033[F")
                    sys.stdout.flush()
                    s += 1

            log_animation = threading.Thread(target=print_footer)
            log_animation.start()

            process_finished = False
            try:
                for lib in librarys:
                    result = subprocess.run(
                        [pip_path, 'install', lib],
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )


                    if result.stdout:
                        print(f"\033[0J{result.stdout.strip()}\033[0J")

            except subprocess.CalledProcessError as e:
                print(f"{self.visuals.bold}{self.visuals.RD} Failed to install {lib}: {e.stderr.strip()}{self.visuals.RESET}", end="\r")
                return False
            finally:
                process_finished = True
                log_animation.join()
            print(f" {self.visuals.bold}{self.visuals.GR} > All packges installed with sucessfully {self.visuals.RESET}", end="\r")

        def recreate_venv(self):
            self.delete_venv()
            self.create_venv()


        def main(self):
            self.delete_venv()
            self.create_venv()
            self.install_imports()