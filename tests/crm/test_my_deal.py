import allure
from tests.base_test_classes import BaseTestCase
from tests.utils.factories import DataFactory
from crm.models import Deal
from common.utils.helpers import USER_MODEL


@allure.feature("交易管理")
class TestMyDeal(BaseTestCase):
    """测试 Deal 模型的字段校验和关联（使用数据工厂）"""

    def setUp(self):
        owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.factory = DataFactory(owner=owner)

    @allure.story("创建交易")
    def test_create_deal(self):
        deal = self.factory.create_deal()
        self.assertEqual(Deal.objects.count(), 1)
        self.assertEqual(deal.name, "测试交易")

    @allure.story("字符串表示")
    def test_deal_str(self):
        deal = self.factory.create_deal()
        self.assertEqual(str(deal), "测试交易")

    @allure.story("默认值")
    def test_deal_default_amount(self):
        deal = self.factory.create_deal()
        self.assertEqual(deal.amount, 0)

    @allure.story("关联查询")
    def test_deal_with_company(self):
        company = self.factory.create_company(full_name="关联公司")
        deal = self.factory.create_deal(company=company)
        self.assertEqual(deal.company, company)
        self.assertEqual(company.deals.count(), 1)

    @allure.story("关联查询")
    def test_deal_without_company(self):
        deal = self.factory.create_deal()
        self.assertIsNone(deal.company)