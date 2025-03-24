from typing import Any, Generator
from contextlib import contextmanager

from ..decorator import chainable
from ..middleware import MiddlewareBase


class SeleniumMiddleware(MiddlewareBase):
    '''
    SeleniumMiddleware - middleware for using Selenium.

    For downloading ChromeDriver and Chrome executable:
    https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
    '''

    name = 'selenium'
    dependency = ['selenium', 'selenium_stealth', 'fake_useragent']

    _config: dict[str, Any] = {}

    @classmethod
    def config(
        cls,
        *,
        binary_location: str | None = None,
        headless: bool | None = True,
        option_arguments: list | None = None,
        proxy: str | None = None,
        stealth_options: dict | None = None,
        ua_options: dict | None = None,
        webdriver_location: str | None = None,
    ) -> type['SeleniumMiddleware']:
        if stealth_options is None:
            stealth_options = {}
        if ua_options is None:
            ua_options = {}

        cls._config = {
            'binary_location': binary_location,
            'headless': headless,
            'option_arguments': option_arguments,
            'proxy': proxy,
            'stealth_options': stealth_options,
            'ua_options': ua_options,
            'webdriver_location': webdriver_location,
        }

        return cls

    @chainable
    async def create(self) -> 'SeleniumMiddleware':
        try:
            from selenium import webdriver
            from selenium_stealth import stealth
            from fake_useragent import UserAgent
        except ImportError:
            self.log('can not initialize selenium')
        else:

            @contextmanager
            def open_selenium_session() -> (
                Generator[webdriver.Chrome, None, None]
            ):

                proxy = self._config['proxy']
                binary_location = self._config['binary_location']
                webdriver_location = self._config['webdriver_location']
                option_arguments = self._config['option_arguments']
                ua_options = self._config['ua_options']
                stealth_options = self._config['stealth_options']

                user_agent: str = UserAgent(
                    platforms='desktop', **ua_options
                ).random

                options = webdriver.ChromeOptions()
                service = webdriver.ChromeService(
                    executable_path=webdriver_location
                )

                if binary_location:
                    options.binary_location = binary_location

                if self._config['headless']:
                    options.add_argument('--headless')

                if proxy is not None:
                    options.add_argument(f'--proxy-server={proxy}')

                options.add_argument('--no-sandbox')
                options.add_argument('--disable-gpu')
                options.add_argument('blink-settings=imagesEnabled=false')
                options.add_argument(user_agent)
                options.add_argument('--disable-plugins')
                options.add_argument('--disable-popup-blocking')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('start-maximized')
                options.add_argument('--deny-permission-prompts')
                options.add_experimental_option(
                    'prefs',
                    {'profile.default_content_settings.geolocation': 2},
                )
                options.add_experimental_option(
                    'excludeSwitches', ['enable-automation']
                )
                options.add_experimental_option(
                    'useAutomationExtension', False
                )

                if isinstance(option_arguments, list):
                    for opt in option_arguments:
                        options.add_argument(opt)

                session = webdriver.Chrome(options=options, service=service)

                stealth(
                    session,
                    user_agent=user_agent,
                    languages=['en-US', 'en'],
                    vendor='Google Inc.',
                    platform='Win32',
                    webgl_vendor='Intel Inc.',
                    renderer='Intel Iris OpenGL Engine',
                    fix_hairline=False,
                    run_on_insecure_origins=False,
                    **stealth_options,
                )

                self.log('Selenium session initialized')

                yield session

                session.quit()

                self.log('Selenium session closed')

            self.bind_object(SeleniumMiddleware.name, open_selenium_session)

    @chainable
    async def destroy(self) -> 'SeleniumMiddleware': ...
