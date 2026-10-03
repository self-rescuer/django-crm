"""测试数据工厂：统一创建测试对象，减少重复代码"""
from datetime import date, timedelta
from crm.models import Company, Contact, Deal, Lead, Request, Stage
from tasks.models import Task, Project, TaskStage, ProjectStage
from common.utils.helpers import USER_MODEL, get_department_id


class DataFactory:
    """测试数据工厂，提供各类对象的创建方法"""

    def __init__(self, owner=None):
        if owner is None:
            owner = USER_MODEL.objects.get(username="Andrew.Manager.Global")
        self.owner = owner
        self.department_id = get_department_id(self.owner)

    # ---------- CRM ----------

    def create_company(self, **kwargs):
        defaults = {
            "full_name": "测试公司",
            "email": "company@test.com",
            "owner": self.owner,
            "department_id": self.department_id,
        }
        defaults.update(kwargs)
        return Company.objects.create(**defaults)

    def create_contact(self, company=None, **kwargs):
        if company is None:
            company = self.create_company()
        defaults = {
            "first_name": "测试",
            "last_name": "联系人",
            "email": "contact@test.com",
            "company": company,
            "department_id": self.department_id,
            "owner": self.owner,
        }
        defaults.update(kwargs)
        return Contact.objects.create(**defaults)

    def create_lead(self, **kwargs):
        defaults = {
            "first_name": "潜在",
            "last_name": "客户",
            "email": "lead@test.com",
            "company_name": "潜在公司",
            "department_id": self.department_id,
            "owner": self.owner,
        }
        defaults.update(kwargs)
        return Lead.objects.create(**defaults)

    def create_deal(self, **kwargs):
        defaults = {
            "name": "测试交易",
            "next_step": "下一步",
            "next_step_date": date.today() + timedelta(days=1),
            "department_id": self.department_id,
            "owner": self.owner,
            "stage": Stage.objects.filter(
                department_id=self.department_id, default=True
            ).first(),
        }
        defaults.update(kwargs)
        return Deal.objects.create(**defaults)

    def create_request(self, **kwargs):
        defaults = {
            "request_for": "测试请求",
            "first_name": "请求",
            "email": "request@test.com",
            "department_id": self.department_id,
            "owner": self.owner,
        }
        defaults.update(kwargs)
        return Request.objects.create(**defaults)

    # ---------- Tasks ----------

    def create_task(self, **kwargs):
        defaults = {
            "name": "测试任务",
            "stage": TaskStage.objects.get(default=True),
            "owner": self.owner,
            "next_step": "处理",
            "next_step_date": date.today() + timedelta(days=1),
        }
        defaults.update(kwargs)
        return Task.objects.create(**defaults)

    def create_project(self, **kwargs):
        defaults = {
            "name": "测试项目",
            "stage": ProjectStage.objects.get(default=True),
            "owner": self.owner,
            "next_step": "启动",
            "next_step_date": date.today() + timedelta(days=1),
        }
        defaults.update(kwargs)
        return Project.objects.create(**defaults)