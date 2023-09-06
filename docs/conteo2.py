from selenium import webdriver
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
#import undetected_chromedriver as uc
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import os

url = "http://epmigpm.epmigraciones.gob.pe:7001/prod-mgr/ui/login#!com.gemalto.ics.rnd.pm.ri.web.ui.view.LoginView"
user = "ftobalaz"
password = "Peru1234!"
path = r'C:\Users\VB\Desktop\docs\docs\msedgedriver.exe'

edge_drive_path = (path)
edge_service = Service(edge_drive_path)
edge_option = Options()

#browser = uc.Chrome(service=edge_service,options=edge_option)  
browser = webdriver.Edge(service=edge_service, options=edge_option) #original
browser.get(url)
wait = WebDriverWait(browser, 50) #asignas valor de esperar hasta 50s por respuesta
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))) # requiere doble () para ser entendido como 1 solo dato

rock = browser.find_element(By.ID, 'com.gemalto.ics.rnd.pm.ri.web.loginpage.form.usernameField')
rock.send_keys(user)
rock = browser.find_element(By.ID, 'com.gemalto.ics.rnd.pm.ri.web.loginpage.form.passwordField')
rock.send_keys(password)
rock.send_keys(Keys.ENTER)
wait = WebDriverWait(browser, 10) #espera
wait.until(EC.visibility_of_element_located((By.ID, 'com.gemalto.ics.rnd.pm.web.panel.MenuPanel.item[com.gemalto.ics.peru.pm.mod.stockmanagement.ui.menu.countdocumentspanel]')))

rock = browser.find_element(By.ID, 'com.gemalto.ics.rnd.pm.web.panel.MenuPanel.item[com.gemalto.ics.peru.pm.mod.stockmanagement.ui.menu.countdocumentspanel]')
rock.send_keys(Keys.ENTER)

selector = "input.v-textfield.v-widget.v-has-width[type='text'][style='width: 200px;']" #funciono
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
rock = browser.find_element(By.CSS_SELECTOR, selector)

folder = os.listdir(r'C:\Users\VB\Desktop\docs\documentos_csv')
folder_csv = [file for file in folder if file.endswith(".csv")] # 
print(f"--- se encontraron {len(folder_csv)} para ingresar datos ---")
BOX = []

for rote in folder_csv:
    cv = os.path.join(r'C:\Users\VB\Desktop\docs\documentos_csv', rote)
    
    with open(cv, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        
        a = ""
        count = 0
        boxes = []
        i = 0 #contador para enviados
        for row in reader:
            tabla = browser.find_element(By.CSS_SELECTOR, "table.v-table-table") #identificamos a la tabla donde se agregara valores
            if row[2] != a:
                a = row[2]
                count = count + 1
                boxes.append(a)
            fila=tabla.find_elements(By.TAG_NAME, "tr")
            filas = len(tabla.find_elements(By.TAG_NAME, "tr"))
            
            rock.send_keys(row[3])
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))) #espera hasta que cargue el dato enviado
            
            while a == "a":
                try:
                    WebDriverWait(browser, 10).until(lambda x: (browser.find_elements(By.CSS_SELECTOR, selector)) == row[3])
                    a = "b"
                except:
                    a = "a"
            
            rock.send_keys(Keys.ENTER) #acaba de ingresar dato nuevo
            i=+1
            """
            try:
                #codigo espera a encontrar nueva tabla y campara su cantidad si es mayor o igual a la anterior
                WebDriverWait(browser, 10).until(lambda x: len(browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")) >= filas)
                fila=browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")
                wait.until(fila[-1]==row[3])
                i = -1
            except: 
                i = i + 1
                print(f"intento: {i}\nse enuentra un error estando el el csv: {rote} con el {row[0]}")
                x = input("hubo un error en la ejecucion, analizar porfa ;')  y luego dar ENTER para reintentar o ctrl+c en path para cancelar\ntambien puede ingresar s para saltar este evento")
                if x == "s":
                    i = -1
            """
            ip=""
            while ip !="a":
                qc=0
                try:
                    wait.until(EC.presence_of_element_located((By.TAG_NAME,"body")))
                    qc=+1
                    print(qc)

                    #este es trabador, dejar comentado que ya funciona!!!!
                    #wait.until(lambda x: browser.find_elements(By.CSS_SELECTOR,"table.v-table-table tr"[-1]==row[3]))
                   # wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "table.v-table-table tr:last-child td.v-table-cell-content div.v-table-cell-wrapper"), row[3]))
                    
                    #wait.until(EC.staleness_of(tabla))
                    #print(qc)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.v-table-table")))
                    qc=+1
                    print(qc)
                    wait.until(lambda x: browser.find_element(By.CSS_SELECTOR, "table.v-table-table") != tabla)
                    qc=+1
                    print(qc)
                    WebDriverWait(browser, 10).until(lambda x: len(browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")) >= filas)
                    qc=+1
                    print(qc)
                    selector_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    qc=+1
                    print(qc)
                    wait.until(EC.visibility_of(selector_element))
                    print("complete !")
                    ip="a"
                    #filax = browser.find_elements(By.CSS_SELECTOR, "table.v-table-table tr")  # Obtener la última fila
                    #print(fila)
                    #fila_text = fila.find_element(By.CSS_SELECTOR, "td.v-table-cell-content div.v-table-cell-wrapper")
                    #print(fila_text)
                    #if fila_text == row[3]:
                    #    i = "a" # El valor coincide, salir del bucle
                    #else:
                    #    i = "" # El valor no coincide, intentar de nuevo
                except:
                    ip=input("no carga tabla ni row, ingresar (a) para no esperar o otra cosa para volver a esperar")
    # Resto del manejo de errores
        wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='v-button v-widget' and @role='button']/span[@class='v-button-wrap']/span[@class='v-button-caption'][text()='Guardar']")))
        boton_guardar = browser.find_element(By.XPATH,"//div[@class='v-button v-widget' and @role='button']/span[@class='v-button-wrap']/span[@class='v-button-caption'][text()='Guardar']")
        #input("-- conteo finalizado, desea guardar?(ENTER): ") 
        boton_guardar.click()
        #esperar hasta que aparezca notificacion de conteo exitoso
        wait=wait = WebDriverWait(browser, 200)
        notificacion = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-Notification.tray.tray-info")))

time.sleep(4)
print(f" --- fin de conteos ---\n las cajas son: {BOX}")
#browser.quit()
