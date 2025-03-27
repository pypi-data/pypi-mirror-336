import time
import sys
import multiprocessing
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import requests
from urllib.parse import urljoin
from urllib.parse import parse_qs

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from channels.testing import ChannelsLiveServerTestCase
from django.test import override_settings

from testing.selenium_helper import SeleniumHelper
from testing.mail import get_outbox, empty_outbox, delete_outbox


# From https://realpython.com/testing-third-party-apis-with-mock-servers/
class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/admin/?page=importsimple":
            self.send_response(requests.codes.not_found)
            self.end_headers()
            return
        content_length = int(self.headers["Content-Length"])
        form = parse_qs(self.rfile.read(content_length).decode("utf-8"))
        if "cmd" in form and form["cmd"][0] == "login":
            self.send_response(requests.codes.ok)
            self.send_header("Set-Cookie", "fish=2000")
            self.end_headers()
            self.wfile.write(
                '<html><head></head><body><input type="hidden" name="formtoken" value="1f2342432j4bn3b237114" /></body></html>'.encode(
                    "utf-8"
                )
            )
        elif "importcontent" in form:
            self.send_response(requests.codes.ok)
            self.end_headers()
            self.wfile.write(
                "<html><head></head><body>Email has been subscribed!</body></html>".encode(
                    "utf-8"
                )
            )
        else:
            self.send_response(requests.codes.not_found)
            self.end_headers()
        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return port


MAIL_STORAGE_NAME = "phplist"

SERVER_PORT = get_free_port()


