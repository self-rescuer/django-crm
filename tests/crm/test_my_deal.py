import allure
from datetime import date, timedelta
from tests.base_test_classes import BaseTestCase
from crm.models import Deal, Stage, Company
from common.utils.helpers import USER_MODEL, get_department_id


@allure.feature("交易管理")
class TestMyDeal(BaseTestCase):
    """测试 Deal 模型的字段校验和关联"""

    def setUp(self):
        self.owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.department_id = get_department_id(self.owner)
        self.stage = Stage.objects.filter(
            department_id=self.department_id,
            default=True
        ).first()

    def _create_deal(self, **kwargs):
        """辅助方法：创建 Deal，可覆盖默认字段"""
        defaults = {
            "name": "测试交易",
            "next_step": "打电话",
            "next_step_date": date.today() + timedelta(days=1),
            "department_id": self.department_id,
            "owner": self.owner,
            "stage": self.stage,
        }
        defaults.update(kwargs)
        return Deal.objects.create(**defaults)

    @allure.story("创建交易")
    def test_create_deal(self):
        """创建 Deal 后能查询到"""
        deal = self._create_deal()
        self.assertEqual(Deal.objects.count(), 1)
        self.assertEqual(deal.name, "测试交易")

    @allure.story("字符串表示")
    def test_deal_str(self):
        """Deal 的字符串表示是 name"""
        deal = self._create_deal()
        self.assertEqual(str(deal), "测试交易")

    @allure.story("字段校验")
    def test_deal_requires_name(self):
        """name 为空时应报错"""
        deal = Deal(
            name="",
            next_step="打电话",
            next_step_date=date.today() + timedelta(days=1),
            department_id=self.department_id,
            owner=self.owner,
        )
        with self.assertRaises(Exception):
            deal.full_clean()

    @allure.story("默认值")
    def test_deal_default_amount(self):
        """不填 amount 时默认为 0"""
        deal = self._create_deal()
        self.assertEqual(deal.amount, 0)

    @allure.story("关联查询")
    def test_deal_with_company(self):
        """Deal 关联到 Company 后能正确查询"""
        company = Company.objects.create(
            full_name="关联公司",
            email="company@test.com",
            owner=self.owner
        )
        deal = self._create_deal(company=company)

        self.assertEqual(deal.company, company)
        self.assertEqual(company.deals.count(), 1)
        self.assertIn(deal, company.deals.all())

    @allure.story("关联查询")
    def test_deal_without_company(self):
        """Deal 不关联 Company 时，company 字段为 None"""
        deal = self._create_deal()
        self.assertIsNone(deal.company)