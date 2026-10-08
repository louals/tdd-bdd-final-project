# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
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

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel
"""

import os
import logging
import unittest
from decimal import Decimal

from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(
            name="Fedora",
            description="A red hat",
            price=12.50,
            available=True,
            category=Category.CLOTHS,
        )

        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])

        product = ProductFactory()
        product.id = None
        product.create()

        self.assertIsNotNone(product.id)

        products = Product.all()
        self.assertEqual(len(products), 1)

        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    # Q2 - READ
    def test_read_a_product(self):
        """It should Read a Product from the database"""
        product = ProductFactory()
        product.id = None
        product.create()

        found_product = Product.find(product.id)

        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(Decimal(found_product.price), product.price)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.category, product.category)

    # Q3 - UPDATE
    def test_update_a_product(self):
        """It should Update a Product in the database"""
        product = ProductFactory()
        product.id = None
        product.create()

        product.name = "Updated Product"
        product.description = "Updated description"
        product.price = 99.99
        product.available = False
        product.category = Category.TOOLS

        product.update()

        found_product = Product.find(product.id)

        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.name, "Updated Product")
        self.assertEqual(found_product.description, "Updated description")
        self.assertEqual(Decimal(found_product.price), Decimal("99.99"))
        self.assertFalse(found_product.available)
        self.assertEqual(found_product.category, Category.TOOLS)

    # Q4 - DELETE
    def test_delete_a_product(self):
        """It should Delete a Product from the database"""
        product = ProductFactory()
        product.id = None
        product.create()

        product_id = product.id

        product.delete()

        found_product = Product.find(product_id)

        self.assertIsNone(found_product)

    # Q5 - LIST ALL
    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = ProductFactory.create_batch(5)

        for product in products:
            product.id = None
            product.create()

        found_products = Product.all()

        self.assertEqual(len(found_products), 5)

    # Q6 - FIND BY NAME
    def test_find_by_name(self):
        """It should Find Products by name"""
        product = ProductFactory(name="Hat")
        product.id = None
        product.create()

        products = Product.find_by_name("Hat").all()

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Hat")

    # Q7 - FIND BY CATEGORY
    def test_find_by_category(self):
        """It should Find Products by category"""
        product = ProductFactory(category=Category.FOOD)
        product.id = None
        product.create()

        products = Product.find_by_category(Category.FOOD).all()

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].category, Category.FOOD)

    # Q8 - FIND BY AVAILABILITY
    def test_find_by_availability(self):
        """It should Find Products by availability"""
        product = ProductFactory(available=True)
        product.id = None
        product.create()

        products = Product.find_by_availability(True).all()

        self.assertEqual(len(products), 1)
        self.assertTrue(products[0].available)


if __name__ == "__main__":
    unittest.main()