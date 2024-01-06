V1
---------------
import requests
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# Generate a random username and password
username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

print(f"Username: {username}")
print(f"Password: {password}")

# Initialize Mail.tm API
response = requests.get('https://api.mail.tm/domains')
domains = response.json()['hydra:member']
domain = domains[0]['domain']

# Create an email address with the random username and fetched domain
email_address = f"{username}@{domain}"
print(f"Email Address: {email_address}")

# Create an account
account_data = {
    "address": email_address,
    "password": password
}
response = requests.post('https://api.mail.tm/accounts', json=account_data)
account = response.json()

# Get the token
token_data = {
    "address": account['address'],
    "password": account_data['password']
}
response = requests.post('https://api.mail.tm/token', json=token_data)
mailtm_token = response.json()['token']

headers = {
    'Authorization': f'Bearer {mailtm_token}'
}

# Initialize Selenium WebDriver with undetected-chromedriver
driver = uc.Chrome()

# Navigate to the website
driver.get('https://www.phind.com/search?home=true')

# Click on "Sign In"
sign_in_button = driver.find_element(By.XPATH, '//button[text()="Sign In"]')
sign_in_button.click()

# Wait for 4 seconds
WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.NAME, 'email')))

# Input the email address
email_input = driver.find_element(By.NAME, 'email')
email_input.send_keys(email_address)

# Click on "Sign In with Email"
sign_in_with_email_button = driver.find_element(By.ID, 'submitButton')
sign_in_with_email_button.click()

# Fetch the message list
time.sleep(5)
driver.get('https://api.mail.tm/messages')

# Locate the confirmation email and extract the confirmation link
confirmation_link = None
for message in driver.find_elements(By.CSS_SELECTOR, "pre"):
    if 'confirmation' in message.text:
        confirmation_link = message.text  # or message.get_attribute('innerHTML') if the link is in the HTML content
        break

# Navigate to the confirmation link
if confirmation_link:
    driver.get(confirmation_link)

# Close the browser
driver.quit()