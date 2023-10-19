from selenium import webdriver

# Inicializa o driver do Chrome
driver = webdriver.Chrome()

# Obtém a versão do ChromeDriver
versao_chromedriver = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[
    0]

# Imprime a versão do ChromeDriver
print("Versão do ChromeDriver instalada: " + versao_chromedriver)

# Fecha o driver
driver.quit()
