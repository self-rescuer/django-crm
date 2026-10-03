import allure
from django.urls import reverse
from tests.base_test_classes import BaseTestCase
from tests.utils.factories import DataFactory
from common.utils.helpers import USER_MODEL


@allure.feature("对象级权限")
class TestObjectPermissions(BaseTestCase):
    """测试跨部门的对象访问权限"""

    def setUp(self):
        self.user_global = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.user_bookkeeping = USER_MODEL.objects.get(username="Sergey.Co-worker.Head.Bookkeeping")
        self.admin = USER_MODEL.objects.get(username="Adam.Admin")
        self.factory_global = DataFactory(owner=self.user_global)
        self.factory_bookkeeping = DataFactory(owner=self.user_bookkeeping)

    @allure.story("同部门可协作")
    def test_same_department_can_access(self):
        """同一部门的用户可以编辑对方创建的公司"""
        company = self.factory_global.create_company(full_name="Global公司")
        self.client.force_login(self.user_global)
        url = reverse("site:crm_company_change", args=(company.id,))
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])

    @allure.story("跨部门被拦截")
    def test_cross_department_blocked(self):
        """跨部门的用户不能编辑对方创建的公司"""
        company = self.factory_bookkeeping.create_company(full_name="Bookkeeping公司")

        self.client.force_login(self.user_global)
        url = reverse("site:crm_company_change", args=(company.id,))
        response = self.client.get(url, follow=True)

        # 被重定向
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            len(response.redirect_chain) > 0,
            "跨部门访问应该被重定向"
        )

    @allure.story("管理员跨部门")
    def test_admin_can_access_any_department(self):
        """管理员能跨部门编辑任何公司"""
        company = self.factory_bookkeeping.create_company(full_name="Bookkeeping公司")
        self.client.force_login(self.admin)
        url = reverse("site:crm_company_change", args=(company.id,))
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])