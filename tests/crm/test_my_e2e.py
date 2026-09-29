from datetime import date, timedelta
from crm.models import Request, Deal, Stage, Company, Contact
from tests.base_test_classes import BaseTestCase
from common.utils.helpers import USER_MODEL, get_department_id


class TestRequestToDealFlow(BaseTestCase):
    """端到端测试：从客户请求到交易的完整流程"""

    def setUp(self):
        self.owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.department_id = get_department_id(self.owner)
        self.stage = Stage.objects.filter(
            department_id=self.department_id,
            default=True
        ).first()

    def test_request_to_deal_flow(self):
        """完整流程：请求 → 客户 → 交易"""
        # 1. 创建公司
        company = Company.objects.create(
            full_name="端到端测试公司",
            email="e2e@test.com",
            owner=self.owner
        )

        # 2. 创建联系人
        contact = Contact.objects.create(
            first_name="端",
            last_name="到端",
            email="contact@test.com",
            company=company,
            department_id=self.department_id,
            owner=self.owner
        )

        # 3. 创建请求
        request = Request.objects.create(
            request_for="购买产品咨询",
            first_name="端",
            email="contact@test.com",
            company=company,
            contact=contact,
            department_id=self.department_id,
            owner=self.owner
        )

        # 4. 创建交易，关联请求
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

        # 5. 验证关联关系
        self.assertEqual(deal.request, request)
        self.assertEqual(deal.company, company)
        self.assertEqual(deal.contact, contact)
        self.assertEqual(company.deals.count(), 1)
        self.assertIn(deal, company.deals.all())
        self.assertEqual(request.deal, None)  # Request 还没反向关联

        # 6. 建立双向关联
        request.deal = deal
        request.save()

        # 7. 重新查询验证
        request.refresh_from_db()
        self.assertEqual(request.deal, deal)
        self.assertEqual(deal.requests.count(), 1)