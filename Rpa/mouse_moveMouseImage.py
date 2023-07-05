import pyautogui as PAG

screenshotIcon = "your_path_to_file"

def locateImage():
    CurrentScreen = PAG.screenshot()
    CurrentScreen.save("your_name_to_save.extension")
    findImage = PAG.locateOnScreen(screenshotIcon, grayscale=False, confidence=0.9)
    print(findImage)
    return(findImage)

def moveMouseToLocation():
    PAG.moveTo(locateImage())
    PAG.click()

moveMouseToLocation()