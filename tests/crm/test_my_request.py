from django.core.exceptions import ValidationError
from crm.models import Request, Company, Contact, Lead
from tests.base_test_classes import BaseTestCase
from common.utils.helpers import USER_MODEL, get_department_id


class TestMyRequest(BaseTestCase):
    """测试 Request 模型的验证规则"""

    def setUp(self):
        self.owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.department_id = get_department_id(self.owner)
        self.company = Company.objects.create(
            full_name="测试公司A",
            email="compA@test.com",
            owner=self.owner
        )

    def test_request_requires_first_name(self):
        """first_name 为空时校验失败"""
        request = Request(
            request_for="咨询",
            first_name="",
            email="test@test.com",
            department_id=self.department_id,
            owner=self.owner
        )
        with self.assertRaises(ValidationError):
            request.full_clean()

    def test_request_contact_and_company_must_match(self):
        """contact 属于另一家公司时校验失败"""
        other_company = Company.objects.create(
            full_name="测试公司B",
            email="compB@test.com",
            owner=self.owner
        )
        contact = Contact.objects.create(
            first_name="张",
            last_name="三",
            email="zhang@test.com",
            company=other_company,
            department_id=self.department_id,
            owner=self.owner
        )
        request = Request(
            request_for="咨询",
            first_name="张",
            contact=contact,
            company=self.company,    # ← 和 contact.company 不一致
            department_id=self.department_id,
            owner=self.owner
        )
        with self.assertRaises(ValidationError):
            request.full_clean()

    def test_request_cannot_have_both_contact_and_lead(self):
        """不能同时指定 contact 和 lead"""
        contact = Contact.objects.create(
            first_name="李",
            last_name="四",
            email="li@test.com",
            company=self.company,
            department_id=self.department_id,
            owner=self.owner
        )
        lead = Lead.objects.create(
            first_name="王",
            last_name="五",
            email="wang@test.com",
            company=self.company,
            department_id=self.department_id,
            owner=self.owner
        )
        request = Request(
            request_for="咨询",
            first_name="李",
            contact=contact,
            lead=lead,    # ← 同时指定了两个
            department_id=self.department_id,
            owner=self.owner
        )
        with self.assertRaises(ValidationError):
            request.full_clean()