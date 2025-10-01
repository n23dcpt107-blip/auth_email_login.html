import time
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "file://" + str((Path(__file__).resolve().parents[1] / "auth_email_login.html").as_posix())

def shot(driver, name):
    out = Path(__file__).resolve().parents[1] / "screenshots"
    out.mkdir(exist_ok=True)
    driver.save_screenshot(str(out / f"{name}.png"))

@pytest.fixture(scope="module")
def driver():
    opts = Options()
    # opts.add_argument("--headless=new")  # Bật nếu cần chạy headless
    opts.add_argument("--window-size=1200,900")
    service = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=opts)
    yield d
    d.quit()

def open_form(d):
    d.get(BASE_URL)
    WebDriverWait(d, 5).until(EC.presence_of_element_located((By.ID, "login")))

def msg_text(d):
    return d.find_element(By.ID, "message").text.strip()

def fill_and_submit(d, email="", pwd="", captcha=False):
    d.find_element(By.ID, "email").clear()
    d.find_element(By.ID, "email").send_keys(email)
    d.find_element(By.ID, "pwd").clear()
    d.find_element(By.ID, "pwd").send_keys(pwd)
    cb = d.find_element(By.ID, "captcha")
    if captcha and not cb.is_selected():
        cb.click()
    if not captcha and cb.is_selected():
        cb.click()
    d.find_element(By.ID, "login").click()

def wait_hash(d, expected, timeout=2):
    WebDriverWait(d, timeout).until(lambda x: x.current_url.endswith(expected))

def test_success_with_captcha(driver):
    open_form(driver)
    fill_and_submit(driver, "friend@example.com", "Passw0rd!", captcha=True)
    WebDriverWait(driver, 3).until(lambda d: "successfully" in msg_text(d))
    wait_hash(driver, "#/home")
    shot(driver, "F-TC01_success")

def test_wrong_password(driver):
    open_form(driver)
    fill_and_submit(driver, "friend@example.com", "wrong", captcha=True)
    WebDriverWait(driver, 3).until(lambda d: "Incorrect email or password." in msg_text(d))
    assert not driver.current_url.endswith("#/home")
    shot(driver, "F-TC02_wrong_pwd")

@pytest.mark.parametrize("email,pwd,field_err_id,err_text", [
    ("", "Passw0rd!", "emailError", "Please enter email."),
    ("friend@example.com", "", "pwdError", "Please enter password.")
])
def test_empty_fields(driver, email, pwd, field_err_id, err_text):
    open_form(driver)
    fill_and_submit(driver, email, pwd, captcha=True)
    WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.ID, field_err_id), err_text))
    assert "Fix the highlighted errors." in msg_text(driver)
    shot(driver, f"F-TC03_empty_{field_err_id}")

def test_invalid_email_format(driver):
    open_form(driver)
    fill_and_submit(driver, "abc@", "Passw0rd!", captcha=True)
    WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.ID, "emailError"), "Invalid email format."))
    shot(driver, "F-TC04_invalid_email")

def test_captcha_required(driver):
    open_form(driver)
    fill_and_submit(driver, "friend@example.com", "Passw0rd!", captcha=False)
    WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.ID, "captchaError"), "Please verify captcha."))
    assert not driver.current_url.endswith("#/home")
    shot(driver, "F-TC05_captcha_required")

def test_toggle_show_password(driver):
    open_form(driver)
    driver.find_element(By.ID, "pwd").send_keys("abc")
    t = driver.find_element(By.ID, "toggle")
    assert driver.find_element(By.ID, "pwd").get_attribute("type") == "password"
    t.click()
    WebDriverWait(driver, 2).until(lambda d: d.find_element(By.ID, "pwd").get_attribute("type") == "text")
    t.click()
    WebDriverWait(driver, 2).until(lambda d: d.find_element(By.ID, "pwd").get_attribute("type") == "password")
    shot(driver, "F-TC06_toggle_eye")
