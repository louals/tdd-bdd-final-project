######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa

"""
Web Steps

Steps file for products.feature
"""

import logging

from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions


ID_PREFIX = "product_"


##################################################################
# HOME PAGE
##################################################################

@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL."""
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message."""
    assert message in context.driver.title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    """Check that text is not present on the page."""
    element = context.driver.find_element(By.TAG_NAME, "body")
    assert text_string not in element.text


##################################################################
# INPUT FIELDS
##################################################################

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set the value of a text field."""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Select a value from a dropdown."""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    Select(element).select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Check the selected value in a dropdown."""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    dropdown = Select(element)

    assert dropdown.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Check that a field is empty."""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    assert element.get_attribute("value") == ""


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Check that a field contains specific text."""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    found = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )

    assert found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Change the value of a field."""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    element.clear()
    element.send_keys(text_string)


##################################################################
# BUTTONS
##################################################################

@when('I press the "{button_name}" button')
def step_impl(context, button_name):
    """Press a button on the page."""
    button_id = button_name.lower().replace(" ", "_") + "-btn"

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.element_to_be_clickable(
            (By.ID, button_id)
        )
    )

    element.click()


##################################################################
# MESSAGES
##################################################################

@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check that a message appears somewhere on the page."""

    def message_is_visible(driver):
        element = driver.find_element(By.TAG_NAME, "body")
        return message in element.text

    WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(message_is_visible)


##################################################################
# COPY AND PASTE
##################################################################

@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy a field value into the simulated clipboard."""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    context.clipboard = element.get_attribute("value")

    logging.info(
        "Clipboard contains: %s",
        context.clipboard
    )


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste the simulated clipboard value into a field."""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")

    element = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.presence_of_element_located(
            (By.ID, element_id)
        )
    )

    element.clear()
    element.send_keys(context.clipboard)


##################################################################
# VERIFY TEXT
##################################################################

@then('I should see "{text_string}"')
def step_impl(context, text_string):
    """Verify that specific text exists on the page."""

    def text_is_visible(driver):
        element = driver.find_element(By.TAG_NAME, "body")
        return text_string in element.text

    WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(text_is_visible)