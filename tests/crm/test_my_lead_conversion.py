from django.urls import reverse
from crm.models import Lead, Company, Contact, Country
from tests.base_test_classes import BaseTestCase
from tests.utils.helpers import get_adminform_initials
from common.utils.helpers import USER_MODEL
from common.utils.helpers import get_department_id




class TestMyLeadConversion(BaseTestCase):
    """测试 Lead 转化流程"""

    def test_conversion_with_existing_company(self):
        """Lead 已经关联 Company 时，不新建"""
        owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        country = Country.objects.first()

        company = Company.objects.create(
            full_name="已有公司",
            email="existing@test.com",
            owner=owner
        )
        lead = Lead.objects.create(
            first_name="李",
            last_name="四",
            email="lisi@test.com",
            company=company,
            country=country,
            department_id=get_department_id(owner),
            owner=owner
        )
        company_count_before = Company.objects.count()

        self.client.force_login(owner)
        url = reverse("site:crm_lead_change", args=(lead.id,))
        response = self.client.get(url, follow=True)
        data = get_adminform_initials(response)
        data['_convert'] = ''
        data.pop('avatar', None)
        self.client.post(url, data, follow=True)

        self.assertEqual(Company.objects.count(), company_count_before)
        self.assertFalse(Lead.objects.filter(id=lead.id).exists())

    def setUp(self):
        self.owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.country = Country.objects.first()
        self.department_id = get_department_id(self.owner)

    def test_conversion_creates_company_and_contact(self):
        """转化 Lead 时自动创建 Company 和 Contact"""
        owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        country = Country.objects.first()

        lead = Lead.objects.create(
            first_name="张",
            last_name="三",
            email="zhangsan@test.com",
            company_name="测试科技公司",
            company_email="office@test.com",
            country=self.country,
            department_id=self.department_id,
            owner=self.owner
        )
        lead_id = lead.id
        company_count_before = Company.objects.count()
        contact_count_before = Contact.objects.count()

        self.client.force_login(owner)
        url = reverse("site:crm_lead_change", args=(lead_id,))
        response = self.client.get(url, follow=True)

        data = get_adminform_initials(response)
        data['_convert'] = ''
        data.pop('avatar', None)
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Company.objects.count(), company_count_before + 1)
        self.assertEqual(Contact.objects.count(), contact_count_before + 1)
        self.assertFalse(Lead.objects.filter(id=lead_id).exists())














