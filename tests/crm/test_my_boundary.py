import allure
from django.core.exceptions import ValidationError
from tests.base_test_classes import BaseTestCase
from tests.utils.factories import DataFactory
from crm.models import Company
from common.utils.helpers import USER_MODEL


@allure.feature("边界值测试")
class TestCompanyBoundary(BaseTestCase):
    """测试 Company 字段的边界值"""

    def setUp(self):
        self.owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.factory = DataFactory(owner=self.owner)

    @allure.story("字段长度边界")
    def test_full_name_at_max_length(self):
        """full_name 长度正好等于 200 时应该通过"""
        name = "a" * 200
        company = self.factory.create_company(full_name=name)
        self.assertEqual(len(company.full_name), 200)

    @allure.story("字段长度边界")
    def test_full_name_exceeds_max_length(self):
        """full_name 长度 201 时应该报错"""
        name = "a" * 201
        company = Company(
            full_name=name,
            email="test@test.com",
            owner=self.owner,
            department_id=self.factory.department_id,
        )
        with self.assertRaises(ValidationError):
            company.full_clean()

    @allure.story("字段长度边界")
    def test_full_name_one_below_max(self):
        """full_name 长度 199 时应该通过"""
        name = "a" * 199
        company = self.factory.create_company(full_name=name)
        self.assertEqual(len(company.full_name), 199)

    @allure.story("空值边界")
    def test_full_name_empty(self):
        """full_name 为空时应该报错"""
        company = Company(
            full_name="",
            email="test@test.com",
            owner=self.owner,
            department_id=self.factory.department_id,
        )
        with self.assertRaises(ValidationError):
            company.full_clean()

    @allure.story("特殊字符")
    def test_full_name_with_chinese(self):
        """full_name 包含中文应正常处理"""
        name = "测试科技公司"
        company = self.factory.create_company(full_name=name)
        self.assertEqual(company.full_name, "测试科技公司")

    @allure.story("特殊字符")
    def test_full_name_with_emoji(self):
        """full_name 包含 emoji 应正常处理"""
        name = "Test Company 🚀"
        company = self.factory.create_company(full_name=name)
        self.assertEqual(company.full_name, "Test Company 🚀")

    @allure.story("特殊字符")
    def test_full_name_with_special_chars(self):
        """full_name 包含特殊符号应正常处理"""
        name = "A&B Co., Ltd. (Test)"
        company = self.factory.create_company(full_name=name)
        self.assertEqual(company.full_name, "A&B Co., Ltd. (Test)")