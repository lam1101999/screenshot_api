"""Router for getting screenshot of website"""

from fastapi import APIRouter, Response
from service.screenshot_service import ScreenshotService

screenshot = ScreenshotService()

router = APIRouter()
@router.get("/firstpageget/")
async def screenshot_first_page_get(url:str):
    """Routing for taking the first screen shot

    Args:
        url (str): _description_

    Returns:
        _type_: _description_
    """
    image = screenshot.screenshot_first_page(url)
    response = Response(image, media_type = "image/png")
    return response

@router.get("/entirepage/")
async def screenshot_entire_page(url:str):
    """routing for taking entire screenshot

    Args:
        url (str): _description_

    Returns:
        _type_: _description_
    """
    image =  screenshot.screenshot_entire_page(url)
    response = Response(image, media_type = "image/png")
    return response
    