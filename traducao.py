import os
import re
import logging
from deep_translator import GoogleTranslator
from datetime import datetime

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Cores para logs
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def log_info(message):
    logging.info(f"{Colors.OKBLUE}{message}{Colors.ENDC}")

def log_success(message):
    logging.info(f"{Colors.OKGREEN}{message}{Colors.ENDC}")

def log_warning(message):
    logging.warning(f"{Colors.WARNING}{message}{Colors.ENDC}")

def log_error(message):
    logging.error(f"{Colors.FAIL}{message}{Colors.ENDC}")

def translate_snbt_files(directory):
    """
    Traduza títulos e descrições em arquivos SNBT no diretório fornecido.

    Args:
        directory (str): Caminho para o diretório contendo os arquivos SNBT.
    """

    for filename in os.listdir(directory):
        if filename.endswith('.snbt'):
            file_path = os.path.join(directory, filename)
            log_info(f"Starting file translation: {filename}")

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            title_matches = re.findall(r'(title\s*:\s*")(.*?)(\")', content)
            description_matches = re.findall(r'(description\s*:\s*\[)(.*?)(\])', content, re.DOTALL)

            for match in title_matches:
                original_text = match[1]
                try:
                    translated_text = GoogleTranslator(source='auto', target=lang).translate(original_text)
                    translated_text = re.sub(r'(&[0-9a-fk-or])', lambda m: m.group(1), translated_text)
                    content = content.replace(f'title: "{original_text}"', f'title: "{translated_text}"')
                    log_info(f"Translated title: '{original_text}' -> '{translated_text}'")
                except Exception as e:
                    log_error(f"Error translating title '{original_text}': {e}")

            for match in description_matches:
                original_text = match[1]
                try:
                    lines = original_text.splitlines()
                    translated_lines = []
                    for line in lines:
                        line = line.strip()
                        if line:
                            translated_line = GoogleTranslator(source='auto', target=lang).translate(line)
                            if translated_line is None:
                                translated_line = line
                            translated_lines.append(translated_line)
                        else:
                            translated_lines.append('""')
                    translated_text = '\n'.join(translated_lines)
                    translated_text = re.sub(r'(&[0-9a-fk-or])', lambda m: m.group(1), translated_text)
                    content = content.replace(original_text, translated_text, 1)
                    log_info(f"Translated description: '{original_text}' -> '{translated_text}'")
                except Exception as e:
                    log_error(f"Error translating description '{original_text}': {e}")

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            log_success(f"File translated successfully: {filename}")

    log_success("All translations have been completed.")

log_success("Simple FTB Quest universal translator using GoogleTranslator made by @nebulotico")
log_success("Feel free to ask me any questions on discord or if you need any other tools")
directory_path = input("Quests folders (ex: /config/ftbquests/quests/chapters/): ")
lang = input("Language to be translated (ex: pt): ")
translate_snbt_files(directory_path)