@override_settings(MAIL_STORAGE_NAME=MAIL_STORAGE_NAME)
@override_settings(EMAIL_BACKEND="testing.mail.EmailBackend")
@override_settings(PHPLIST_BASE_URL="")
class PHPlistTestNotAvailable(SeleniumHelper, ChannelsLiveServerTestCase):
    fixtures = ["initial_documenttemplates.json", "initial_styles.json"]

    @classmethod
    def start_server(cls, port):
        httpd = HTTPServer(("", port), MockServerRequestHandler)
        httpd.serve_forever()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = cls.live_server_url
        driver_data = cls.get_drivers(1)
        cls.driver = driver_data["drivers"][0]
        cls.client = driver_data["clients"][0]
        cls.driver.implicitly_wait(driver_data["wait_time"])
        cls.wait_time = driver_data["wait_time"]
        cls.server = multiprocessing.Process(
            target=cls.start_server, args=(SERVER_PORT,)
        )
        cls.server.daemon = True
        cls.server.start()

    def tearDown(self):
        self.driver.execute_script("window.localStorage.clear()")
        self.driver.execute_script("window.sessionStorage.clear()")
        super().tearDown()
        empty_outbox(MAIL_STORAGE_NAME)
        if "coverage" in sys.modules.keys():
            # Cool down
            time.sleep(self.wait_time / 3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server.terminate()
        delete_outbox(MAIL_STORAGE_NAME)
        super().tearDownClass()

    def test_signup_yes(self):
        self.signup(self.driver, True, False, False)

    def test_signup_no(self):
        self.signup(self.driver, False, False, False)

    def assertInfoAlert(self, message):
        i = 0
        message_found = False
        while i < 100:
            i = i + 1
            try:
                if (
                    self.driver.find_element(
                        By.CSS_SELECTOR,
                        "body #alerts-outer-wrapper .alerts-info",
                    ).text
                    == message
                ):
                    message_found = True
                    break
                else:
                    time.sleep(0.1)
                    continue
            except StaleElementReferenceException:
                time.sleep(0.1)
                continue
        self.assertTrue(message_found)

    def signup(self, driver, list=False, signed_up=False, setting=False):
        driver.get(urljoin(self.base_url, "/account/sign-up/"))

        driver.find_element(By.ID, "id-username").send_keys(
            f"username_{list}_{signed_up}_{setting}"
        )
        driver.find_element(By.ID, "id-password1").send_keys("password")
        driver.find_element(By.ID, "id-password2").send_keys("password")
        driver.find_element(By.ID, "id-email").send_keys(
            f"my.no.{list}.{signed_up}.{setting}@email.com"
        )
        driver.find_element(By.ID, "signup-submit").click()
        time.sleep(1)
        signup_link = self.find_urls(get_outbox(MAIL_STORAGE_NAME)[-1].body)[0]
        driver.get(signup_link)
        driver.find_element(By.ID, "terms-check").click()
        driver.find_element(By.ID, "test-check").click()
        if list:
            answer = "yes"
        else:
            answer = "no"
        driver.find_element(
            By.CSS_SELECTOR,
            'input[name="emaillist"][value="{}"]'.format(answer),
        ).click()
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        if signed_up:
            self.assertInfoAlert("Subscribed to email list")
        WebDriverWait(driver, self.wait_time).until(
            EC.staleness_of(submit_button)
        )
        self.assertEqual(
            driver.find_element(By.CSS_SELECTOR, ".fw-contents h1").text,
            "Thanks for verifying!",
        )


@override_settings(MAIL_STORAGE_NAME=MAIL_STORAGE_NAME)
@override_settings(EMAIL_BACKEND="testing.mail.EmailBackend")
@override_settings(PHPLIST_BASE_URL="http://localhost:{}/".format(SERVER_PORT))
@override_settings(PHPLIST_LOGIN="login")
@override_settings(PHPLIST_PASSWORD="password")
@override_settings(PHPLIST_LIST_ID="1")
class PHPlistTestAvailable(SeleniumHelper, ChannelsLiveServerTestCase):
    fixtures = ["initial_documenttemplates.json", "initial_styles.json"]

    @classmethod
    def start_server(cls, port):
        httpd = HTTPServer(("", port), MockServerRequestHandler)
        httpd.serve_forever()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = cls.live_server_url
        driver_data = cls.get_drivers(1)
        cls.driver = driver_data["drivers"][0]
        cls.client = driver_data["clients"][0]
        cls.driver.implicitly_wait(driver_data["wait_time"])
        cls.wait_time = driver_data["wait_time"]
        cls.server = multiprocessing.Process(
            target=cls.start_server, args=(SERVER_PORT,)
        )
        cls.server.daemon = True
        cls.server.start()

    def tearDown(self):
        self.driver.execute_script("window.localStorage.clear()")
        self.driver.execute_script("window.sessionStorage.clear()")
        super().tearDown()
        empty_outbox(MAIL_STORAGE_NAME)
        if "coverage" in sys.modules.keys():
            # Cool down
            time.sleep(self.wait_time / 3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server.terminate()
        delete_outbox(MAIL_STORAGE_NAME)
        super().tearDownClass()

    def test_signup_no(self):
        self.signup(self.driver, False, False, True)

    def test_signup_yes(self):
        self.signup(self.driver, True, True, True)

    def assertInfoAlert(self, message):
        i = 0
        message_found = False
        while i < 100:
            i = i + 1
            try:
                if (
                    self.driver.find_element(
                        By.CSS_SELECTOR,
                        "body #alerts-outer-wrapper .alerts-info",
                    ).text
                    == message
                ):
                    message_found = True
                    break
                else:
                    time.sleep(0.1)
                    continue
            except StaleElementReferenceException:
                time.sleep(0.1)
                continue
        self.assertTrue(message_found)

    def signup(self, driver, list=False, signed_up=False, setting=False):
        driver.get(urljoin(self.base_url, "/account/sign-up/"))

        driver.find_element(By.ID, "id-username").send_keys(
            f"username_{list}_{signed_up}_{setting}"
        )
        driver.find_element(By.ID, "id-password1").send_keys("password")
        driver.find_element(By.ID, "id-password2").send_keys("password")
        driver.find_element(By.ID, "id-email").send_keys(
            f"my.no.{list}.{signed_up}.{setting}@email.com"
        )
        driver.find_element(By.ID, "signup-submit").click()
        time.sleep(1)
        signup_link = self.find_urls(get_outbox(MAIL_STORAGE_NAME)[-1].body)[0]
        driver.get(signup_link)
        driver.find_element(By.ID, "terms-check").click()
        driver.find_element(By.ID, "test-check").click()
        if list:
            answer = "yes"
        else:
            answer = "no"
        driver.find_element(
            By.CSS_SELECTOR,
            'input[name="emaillist"][value="{}"]'.format(answer),
        ).click()
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        if signed_up:
            self.assertInfoAlert("Subscribed to email list")
        WebDriverWait(driver, self.wait_time).until(
            EC.staleness_of(submit_button)
        )
        self.assertEqual(
            driver.find_element(By.CSS_SELECTOR, ".fw-contents h1").text,
            "Thanks for verifying!",
        )
