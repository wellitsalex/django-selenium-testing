from behave import *
from selenium import webdriver

use_step_matcher('re')


@given('I am on the welcome page')
def step_impl(context):
    context.browser = webdriver.Chrome('django_capstone_site\webdriver\chromedriver')
    context.browser.get('http://127.0.0.1:8000/')


@given('I am on the login page')
def step_impl(context):
    context.browser = webdriver.Chrome('django_capstone_site\webdriver\chromedriver')
    context.browser.get('http://127.0.0.1:8000/login/')


@then('I am on the login page')
def step_impl(context):
    expected_url = 'http://127.0.0.1:8000/login/'
    assert context.browser.current_url == expected_url


@then('I am on the welcome page')
def step_impl(context):
    expected_url = 'http://127.0.0.1:8000/'
    assert context.browser.current_url == expected_url


@then('I am on the register page')
def step_impl(context):
    expected_url = 'http://127.0.0.1:8000/register/'
    assert context.browser.current_url == expected_url


@then('I am on the dashboard page')
def step_impl(context):
    expected_url = 'http://127.0.0.1:8000/dashboard/'
    assert context.browser.current_url == expected_url


@then('I am on the login page with next to dashboard')
def step_impl(context):
    expected_url = 'http://127.0.0.1:8000/login/?dashboard-page=/dashboard/'
    assert context.browser.current_url == expected_url


@then('I am on the login page with next to profile')
def step_impl(context):
    expected_url = 'http://127.0.0.1:8000/login/?profile-page=/profile/'
    assert context.browser.current_url == expected_url

