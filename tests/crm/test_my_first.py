from django.db import IntegrityError
from tests.base_test_classes import BaseTestCase
from crm.models import Company
from crm.models import Country
from common.utils.helpers import USER_MODEL


class TestMyCompany(BaseTestCase):
    """测试 Company 模型的基础功能"""

    def test_create_company(self):
        """创建公司后能查询到"""
        owner = USER_MODEL.objects.get(username="Adam.Admin")
        company = Company.objects.create(
            full_name="测试公司",
            email="test@test.com",
            owner=owner
        )
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(company.full_name, "测试公司")

    def test_company_str(self):
        """公司对象的字符串表示是 full_name"""
        owner = USER_MODEL.objects.get(username="Adam.Admin")
        company = Company.objects.create(
            full_name="测试公司",
            email="test@test.com",
            owner=owner
        )
        self.assertEqual(str(company), "测试公司")

    def test_company_requires_name(self):
        """公司名为空时应报错"""
        owner = USER_MODEL.objects.get(username="Adam.Admin")
        company = Company(full_name="", email="test@test.com", owner=owner)
        with self.assertRaises(Exception):
            company.full_clean()

    def test_company_email_required(self):
        """邮箱为空时应报错"""
        owner = USER_MODEL.objects.get(username="Adam.Admin")
        company = Company(full_name="测试公司", email="", owner=owner)
        with self.assertRaises(Exception):
            company.full_clean()

    def test_company_unique_together(self):
        """同一国家内公司名不能重复"""
        owner = USER_MODEL.objects.get(username="Adam.Admin")
        country = Country.objects.first()

        Company.objects.create(
            full_name="重复公司",
            email="a@a.com",
            owner=owner,
            country=country
        )
        with self.assertRaises(IntegrityError):
            Company.objects.create(
                full_name="重复公司",
                email="b@b.com",
                owner=owner,
                country=country
            )
