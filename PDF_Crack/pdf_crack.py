import PyPDF2
import os
import argparse
import subprocess
from colorama import init, Fore, Style
from alive_progress import alive_bar

# Inicializar colorama para colores en terminal
init()

# Banner decorativo
BANNER = f"""{Fore.YELLOW}
 _____ ____  _____    _____             _   
|  _  |    \\|   __|  |     |___ ___ ___| |_ 
|   __|  |  |   __|  |   --|  _| .'|  _| '_|
|__|  |____/|__|     |_____|_| |__,|___|_,_|
{Style.RESET_ALL}
"""

def crack_pdf(pdf_path, wordlist_path, verbose=False, output_path=None, clean_pdf_path=None):
    """
    Intenta descifrar un PDF protegido con contraseña usando un diccionario de palabras.
    Si se encuentra la contraseña, puede generar una copia limpia sin protección usando qpdf.
    """
    if not os.path.isfile(pdf_path):
        print(f"{Fore.RED}[-] Error: El archivo PDF '{pdf_path}' no existe.{Style.RESET_ALL}")
        return
    if not os.path.isfile(wordlist_path):
        print(f"{Fore.RED}[-] Error: El archivo de diccionario '{wordlist_path}' no existe.{Style.RESET_ALL}")
        return

    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            if not reader.is_encrypted:
                print(f"{Fore.CYAN}[*] El PDF no está protegido con contraseña.{Style.RESET_ALL}")
                return

            with open(wordlist_path, "r", encoding="latin-1", errors="ignore") as w:
                passwords = [line.strip() for line in w]
                total = len(passwords)

            print(f"{Fore.YELLOW}[*] Total de contraseñas a probar: {total:,}{Style.RESET_ALL}")

            with alive_bar(total, title="Crackeando PDF", spinner="dots_waves") as bar:
                for count, password in enumerate(passwords, 1):
                    try:
                        if reader.decrypt(password):
                            print(f"\n{Fore.GREEN}[+] Contraseña encontrada: '{password}' (después de {count} intentos){Style.RESET_ALL}")
                            
                            if output_path:
                                with open(output_path, "w") as out:
                                    out.write(password)
                                print(f"{Fore.CYAN}[*] Contraseña guardada en: {output_path}{Style.RESET_ALL}")

                            if clean_pdf_path:
                                print(f"{Fore.YELLOW}[*] Generando PDF sin contraseña: {clean_pdf_path}{Style.RESET_ALL}")
                                result = subprocess.run([
                                    "qpdf",
                                    "--password=" + password,
                                    "--decrypt",
                                    pdf_path,
                                    clean_pdf_path
                                ], capture_output=True, text=True)

                                if result.returncode == 0:
                                    if result.stderr.strip():
                                        print(f"{Fore.YELLOW}[!] Advertencias de qpdf:{Style.RESET_ALL}")
                                        print(result.stderr.strip())
                                    print(f"{Fore.GREEN}[+] PDF sin contraseña creado exitosamente como: {clean_pdf_path}{Style.RESET_ALL}")
                                else:
                                    print(f"{Fore.RED}[-] qpdf encontró un error real al generar el PDF limpio:{Style.RESET_ALL}")
                                    print(result.stderr.strip() or "(sin salida)")
                            return

                    except Exception as e:
                        if verbose:
                            print(f"{Fore.RED}[!] Error al probar '{password}': {str(e)}{Style.RESET_ALL}")
                        continue
                    bar()

    except Exception as e:
        print(f"{Fore.RED}[-] Error inesperado: {str(e)}{Style.RESET_ALL}")
        return

    print(f"\n{Fore.RED}[-] Contraseña no encontrada en el diccionario proporcionado.{Style.RESET_ALL}")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="Herramienta para crackear contraseñas de PDFs")
    parser.add_argument("pdf", help="Ruta al archivo PDF protegido")
    parser.add_argument("wordlist", help="Ruta al archivo de diccionario de contraseñas")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar salida detallada")
    parser.add_argument("-o", "--output", help="Archivo donde guardar la contraseña si se encuentra")
    parser.add_argument("-c", "--clean", metavar="SALIDA.pdf", help="Generar PDF limpio sin contraseña con este nombre")

    args = parser.parse_args()

    print(f"{Fore.YELLOW}[*] Iniciando ataque de fuerza bruta...{Style.RESET_ALL}")
    crack_pdf(args.pdf, args.wordlist, args.verbose, args.output, args.clean)

if __name__ == "__main__":
    main()
