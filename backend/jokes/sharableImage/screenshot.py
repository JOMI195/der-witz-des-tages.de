from typing import Optional
import requests
from playwright.sync_api import sync_playwright, Browser, Page


def get_chrome_browser_endpoint() -> Optional[str]:
    """
    Retrieve the Chrome browser WebSocket endpoint for remote debugging.
    """
    try:
        response = requests.get(
            "http://chrome:9222/json/version",
            headers={"Host": "0.0.0.0:9222"},
            timeout=10,
        )
        response.raise_for_status()

        endpoint = response.json()["webSocketDebuggerUrl"]
        return endpoint.replace("0.0.0.0", "chrome")

    except (requests.RequestException, KeyError) as e:
        return None


def capture_screenshot(html_content: str) -> Optional[bytes]:
    """
    Capture a screenshot of the given HTML content.
    """
    try:
        with sync_playwright() as p:
            browser_ws_endpoint = get_chrome_browser_endpoint()

            if not browser_ws_endpoint:
                return None

            browser: Browser = p.chromium.connect_over_cdp(browser_ws_endpoint)
            context = browser.new_context(
                viewport={"width": 1080, "height": 1080},
            )

            try:
                page: Page = context.new_page()
                page.set_content(html_content)
                page.wait_for_timeout(1000)

                image_data = page.screenshot()
                return image_data
            finally:
                browser.close()

    except Exception as e:
        return None
