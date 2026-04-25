import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Scenario data remains the same
test_data = [
    ("standard_user", "secret_sauce", "success"),
    ("locked_out_user", "secret_sauce", "locked_error"),
    ("invalid_user", "wrong_pass", "login_error")
]

@pytest.mark.parametrize("user, pwd, expected", test_data)
def test_authentication_logic(driver, user, pwd, expected):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(pwd)
    driver.find_element(By.ID, "login-button").click()
    
    if expected == "success":
        assert "inventory.html" in driver.current_url
    elif expected == "locked_error":
        error_text = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
        assert "locked out" in error_text.lower()
    else:
        error_text = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
        assert "do not match" in error_text.lower()

def test_cart_functionality(driver):
    """
    STABLE INTEGRATION TEST: Uses Explicit Waits (Industry Standard).
    """
    driver.get("https://www.saucedemo.com/")
    
    # 1. Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # 2. Wait until the 'Add to Cart' button is actually clickable
    wait = WebDriverWait(driver, 15)
    add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
    
    # 3. Action: Click the button
    add_btn.click()
    print("\n[ACTION] Clicked Add to Cart")
    
    # 4. CRITICAL: Wait until the badge actually appears in the DOM and has text '1'
    try:
        # This waits specifically for the element to appear AND contain the text "1"
        badge_present = wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1"))
        
        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "1"
        print("[PASS] Verification: Cart Badge is now '1'")
        
    except Exception as e:
        # Final Debug: If it fails, take a screenshot or print the source
        print(f"[FAIL] Badge did not appear. Current Cart HTML: {driver.find_element(By.ID, 'shopping_cart_container').get_attribute('innerHTML')}")
        raise e

    time.sleep(2)