from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


def get_shadow_root(driver: WebDriver, element: any):
    """Get the shadow root of a given element"""
    return driver.execute_script('return arguments[0].shadowRoot', element)

def close_cookie_banner(driver: WebDriver, wait: WebDriverWait, cookie_tag_name: str = 'bahf-cookie-disclaimer-dpl3') -> None:
    """Close the cookie banner"""
    try:
        shadow_host = driver.find_element(By.TAG_NAME, cookie_tag_name)
        cookie_buttons = get_shadow_root(driver, shadow_host).find_elements(By.CSS_SELECTOR, 'button')
        if (cookie_buttons):
            cookie_buttons[0].click()
            wait.until(EC.invisibility_of_element_located((By.TAG_NAME, cookie_tag_name)))
    except Exception as e:
        print(f'\n>>> 🍪 Cookie Banner:\n{e}')