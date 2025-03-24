from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capture_screenshot(url, output_path="screenshot.png"):
    # Set up WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without opening a browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open URL and take screenshot
    driver.get(url)
    driver.save_screenshot(output_path)
    driver.quit()

    print(f"✅ Screenshot saved at {output_path}")

# Example usage
capture_screenshot("https://www.google.com")
