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

#ingresa a contador

rock = browser.find_element(By.ID, 'com.gemalto.ics.rnd.pm.web.panel.MenuPanel.item[com.gemalto.ics.peru.pm.mod.stockmanagement.ui.menu.countdocumentspanel]')
rock.send_keys(Keys.ENTER)

#boton de guardado: 
# <div tabindex="0" role="button" class="v-button v-widget"><span class="v-button-wrap"><span class="v-button-caption">Guardar</span></span></div>

wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='v-button v-widget' and @role='button']/span[@class='v-button-wrap']/span[@class='v-button-caption'][text()='Guardar']")))
boton_guardar = browser.find_element(By.XPATH,"//div[@class='v-button v-widget' and @role='button']/span[@class='v-button-wrap']/span[@class='v-button-caption'][text()='Guardar']")
boton_guardar.click()
notificacion = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-Notification.tray.tray-info")))
print(notificacion)

# el tiempo de la notificacion no termina hasta que señales otro apartado diferente
#notificacion = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.v-Notification.tray.tray-info")))


#print(f"paso este tiempo desde que aparecio la aerta y desaparece: {tfin}")
time.sleep(5)
