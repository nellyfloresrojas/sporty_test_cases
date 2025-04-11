from behave import given, then
from behave import step
from selenium.webdriver.common.by import By
from maps.streamer_class import StreamerClass
import time
import os
from selenium.common.exceptions import TimeoutException


@given("I load the web without login")
def step_impl(context):
    context.driver.get("https://m.twitch.tv/?desktop-redirect=true&lang=en")


@step('I click on search icon')
def step_impl(context):
    NUM_ATTEMPTS, TIME_BETWEEN_ATTEMPTS, success = 2, 2, False
    for attempt in range(NUM_ATTEMPTS):
        try:
            element = context.driver.execute_script("""
                    return document.evaluate(
                        "/html/body/div[1]/div[2]/a[2]",
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null
                    ).singleNodeValue;
                """)
            element.click()
            success = True
            break
        except Exception as e:
            exception_to_raise = e
            StreamerClass(context).sleep_wait(TIME_BETWEEN_ATTEMPTS)


@step("I input '{search}'")
def step_impl(context, search):
    NUM_ATTEMPTS, TIME_BETWEEN_ATTEMPTS, success = 3, 2, False
    for attempt in range(NUM_ATTEMPTS):
        try:
            element = context.driver.execute_script("""
                    return document.evaluate(
                        "/html/body/div[1]/div[1]/div[2]/header/div/div/div/div/input",
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null
                    ).singleNodeValue;
                """)
            element.click()
            element.send_keys(search)
            success = True
            break
        except Exception as e:
            exception_to_raise = e
            StreamerClass(context).sleep_wait(TIME_BETWEEN_ATTEMPTS)

    NUM_ATTEMPTS, TIME_BETWEEN_ATTEMPTS, success = 3, 2, False
    for attempt in range(NUM_ATTEMPTS):
        try:
            search_phrase = context.driver.execute_script("""
                    return document.evaluate(
                        "/html/body/div[1]/main/div/ul/li[1]/a/div",
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null
                    ).singleNodeValue;
                """)
            search_phrase.click()
            chanel = context.driver.execute_script("""
                    return document.evaluate(
                        "/html/body/div[1]/main/div/div/section[1]/div[1]/h2",
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null
                    ).singleNodeValue;
                """)
            context.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", chanel)
            context.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", chanel)
            success = True
            break
        except Exception as e:
            exception_to_raise = e
            StreamerClass(context).sleep_wait(TIME_BETWEEN_ATTEMPTS)


@step('I select one streamer')
def step_impl(context):
    NUM_ATTEMPTS, TIME_BETWEEN_ATTEMPTS, success = 3, 2, False
    for attempt in range(NUM_ATTEMPTS):
        try:
            first_search_option = context.driver.execute_script("""
                    return document.evaluate(
                        "/html/body/div[1]/main/div/div/section[1]/div[2]/button/div",
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null
                    ).singleNodeValue;
                """)
            first_search_option.click()
            success = True
            break
        except Exception as e:
            exception_to_raise = e
            StreamerClass(context).sleep_wait(TIME_BETWEEN_ATTEMPTS)


@then('Verify the streamer page is successfully loaded')
def step_impl(context):
    NUM_ATTEMPTS, TIME_BETWEEN_ATTEMPTS, success = 6, 5, False
    for attempt in range(NUM_ATTEMPTS):
        try:
            element = context.driver.execute_script("""
                    return document.evaluate(
                        "/html/body/div[1]/div[4]/div/div/div/div[2]/div[1]/div[3]/div/div/section/div/div[3]/div[2]/div[2]/div[3]/div/div/div[1]/div/span",
                        document,
                        null,
                        XPathResult.FIRST_ORDERED_NODE_TYPE,
                        null
                    ).singleNodeValue;
                """)
            assert StreamerClass(context).is_element_present(context.driver, element)
            success = True
            break
        except Exception as e:
            exception_to_raise = e
            StreamerClass(context).sleep_wait(TIME_BETWEEN_ATTEMPTS)
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    context.driver.save_screenshot(f"screenshots/mobile_screenshot_{timestamp}.png")