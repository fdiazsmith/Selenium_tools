import asyncio
from pyppeteer import launch
from  pyppeteer import chromium_downloader

chromium_downloader.download_chromium()
async def take_screenshot(url, resolution, filename):
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.setViewport({'width': resolution[0], 'height': resolution[1]})
    await page.goto(url)
    await page.screenshot({'path': filename})
    await browser.close()

async def main():
    url = 'http://localhost:8000/'
    resolutions = [(1920, 1080), (1366, 768), (1280, 720)]

    for resolution in resolutions:
        filename = f'screenshot_{resolution[0]}x{resolution[1]}.png'
        await take_screenshot(url, resolution, filename)

asyncio.get_event_loop().run_until_complete(main())
