from flask import Flask, render_template
import threading
import requests
from bs4 import BeautifulSoup
from urls import SITE_URLS

app = Flask(__name__)

# cerrojo para sincronizar la escritura en los archivos
file_lock_scraper1 = threading.Lock()
file_lock_scraper2 = threading.Lock()
file_lock_scraper3 = threading.Lock()

# función para guardar datos en un archivo
def save_to_file(data, filename, file_lock, scraper_name):
    with open(filename, 'a', encoding='utf-8') as file:
        for item in data:
            file.write("%s\n" % item)
    print(f"Datos de {scraper_name} guardados exitosamente en {filename}")

# Definir la clase Scraper1
class Scraper1:
    def __init__(self):
        self.name = "Scraper1"

    def scrape(self, url):
        try:
            # Realiza una solicitud HTTP al sitio web
            response = requests.get(url)

            # Verifica si la solicitud fue exitosa 
            if response.status_code == 200:
                # Parsea el contenido HTML de la página web
                soup = BeautifulSoup(response.content, 'html.parser')

                # Encuentra y extrae los datos del sitio web usando BeautifulSoup
                paragraphs = soup.find_all('p')

                # Procesa los datos 
                scraped_data = [paragraph.text for paragraph in paragraphs]

                # Guarda los datos en un archivo usando el cerrojo
                with file_lock_scraper1:
                    save_to_file(scraped_data, f"{self.name}_output.txt", file_lock_scraper1, self.name)

        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir durante el scraping
            print(f"Error al hacer scraping en {url}: {e}")

# clase Scraper2 
class Scraper2:
    def __init__(self):
        self.name = "Scraper2"

    def scrape(self, url):
        try:
            # Realiza una solicitud HTTP al sitio web
            response = requests.get(url)

            # Verifica si la solicitud fue exitosa 
            if response.status_code == 200:
                # Parsea el contenido HTML de la página web
                soup = BeautifulSoup(response.content, 'html.parser')

                # Encuentra y extrae los datos del sitio web usando BeautifulSoup
                paragraphs = soup.find_all('p')

                # Procesamiento de los datos 
                scraped_data = [paragraph.text for paragraph in paragraphs]

                # Guarda los datos en un archivo usando el cerrojo
                with file_lock_scraper2:
                    save_to_file(scraped_data, f"{self.name}_output.txt", file_lock_scraper2, self.name)

        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir durante el scraping
            print(f"Error al hacer scraping en {url}: {e}")

    # Definicon de la clase Scraper3
class Scraper3:
    def __init__(self):
        self.name = "Scraper3"

    def scrape(self, url):
        try:
            # Realiza una solicitud HTTP al sitio web
            response = requests.get(url)

            # Verifica si la solicitud fue exitosa 
            if response.status_code == 200:
                # Parsea el contenido HTML de la página web
                soup = BeautifulSoup(response.content, 'html.parser')

                # Encuentra y extrae los datos  del sitio web usando BeautifulSoup
                paragraphs = soup.find_all('p')

                # Procesamiento de los datos 
                scraped_data = [paragraph.text for paragraph in paragraphs]

                # Guarda los datos en un archivo usando el cerrojo
                with file_lock_scraper3:
                    save_to_file(scraped_data, f"{self.name}_output.txt", file_lock_scraper3, self.name)

        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir durante el scraping
            print(f"Error al hacer scraping en {url}: {e}")

# Función principal para realizar el scraping y servir como frontend utilizando Flask
@app.route('/')
def index():
    # instancias de las clases de scrapers
    scraper1 = Scraper1()
    scraper2 = Scraper2()
    scraper3 = Scraper3()

    # Lista para almacenar los hilos
    threads = []

    # Inicia un hilo para Scraper1
    for url in SITE_URLS[:1]:
        thread = threading.Thread(target=scraper1.scrape, args=(url,))
        threads.append(thread)
        thread.start()

    # Inicia un hilo para Scraper2
    for url in SITE_URLS[1:2]:
        thread = threading.Thread(target=scraper2.scrape, args=(url,))
        threads.append(thread)
        thread.start()

    # Inicia un hilo para Scraper3
    for url in SITE_URLS[2:]:
        thread = threading.Thread(target=scraper3.scrape, args=(url,))
        threads.append(thread)
        thread.start()


    # Espera a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Lee los datos de los archivos
    scraped_data = read_data_from_files()
    return render_template('index.html', data=scraped_data)

# Función para leer los datos de los archivos y devolverlos como un diccionario
def read_data_from_files():
    data = {}
    with open('Scraper1_output.txt', 'r', encoding='utf-8') as file:
        data[SITE_URLS[0]] = [line.strip() for line in file.readlines()]
    with open('Scraper2_output.txt', 'r', encoding='utf-8') as file:
        data[SITE_URLS[1]] = [line.strip() for line in file.readlines()]
    with open('Scraper3_output.txt', 'r', encoding='utf-8') as file:
        data[SITE_URLS[2]] = [line.strip() for line in file.readlines()]  # Aquí también deberías usar la URL correcta para Scraper3
    return data

if __name__ == '__main__':
    app.run(debug=True)
