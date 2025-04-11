import logging

from utils.test_actions import TestActions


class StreamerClass(TestActions):

    def __init__(self, context):
        self.context = context

    logger = logging.getLogger(__name__)

    def search_icon(self):
        """
        Selector for the search_icon
        """
        return self.find_element('XPATH', '/html/body/div[1]/div[2]/a[2]')


    def search_txtfield(self):
        """
        Selector for the search field
        """
        return self.find_element('CSS', 'a[data-a-target="tw-input"]')


    def first_search_option(self):
        """
        Selector for the search field first option
        """
        return self.find_element('CSS', '[title="StarCraft II"]')


    def first_streamer(self):
        """
        Selector for the search field first option
        """
        return self.find_element('XPATH', '//*[@id="page-main-content-wrapper"]/div[3]/div/div/div[1]')


    def title_search_phrase(self):
        """
        Selector for the title in search page
        """
        return self.find_element('XPATH', '/html/body/div[1]/main/div[1]/div[1]/div[2]/h1')