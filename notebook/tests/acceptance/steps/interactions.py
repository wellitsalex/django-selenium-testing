from behave import *
from selenium.webdriver.common.by import By

use_step_matcher('re')


@when('I click on the link with href "(.*)"')
def step_impl(context, link_href):
    link = context.browser.find_element("xpath", f'//a[@href="{link_href}"]')
    link.click()


@when('I enter "(.*)" in the "(.*)" field')
def step_impl(context, content, field_name):
    context.browser.find_element(By.ID, field_name).send_keys(content)


@when('I press the login button')
def step_impl(context):
    context.browser.find_element(By.TAG_NAME, 'button').click()


