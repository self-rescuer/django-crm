import allure
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from tests.base_test_classes import BaseTestCase
from tests.utils.factories import DataFactory
from tasks.models import Task, TaskStage
from common.utils.helpers import USER_MODEL


@allure.feature("任务管理")
class TestMyTask(BaseTestCase):
    """测试 Task 模型（使用数据工厂）"""

    fixtures = (
        'currency.json', 'test_country.json', 'resolution.json',
        'groups.json', 'department.json', 'test_users.json',
        'projectstage.json', 'taskstage.json',
    )

    def setUp(self):
        owner = USER_MODEL.objects.get(username="Garry.Chief")
        self.factory = DataFactory(owner=owner)
        self.default_stage = TaskStage.objects.get(default=True)
        self.done_stage = TaskStage.objects.get(done=True)

    @allure.story("创建任务")
    def test_create_task(self):
        task = self.factory.create_task()
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.name, "测试任务")

    @allure.story("字符串表示")
    def test_task_str(self):
        task = self.factory.create_task()
        self.assertEqual(str(task), "测试任务")

    @allure.story("状态联动")
    def test_task_active_follows_stage(self):
        task = self.factory.create_task(stage=self.default_stage)
        self.assertEqual(task.active, self.default_stage.active)

    @allure.story("业务规则")
    def test_cannot_close_main_task_with_active_subtask(self):
        main_task = self.factory.create_task(name="主任务")
        self.factory.create_task(name="子任务", task=main_task, stage=self.default_stage)
        main_task.stage = self.done_stage
        with self.assertRaises(ValidationError):
            main_task.full_clean()

    @allure.story("业务规则")
    def test_can_close_main_task_without_active_subtask(self):
        main_task = self.factory.create_task(name="主任务")
        self.factory.create_task(name="子任务", task=main_task, stage=self.done_stage)
        main_task.stage = self.done_stage
        main_task.full_clean()