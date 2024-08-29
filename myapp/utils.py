import subprocess
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
from appium.options.android import UiAutomator2Options

# Launch Android Emulator
def launch_emulator(emulator_name):
    subprocess.Popen(f"emulator -avd {emulator_name} -read-only -no-accel -gpu swiftshader_indirect", shell=True)

# Start Appium Session
def start_appium_session(apk_path):
    desired_caps = {
        "platformName": "Android",
        "deviceName": "emulator-5554",  # Change as needed
        "app": apk_path,
        "automationName": "UiAutomator2",
    }
    options = UiAutomator2Options()
    options.load_capabilities(desired_caps)

    driver = webdriver.Remote("http://localhost:4723/wd/hub" , options=options)
    return driver

# Capture UI Hierarchy and Screen
def capture_initial_state(driver):
    driver.get_screenshot_as_file("initial_screen.png")
    initial_hierarchy = driver.page_source
    return initial_hierarchy

# Click the First Button on the Screen
def click_first_button(driver):
    clickable_elements = driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
    if clickable_elements:
        clickable_elements[0].click()
    else:
        print("No clickable elements found on the screen.")

# Capture New Screen State
def capture_new_state(driver):
    driver.get_screenshot_as_file("new_screen.png")
    new_hierarchy = driver.page_source
    return new_hierarchy

# Assess Whether the Screen Changed
def assess_screen_change(initial_hierarchy, new_hierarchy):
    return initial_hierarchy != new_hierarchy

# Record the Video of the Test
def record_video():
    subprocess.Popen("adb shell screenrecord /sdcard/test_video.mp4", shell=True)

def stop_video():
    subprocess.Popen("adb shell pkill -l2 screenrecord", shell=True)
    subprocess.Popen("adb pull /sdcard/test_video.mp4", shell=True)

# Save Test Results
def save_test_results(app, screen_changed, new_hierarchy):
    app.first_screen_screenshot_path = "initial_screen.png"
    app.second_screen_screenshot_path = "new_screen.png"
    app.video_recording_path = "test_video.mp4"
    app.ui_hierarchy = new_hierarchy
    app.screen_changed = screen_changed
    app.save()
    