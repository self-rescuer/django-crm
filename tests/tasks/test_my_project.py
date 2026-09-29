import allure
from datetime import date, timedelta
from tests.base_test_classes import BaseTestCase
from tasks.models import Project, ProjectStage
from common.utils.helpers import USER_MODEL


@allure.feature("项目管理")
class TestMyProject(BaseTestCase):
    """测试 Project 模型"""

    fixtures = (
        'currency.json', 'test_country.json', 'resolution.json',
        'groups.json', 'department.json', 'test_users.json',
        'projectstage.json', 'taskstage.json',
    )

    def setUp(self):
        self.owner = USER_MODEL.objects.get(username="Garry.Chief")
        self.default_stage = ProjectStage.objects.get(default=True)

    @allure.story("创建项目")
    def test_create_project(self):
        """创建项目后能查询到"""
        project = Project.objects.create(
            name="测试项目",
            stage=self.default_stage,
            owner=self.owner,
            next_step="启动",
            next_step_date=date.today() + timedelta(days=1),
        )
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(project.name, "测试项目")

    @allure.story("字符串表示")
    def test_project_str(self):
        """Project 的字符串表示是 name"""
        project = Project.objects.create(
            name="测试项目",
            stage=self.default_stage,
            owner=self.owner,
            next_step="启动",
            next_step_date=date.today() + timedelta(days=1),
        )
        self.assertEqual(str(project), "测试项目")

    @allure.story("状态联动")
    def test_project_active_follows_stage(self):
        """项目的 active 状态由 stage 决定"""
        project = Project.objects.create(
            name="测试项目",
            stage=self.default_stage,
            owner=self.owner,
            next_step="启动",
            next_step_date=date.today() + timedelta(days=1),
        )
        self.assertEqual(project.active, self.default_stage.active)