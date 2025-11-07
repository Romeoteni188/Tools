import requests
import os
from colorama import Fore, Style, init

os.system("printf '\033]2;Cerberus v1.0 🕵🏽‍♂️\a'")

# Inicializar colorama
init(autoreset=True)

# Logo
print(Style.BRIGHT + Fore.YELLOW + r'''
                            /\_/\____,
                  ,___/\_/\ \  ~     /
                  \     ~  \ )   XXX
                    XXX     /    /\_/\___,
                       \o-o/-o-o/   ~    /
                        ) /     \    XXX
                       _|    / \ \_/
                    ,-/   _  \_/   \
                   / (   /____,__|  )
                  (  |_ (    )  \) _|
                 _/ _)   \   \__/   (_
                (,-(,(,(,/      \,),),)
''')
print(f"{' ' * 17}{Fore.WHITE}{Style.BRIGHT}Created by Hack Underway{Style.RESET_ALL}")

BASE_URL = "https://cvedb.shodan.io"

def fetch_cves(query):
    """Consulta la API de cvedb.shodan.io por producto o CVE puntual."""
    results = []
    query = query.strip()

    # Si es CVE-ID, buscar directamente
    if query.upper().startswith("CVE-"):
        url = f"{BASE_URL}/cve/{query.upper()}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                results.append(response.json())
            except ValueError:
                print(f"{Fore.RED}La respuesta del servidor no es JSON válido.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No se encontró información para {query}.{Style.RESET_ALL}")
    else:
        # Búsqueda por producto
        url = f"{BASE_URL}/cves?product={query}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict) and "cves" in data:
                    cve_list = data["cves"]
                    print(f"{Fore.LIGHTCYAN_EX}Se encontraron {len(cve_list)} CVEs para '{query}'. Mostrando los primeros 10...{Style.RESET_ALL}")
                    results.extend(cve_list[:10])  # Limita a los primeros 10
                else:
                    print(f"{Fore.RED}Formato de respuesta inesperado para '{query}'.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}No se pudo analizar la respuesta JSON para '{query}'.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error al buscar vulnerabilidades para '{query}'. Código: {response.status_code}{Style.RESET_ALL}")

    return results

def display_cves(cves):
    """Muestra los CVEs obtenidos de forma formateada."""
    results_output = []

    if not cves:
        print(f"{Fore.YELLOW}No se encontraron vulnerabilidades.{Style.RESET_ALL}")
        return results_output

    for idx, cve in enumerate(cves, 1):
        print(f"{Fore.GREEN}--- CVE {idx} ---{Style.RESET_ALL}")
        cve_id = cve.get("id") or cve.get("cve_id", "N/A")
        description = cve.get("summary", "Sin descripción.")
        cvss = cve.get("cvss", "N/A")
        severity = cve.get("severity", "N/A")
        exploited = cve.get("exploit") == True
        references = cve.get("references", [])

        output = f"--- CVE {idx} ---\n"
        output += f"ID: {cve_id}\n"
        output += f"Descripción: {description}\n"
        output += f"CVSS: {cvss} | Severidad: {severity}\n"
        output += f"¿Explotado?: {'Sí' if exploited else 'No'}\n"
        output += "Referencias:\n"
        for ref in references:
            output += f" - {ref}\n"

        print(f"{Fore.CYAN}ID:{Style.RESET_ALL} {cve_id}")
        print(f"{Fore.CYAN}Descripción:{Style.RESET_ALL} {description}")
        print(f"{Fore.CYAN}CVSS:{Style.RESET_ALL} {cvss} | Severidad: {severity}")
        print(f"{Fore.CYAN}¿Explotado?:{Style.RESET_ALL} {'Sí' if exploited else 'No'}")
        print(f"{Fore.CYAN}Referencias:{Style.RESET_ALL}")
        for ref in references:
            print(f"{Fore.BLUE} - {ref}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{'-'*60}{Style.RESET_ALL}")

        results_output.append(output + '-'*60 + '\n\n')

    return results_output

def save_results(results, query):
    """Guarda resultados en archivo TXT."""
    if not results:
        print(f"{Fore.YELLOW}No hay resultados para guardar.{Style.RESET_ALL}")
        return

    filename = f"cvedb_results_{query.replace(' ', '_')}_{os.urandom(3).hex()}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(results)

    print(f"{Fore.GREEN}Resultados guardados en {filename}{Style.RESET_ALL}")

def main():
    while True:
        query = input(f"\n{Fore.LIGHTBLUE_EX}Introduce un CVE o nombre de producto (ej. CVE-2024-12345, nginx): {Style.RESET_ALL}").strip()
        cves = fetch_cves(query)
        results = display_cves(cves)

        if results:
            choice = input(f"{Fore.YELLOW}¿Guardar resultados en archivo? (s/n): {Style.RESET_ALL}").lower()
            if choice == 's':
                save_results(results, query)

        again = input(f"{Fore.LIGHTBLUE_EX}¿Deseas hacer otra búsqueda? (s/n): {Style.RESET_ALL}").lower()
        if again != 's':
            print(f"{Fore.GREEN}¡Hasta luego!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()
