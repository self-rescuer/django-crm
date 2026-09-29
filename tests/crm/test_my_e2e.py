import allure
from datetime import date, timedelta
from crm.models import Request, Deal, Stage, Company, Contact
from tests.base_test_classes import BaseTestCase
from common.utils.helpers import USER_MODEL, get_department_id


@allure.feature("端到端流程")
class TestRequestToDealFlow(BaseTestCase):
    """端到端测试：从客户请求到交易的完整流程"""

    def setUp(self):
        self.owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.department_id = get_department_id(self.owner)
        self.stage = Stage.objects.filter(
            department_id=self.department_id,
            default=True
        ).first()

    @allure.story("请求到交易")
    def test_request_to_deal_flow(self):
        """完整流程：请求 → 客户 → 交易"""
        with allure.step("创建公司"):
            company = Company.objects.create(
                full_name="端到端测试公司",
                email="e2e@test.com",
                owner=self.owner
            )

        with allure.step("创建联系人"):
            contact = Contact.objects.create(
                first_name="端",
                last_name="到端",
                email="contact@test.com",
                company=company,
                department_id=self.department_id,
                owner=self.owner
            )

        with allure.step("创建请求"):
            request = Request.objects.create(
                request_for="购买产品咨询",
                first_name="端",
                email="contact@test.com",
                company=company,
                contact=contact,
                department_id=self.department_id,
                owner=self.owner
            )

        with allure.step("创建交易并关联请求"):
            deal = Deal.objects.create(
                name="端到端交易",
                request=request,
                company=company,
                contact=contact,
                next_step="报价",
                next_step_date=date.today() + timedelta(days=3),
                stage=self.stage,
                department_id=self.department_id,
                owner=self.owner
            )

        with allure.step("验证关联关系"):
            self.assertEqual(deal.request, request)
            self.assertEqual(deal.company, company)
            self.assertEqual(deal.contact, contact)
            self.assertEqual(company.deals.count(), 1)
            self.assertIn(deal, company.deals.all())

        with allure.step("建立双向关联并验证"):
            request.deal = deal
            request.save()
            request.refresh_from_db()
            self.assertEqual(request.deal, deal)
            self.assertEqual(deal.requests.count(), 1)