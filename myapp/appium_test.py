from appium import webdriver

# Define the desired capabilities
desired_caps = {
    "platformName": "Android",
    "platformVersion": "9.0",  # Replace with your device's Android version
    "deviceName": "emulator-5554",  # Replace with your device name or emulator ID
    "appPackage": "D:\\work\\ChallegeTradvo\\tradvo_challenge\\apks\\com.intelloware.apkinfo.apk",  # Replace with the app package you're testing
    "automationName": "UiAutomator2"  # Set the automation engine
}

# Initialize the driver
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# Interact with the app (simple example: click a button with resource ID 'btn_login')
try:
    element = driver.find_element_by_id("com.example.myapp:id/btn_login")
    element.click()
    print("Button clicked successfully!")
except Exception as e:
    print(f"Failed to find or click the element: {e}")

# Quit the driver
driver.quit()
