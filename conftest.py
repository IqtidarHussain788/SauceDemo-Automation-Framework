import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    """
    Setup: Initializes Chrome with optimized settings for university laboratory environments.
    Teardown: Automatically closes the session after each test case execution.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    # Initialize the driver using WebDriver Manager (no need to manually download chromedriver.exe)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10) # Safety wait for slow internet connections
    
    yield driver
    
    # This ensures the browser closes even if a test fails
    driver.quit()