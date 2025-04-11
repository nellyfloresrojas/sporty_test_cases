"""
Utilities for mobile interactions
"""
import logging
import time
from distutils.cmd import Command

from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.script_key import ScriptKey
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from hamcrest import assert_that, equal_to
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)


class TestActions:
    logger = logging.getLogger(__name__)
    locator_name = By.CLASS_NAME
    locator_value = ''

    def __init__(self, context):
        self.context = context

    def find_element(self, locator_name, locator_value, wait_until='visible'):
        if wait_until.lower() == 'clickable':
            self.wait_until_clickable(locator_name, locator_value)
        else:
            self.wait_until_visible(locator_name, locator_value)
        return self.context.driver.find_element(self.locator_name, self.locator_value)

    def set_locator(self, locator_name, locator_value):
        """
        :param element_locator: search the element by its type either CSS, ID, XPATH, TAGNAME, NAME,TEXT OR ACCESSIBILITY_ID.
        """
        self.locator_value = locator_value
        if locator_name == 'CSS':
            self.locator_name = By.CSS_SELECTOR
        elif locator_name == 'ID':
            self.locator_name = By.ID
        elif locator_name == 'XPATH':
            self.locator_name = By.XPATH
        elif locator_name == 'TAG':
            self.locator_name = By.TAG
        elif locator_name == 'NAME':
            self.locator_name = By.NAME
        elif locator_name == 'TEXT':
            self.locator_name = By.XPATH
            self.locator_value = './/*[text()="%s"]' % locator_value
        elif locator_name == 'ACCESSIBILITY_ID':
            self.locator_name = By.ACCESSIBILITY_ID
        elif locator_name == "IOS_CLASS_CHAIN":
            self.locator_name = By.IOS_CLASS_CHAIN
        elif locator_name == "IOS_PREDICATE":
            self.locator_name = By.IOS_PREDICATE
        else:
            self.locator_name = By.CLASS_NAME

    def wait_until_visible(self, locator_name, locator_value):
        self.set_locator(locator_name, locator_value)
        try:
            WebDriverWait(self.context.driver, self.context.wait_time) \
                .until(EC.visibility_of_element_located((self.locator_name, self.locator_value)))

        except ValueError:
            self.logger.info("Element is not visible on the page")

    def wait_until_clickable(self, locator_name, locator_value):
        self.set_locator(locator_name, locator_value)
        try:
            WebDriverWait(self.context.driver, self.context.wait_time) \
                .until(EC.element_to_be_clickable((self.locator_name, self.locator_value)))
        except ValueError:
            self.logger.info("Element is not clickable on the page")

    def handle_alert(self, accept_dismiss_text):
        """
        Handles an alert if exists.
        :param element: 'Accept', 'Dismiss' or 'Text'
        :type element: String
        :return: alert text
        """
        alert_text = ''
        for attempt in range(5):
            try:
                alert = self.switch_to_alert()
                alert_text = alert.text
                if accept_dismiss_text == 'accept':
                    alert.accept()
                elif accept_dismiss_text == 'dismiss':
                    alert.dismiss()
                elif accept_dismiss_text == 'text':
                    logger.info(alert_text)
                else:
                    raise Exception("The parameter passed was not expected. Please review.")
                break
            except Exception:
                alert_text = "No Alert"
                time.sleep(1)
        return alert_text

    def get_element(self, element):
        """
        Call function to get element if the element value is name reference to function
        :param element: element instance or string name reference to function
        :return: element
        """
        if isinstance(element, str):
            return getattr(self, element)()
        else:
            return element

    def clicks(self, *elements):
        """
        Replicate sequential mouse click on list of element
        :param elements: <list>element
        :return: <None>
        """
        for element in elements:
            (getattr(self, element)()).click()

    def sleep(self, seconds):
        """
        :param seconds: the amount of seconds to sleep the thread.
        :type seconds: Integer
        """
        time.sleep(seconds)

    def sleep_wait(self, seconds):
        """
        :param seconds: the amount of seconds to sleep the thread.
        :type seconds: Integer
        """
        time.sleep(seconds)

    def is_element_present(self, element_def, wait_time):
        """
        Evaluate if a given WebElement exist by using locator and value
        :param element_def: WebElement instance or string name reference to function
        :param wait_time: Any integer value
        :return: True/False
        """
        self.skip_on()
        try:
            element = self.retry(element_def, attempt_count=1, time_between_attempts=wait_time)
            found = element is not None
        except BaseException:
            found = False
        finally:
            self.skip_off()
            return found

    def is_skip(self):
        """
        Returns true or false based on skip status
        :return: True / False
        """
        return self.context.skip

    def skip_on(self):
        """
        Turn on skip
        :return: <None>
        """
        self.context.skip = True

    def skip_off(self):
        """
        Turn Off skip
        :return: <None>
        """
        self.context.skip = False

    def retry(self, method, *args, attempt_count, time_between_attempts):
        """
        Retry called function and return it's value if no exception thrown within retry limit
        :param method: Any function
        :param args: Function argument(s)
        :param attempt_count: Any integer value, default = 5
        :param time_between_attempts: Any integer value, default = 5
        :return: Value returned by function call or thrown exception
        """
        return_value = None
        while attempt_count >= 0:
            try:
                return_value = getattr(self, method)(*args)
                break
            except BaseException as base_exception:
                if attempt_count == 0:
                    self.logger.info("Attempt to perform action:" + method + " failed, finally!")
                    raise base_exception
                else:
                    self.sleep(time_between_attempts)
                    self.logger.info("Attempt to perform action:" + method + " failed, retrying...")
            finally:
                attempt_count -= 1
        return return_value

    def step_into(self, step_name):
        """
        Assist to call step by statement like feature file
        :param step_name: <use define> e.g.: I hover over the Shop menu
        :return: <None>
        """
        self.context.execute_steps(self.context.step.step_type.capitalize() + " " + step_name.strip())
        self.context.enable_download()

    def type(self, element, text_to_enter):
        my_element = self.get_element(element)
        assert_that(my_element.is_enabled(), "Element is disable")
        my_element.clear()
        my_element.send_keys(text_to_enter)
        assert_that(
            my_element.get_attribute("value"),
            equal_to(text_to_enter),
            "Fail to set text: " + text_to_enter,
        )

    def tap_outside(self):
        """
        Function to tap outside by coordinates
        """
        actions = TouchAction(self.context.driver)
        actions.tap(None, 116, 307)
        actions.perform()

    def swipe_up(self):
        """Swipe from the page"""
        self.context.driver.execute_script("mobile: swipe", {"direction": "up"})

    def swipe_down(self):
        """Swipe from the page"""
        self.context.driver.execute_script("mobile: swipe", {"direction": "down"})

    def swipe_left(self):
        """Swipe to the left"""
        self.context.driver.execute_script("mobile: swipe", {"direction": "left"})

    def move_by_offset(self):
        """
        Function to movebyoffset
        """
        actions = ActionChains(self.context.driver)
        actions.move_to_element(self.context.driver).perform()

    def scroll_down(self):
        """Swipe from the page"""
        self.context.driver.execute_script("mobile: scroll", {"direction": "down"})

    def scroll_up(self):
        """Swipe from the page"""
        self.context.driver.execute_script("mobile: scroll", {"direction": "up"})


    def execute_script(self, script, *args):
        """
        Synchronously Executes JavaScript in the current window/frame.

        :Args:
         - script: The JavaScript to execute.
         - \\*args: Any applicable arguments for your JavaScript.

        :Usage:
            ::

                driver.execute_script('return document.title;')
        """
        if isinstance(script, ScriptKey):
            try:
                script = self.pinned_scripts[script.id]
            except KeyError:
                raise JavascriptException("Pinned script could not be found")

        converted_args = list(args)
        command = None
        if self.w3c:
            command = Command.W3C_EXECUTE_SCRIPT
        else:
            command = Command.EXECUTE_SCRIPT

        return self.execute(command, {
            'script': script,
            'args': converted_args})['value']