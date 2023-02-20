"""logic to take screenshot of website"""
import base64
import io
from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager



class ScreenshotService():
    """Class control logic to take screenshot
    """
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        path_driver = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(path_driver, options = options)

    def screenshot_first_page(self, url):
        """Get the first screen shot of website

        Args:
            url (str): url of website

        Returns:
            image (base64): 1st screenshot of website
        """
        self.driver.get(url)
        return self.driver.get_screenshot_as_png()

    def screenshot_entire_page(self, url):
        """Get screenshot of entire website

        Args:
            url (str): url of website

        Returns:
            image (base64): screenshot of entire website
        """
        self.driver.get(url)
        total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_height = self.driver.execute_script("return window.innerHeight")
        self.driver.execute_script("window.scrollTo(0, 0)")
        rectangles = []

        y_start = 0
        while y_start < total_height:
            x_start = 0
            rectangles.append((x_start, y_start))
            y_start = y_start + viewport_height
        stitched_image = None
        previous = None

        # This value indicates if is the first part of the screenshot, or it is the rest of the screenshot
        init_canvas = True
        # Get the screenshot and save the dimensions of the image, this will be useful for create a
        # correct canvas with correct dimensions
        # and not show images with a wrong size or cut
        size_screenshot = self.__get_screen_size()
        # Get temporary sum of height of the total pages
        height_canvas = size_screenshot['height'] * len(rectangles)

        # Compare if the screenshot it's only one part and assign the correct dimensions of the screenshot size
        # Or assign the height of the total screenshot
        # Assign the height of the total screenshot at canvas
        stitched_image = Image.new(
                'RGB', (size_screenshot['width'], height_canvas))

        # This constant is used top offset the image in the canvas
        jump = round(size_screenshot['height'])
        # With take multiple screenshots this value is used to adjust the position of the image in the canvas
        # This value know update every time the screenshot is taken

        for rectangle in rectangles:
            if previous is not None:
                self.driver.execute_script(f"window.scrollTo({rectangle[0]}, {rectangle[1]})")

            binary_screenshot = self.driver.get_screenshot_as_png()
            screenshot = Image.open(io.BytesIO(binary_screenshot))
            offset = (rectangle[0], rectangle[1])

            stitched_image.paste(screenshot, offset)
            previous = rectangle
        output = io.BytesIO()
        stitched_image.save(output, format='PNG')
        return output.getvalue()

    # Take temporary screenshot of the web page to get the size of the image
    def __get_screen_size(self) -> dict:
        self.driver.get_screenshot_as_file('screenshot.png')
        image = Image.open('screenshot.png')
        width, height = image.size

        return {'width': width, 'height': height}

if __name__ == "__main__":
    screnshotservice = ScreenshotService()
    image = screnshotservice.screenshot_first_page(
        "https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi")
    base64_decoded = base64.b64decode(image)
    image = Image.open(io.BytesIO(base64_decoded))
    image.show()
    