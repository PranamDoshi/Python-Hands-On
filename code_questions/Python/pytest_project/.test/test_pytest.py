import sys
import os
import re

sys.path.append(os.getcwd())

from mytest import test_inventory
import autopep8
from xml.etree import ElementTree
import pytest
import inspect


@pytest.fixture
def inspect_get_sourcecode(obj):
    source_without_comment = re.sub(r"\s*\#.*", " ", inspect.getsource(obj))
    if inspect.getdoc(obj):
        return inspect.cleandoc(source_without_comment).replace(inspect.getdoc(obj), "").replace('"""', "")
    return source_without_comment


@pytest.fixture
def get_xml_root_element(source):
    xml = ElementTree.parse(source)
    root = xml.getroot()
    return root[0]


@pytest.mark.parametrize("obj, expected",
                         [(test_inventory.TestingInventoryCreation.test_creating_empty_inventory,
                           [r"MobileInventory\(\)", r"(assert.+==\s*\{\}|assert\s*\{\}\s*==.+)"]),
                          (test_inventory.TestingInventoryCreation.test_creating_specified_inventory,
                           [
                               r"\{\"iPhone\sModel\sX\"\:\s100,[\n\s]*\"Xiaomi\sModel\sY\"\:\s1000,[\n\s]*\"Nokia\sModel\sZ\"\:\s25\}",
                               r"(assert.+==\s*\{\"iPhone\sModel\sX\"\:\s100,[\n\s]*\"Xiaomi\sModel\sY\"\:\s1000,[\n\s]*\"Nokia\sModel\sZ\"\:\s25\}|assert\s*\{\"iPhone\sModel\sX\"\:\s100,[\n\s]*\"Xiaomi\sModel\sY\"\:\s1000,[\n\s]*\"Nokia\sModel\sZ\"\:\s25\}\s*==.+)"
                           ]),
                          (test_inventory.TestingInventoryCreation.test_creating_inventory_with_list,
                           [
                               r"\[\"iPhone\sModel\sX\",\s\"Xiaomi\sModel\sY\",\s\"Nokia\sModel\sZ\"\]",
                               r"pytest\.raises\(TypeError",
                               r"(assert.+==\s*\"Input\sinventory\smust\sbe\sa\sdictionary\"|assert\s*\"Input\sinventory\smust\sbe\sa\sdictionary\"\s*==.+)"
                           ]),
                          (test_inventory.TestingInventoryCreation.test_creating_inventory_with_numeric_keys,
                           [
                               r"\{1\:\s\"iPhone\sModel\sX\",[\n\s]*2\:\s\"Xiaomi\sModel\sY\",[\n\s]*3\:\s\"Nokia\sModel\sZ\"\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"Mobile\smodel\sname\smust\sbe\sa\sstring\"|assert\s*\"Mobile\smodel\sname\smust\sbe\sa\sstring\"\s*==.+)"
                           ]),
                          (test_inventory.TestingInventoryCreation.test_creating_inventory_with_nonnumeric_values,
                           [
                               r"\{\"iPhone\sModel\sX\"\:\s\"100\",[\n\s]*\"Xiaomi\sModel\sY\"\:\s\"1000\",[\n\s]*\"Nokia\sModel\sZ\"\:\s\"25\"\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"|assert\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"\s*==.+)"
                           ]),
                          (test_inventory.TestingInventoryCreation.test_creating_inventory_with_negative_value,
                           [
                               r"\{\"iPhone\sModel\sX\"\:\s-45,[\n\s]*\"Xiaomi\sModel\sY\"\:\s200,[\n\s]*\"Nokia\sModel\sZ\"\:\s25\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"|assert\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventoryAddStock.setup_class,
                           [
                               r"@classmethod",
                               r"\{\"iPhone\sModel\sX\"\:\s100,[\n\s]*\"Xiaomi\sModel\sY\"\:\s1000,[\n\s]*\"Nokia\sModel\sZ\"\:\s25\}"
                           ]),
                          (test_inventory.TestInventoryAddStock.test_add_new_stock_as_dict,
                           [
                               r"add_stock\(",
                               r"\{\"iPhone\sModel\sX\"\:\s50,[\n\s]*\"Xiaomi\sModel\sY\"\:\s2000,[\n\s]*\"Nokia\sModel\sA\"\:\s10\}",
                               r"(assert.+==\s*\{\"iPhone\sModel\sX\"\:\s150,[\n\s]*\"Xiaomi\sModel\sY\"\:\s3000,[\n\s]*\"Nokia\sModel\sZ\"\:\s25,[\n\s]*\"Nokia\sModel\sA\"\:\s10\}|assert\s*\{\"iPhone\sModel\sX\"\:\s150,[\n\s]*\"Xiaomi\sModel\sY\"\:\s3000,[\n\s]*\"Nokia\sModel\sZ\"\:\s25,[\n\s]*\"Nokia\sModel\sA\"\:\s10\}\s*==.+)"
                           ]),
                          (test_inventory.TestInventoryAddStock.test_add_new_stock_as_list,
                           [
                               r"add_stock\(",
                               r"pytest\.raises\(TypeError",
                               r"\[\"iPhone\sModel\sX\",\s\"Xiaomi\sModel\sY\",\s\"Nokia\sModel\sZ\"\]",
                               r"(assert.+==\s*\"Input\sstock\smust\sbe\sa\sdictionary\"|assert\s*\"Input\sstock\smust\sbe\sa\sdictionary\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventoryAddStock.test_add_new_stock_with_numeric_keys,
                           [
                               r"add_stock\(",
                               r"\{1\:\s\"iPhone\sModel\sA\",[\n\s]*2\:\s\"Xiaomi\sModel\sB\",[\n\s]*3\:\s\"Nokia\sModel\sC\"\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"Mobile\smodel\sname\smust\sbe\sa\sstring\"|assert\s*\"Mobile\smodel\sname\smust\sbe\sa\sstring\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventoryAddStock.test_add_new_stock_with_nonnumeric_values,
                           [
                               r"add_stock\(",
                               r"\{\"iPhone\sModel\sA\"\:\s\"50\",[\n\s]*\"Xiaomi\sModel\sB\"\:\s\"2000\",[\n\s]*\"Nokia\sModel\sC\"\:\s\"25\"\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"|assert\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventoryAddStock.test_add_new_stock_with_float_values,
                           [
                               r"add_stock\(",
                               r"\{\"iPhone\sModel\sA\"\:\s50.5,[\n\s]*\"Xiaomi\sModel\sB\"\:\s2000.3,[\n\s]*\"Nokia\sModel\sC\"\:\s25\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"|assert\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventorySellStock.setup_class,
                           [
                               r"@classmethod",
                               r"\{\"iPhone\sModel\sA\"\:\s50,[\n\s]*\"Xiaomi\sModel\sB\"\:\s2000,[\n\s]*\"Nokia\sModel\sC\"\:\s10,[\n\s]*\"Sony\sModel\sD\"\:\s1\}"
                           ]),
                          (test_inventory.TestInventorySellStock.test_sell_stock_as_dict,
                           [
                               r"sell_stock\(",
                               r"\{\"iPhone\sModel\sA\"\:\s2,[\n\s]*\"Xiaomi\sModel\sB\"\:\s20,[\n\s]*\"Sony\sModel\sD\"\:\s1\}",
                               r"(assert.+==\s*\{\"iPhone\sModel\sA\"\:\s48,[\n\s]*\"Xiaomi\sModel\sB\"\:\s1980,[\n\s]*\"Nokia\sModel\sC\"\:\s10,[\n\s]*\"Sony\sModel\sD\"\:\s0\}|assert\s*\{\"iPhone\sModel\sA\"\:\s48,[\n\s]*\"Xiaomi\sModel\sB\"\:\s1980,[\n\s]*\"Nokia\sModel\sC\"\:\s10,[\n\s]*\"Sony\sModel\sD\"\:\s0\}\s*==.+)"
                           ]),
                          (test_inventory.TestInventorySellStock.test_sell_stock_as_list,
                           [
                               r"sell_stock\(",
                               r"pytest\.raises\(TypeError",
                               r"\[\"iPhone\sModel\sA\",\s\"Xiaomi\sModel\sB\",\s\"Nokia\sModel\sC\"\]",
                               r"(assert.+==\s*\"Requested\sstock\smust\sbe\sa\sdictionary\"|assert\s*\"Requested\sstock\smust\sbe\sa\sdictionary\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventorySellStock.test_sell_stock_with_numeric_keys,
                           [
                               r"sell_stock\(",
                               r"\{1\:\s\"iPhone\sModel\sA\",[\n\s]*2\:\s\"Xiaomi\sModel\sB\",[\n\s]*3\:\s\"Nokia\sModel\sC\"\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"Mobile\smodel\sname\smust\sbe\sa\sstring\"|assert\s*\"Mobile\smodel\sname\smust\sbe\sa\sstring\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventorySellStock.test_sell_stock_with_nonnumeric_values,
                           [
                               r"sell_stock\(",
                               r"\{\"iPhone\sModel\sA\"\:\s\"2\",[\n\s]*\"Xiaomi\sModel\sB\"\:\s\"3\",[\n\s]*\"Nokia\sModel\sC\"\:\s\"4\"\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"|assert\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventorySellStock.test_sell_stock_with_float_values,
                           [
                               r"sell_stock\(",
                               r"\{\"iPhone\sModel\sA\"\:\s2.5,[\n\s]*\"Xiaomi\sModel\sB\"\:\s3.1,[\n\s]*\"Nokia\sModel\sC\"\:\s4\}",
                               r"pytest\.raises\(ValueError",
                               r"(assert.+==\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"|assert\s*\"No\.\sof\smobiles\smust\sbe\sa\spositive\sinteger\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventorySellStock.test_sell_stock_of_nonexisting_model,
                           [
                               r"sell_stock\(",
                               r"\{\"iPhone\sModel\sB\"\:\s2,[\n\s]*\"Xiaomi\sModel\sB\"\:\s5\}",
                               r"pytest\.raises\(InsufficientException",
                               r"(assert.+==\s*\"No\sStock\.\sNew\sModel\sRequest\"|assert\s*\"No\sStock\.\sNew\sModel\sRequest\"\s*==.+)"
                           ]),
                          (test_inventory.TestInventorySellStock.test_sell_stock_of_insufficient_stock,
                           [
                               r"sell_stock\(",
                               r"\{\"iPhone\sModel\sA\"\:\s2,[\n\s]*\"Xiaomi\sModel\sB\"\:\s5,[\n\s]*\"Nokia\sModel\sC\"\:\s15\}",
                               r"pytest\.raises\(InsufficientException",
                               r"(assert.+==\s*\"Insufficient\sStock\"|assert\s*\"Insufficient\sStock\"\s*==.+)"
                           ])
                          ],
                         ids=['test_tescases1', 'test_tescases2', 'test_tescases3', 'test_tescases4', 'test_tescases5',
                              'test_tescases6', 'test_tescases7', 'test_tescases8', 'test_tescases9', 'test_tescases10',
                              'test_tescases11', 'test_tescases12', 'test_tescases13', 'test_tescases14',
                              'test_tescases15',
                              'test_tescases16', 'test_tescases17', 'test_tescases18', 'test_tescases19',
                              'test_tescases20'])
def test_source_code(inspect_get_sourcecode, expected):
    code = autopep8.fix_code(inspect_get_sourcecode).replace("'", '"')
    for exp in expected:
        assert bool(re.search(exp, code))


@pytest.mark.parametrize("source, expected",
                         [("pytestresult.xml", 18)], ids=['test_testcase_result'])
def test_pytest_testcase_result(get_xml_root_element, expected):
    test_case_success = int(get_xml_root_element.attrib["tests"]) - int(get_xml_root_element.attrib["failures"]) - int(
        get_xml_root_element.attrib["errors"]) - int(get_xml_root_element.attrib["skipped"])
    assert int(get_xml_root_element.attrib["tests"]) == expected and test_case_success == expected
