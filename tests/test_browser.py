from mock import patch
import os
import shutil
from selenium import webdriver
import tempfile
from unittest import TestCase

import bok_choy.browser
from .pages import ButtonPage, JavaScriptPage


class TestBrowser(TestCase):

    @patch.dict(os.environ, {'SELENIUM_BROWSER': 'firefox'})
    def test_local_browser(self):
        browser = bok_choy.browser.browser()
        self.addCleanup(browser.quit)
        self.assertIsInstance(browser, webdriver.Firefox)

    @patch.dict(os.environ, {'SELENIUM_BROWSER': 'invalid'})
    def test_invalid_browser_name(self):
        with self.assertRaises(bok_choy.browser.BrowserConfigError):
            bok_choy.browser.browser()


class TestSaveFiles(TestCase):

    def setUp(self):
        super(TestSaveFiles, self).setUp()

        # Create a temp directory to save the files to
        tempdir_path = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(tempdir_path))

        # Take a screenshot of a page
        browser = bok_choy.browser.browser()
        self.addCleanup(browser.quit)
        self.browser = browser
        self.tempdir_path = tempdir_path

    def test_save_screenshot(self):
        browser = self.browser
        tempdir_path = self.tempdir_path

        # Configure the screenshot directory using an environment variable
        os.environ['SCREENSHOT_DIR'] = tempdir_path
        ButtonPage(browser).visit()
        bok_choy.browser.save_screenshot(browser, 'button_page')

        # Check that the file was created
        expected_file = os.path.join(tempdir_path, 'button_page.png')
        self.assertTrue(os.path.isfile(expected_file))

        # Check that the file is not empty
        self.assertGreater(os.stat(expected_file).st_size, 100)

    def test_save_driver_logs(self):
        browser = self.browser
        tempdir_path = self.tempdir_path

        # Configure the driver log directory using an environment variable
        os.environ['SELENIUM_DRIVER_LOG_DIR'] = tempdir_path
        JavaScriptPage(browser).visit()
        bok_choy.browser.save_driver_logs(browser, 'js_page')

        # Check that the files were created.
        # Note that the 'client' and 'server' log files will be empty.
        log_types = ['browser', 'driver', 'client', 'server']
        for log_type in log_types:
            expected_file = os.path.join(tempdir_path, 'js_page_{}.log'.format(log_type))
            self.assertTrue(os.path.isfile(expected_file))

    def test_save_source(self):
        browser = self.browser
        tempdir_path = self.tempdir_path

        # Configure the saved source directory using an environment variable
        os.environ['SAVED_SOURCE_DIR'] = tempdir_path
        ButtonPage(browser).visit()
        bok_choy.browser.save_source(browser, 'button_page')

        # Check that the file was created
        expected_file = os.path.join(tempdir_path, 'button_page.html')
        self.assertTrue(os.path.isfile(expected_file))

        # Check that the file is not empty
        self.assertGreater(os.stat(expected_file).st_size, 100)
