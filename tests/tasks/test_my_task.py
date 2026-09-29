import allure
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from tests.base_test_classes import BaseTestCase
from tasks.models import Task, TaskStage
from common.utils.helpers import USER_MODEL


@allure.feature("任务管理")
class TestMyTask(BaseTestCase):
    """测试 Task 模型"""

    fixtures = (
        'currency.json', 'test_country.json', 'resolution.json',
        'groups.json', 'department.json', 'test_users.json',
        'projectstage.json', 'taskstage.json',
    )

    def setUp(self):
        self.owner = USER_MODEL.objects.get(username="Garry.Chief")
        self.default_stage = TaskStage.objects.get(default=True)
        self.done_stage = TaskStage.objects.get(done=True)

    def _create_task(self, **kwargs):
        defaults = {
            "name": "测试任务",
            "stage": self.default_stage,
            "owner": self.owner,
            "next_step": "处理",
            "next_step_date": date.today() + timedelta(days=1),
        }
        defaults.update(kwargs)
        return Task.objects.create(**defaults)

    @allure.story("创建任务")
    def test_create_task(self):
        """创建任务后能查询到"""
        with allure.step("创建任务"):
            task = self._create_task()
        with allure.step("验证任务已创建"):
            self.assertEqual(Task.objects.count(), 1)
            self.assertEqual(task.name, "测试任务")

    @allure.story("字符串表示")
    def test_task_str(self):
        """Task 的字符串表示是 name"""
        task = self._create_task()
        self.assertEqual(str(task), "测试任务")

    @allure.story("状态联动")
    def test_task_active_follows_stage(self):
        """任务的 active 状态由 stage 决定"""
        task = self._create_task(stage=self.default_stage)
        self.assertEqual(task.active, self.default_stage.active)

    @allure.story("业务规则")
    def test_cannot_close_main_task_with_active_subtask(self):
        """有活跃子任务时，主任务不能关闭"""
        main_task = self._create_task(name="主任务")
        self._create_task(name="子任务", task=main_task, stage=self.default_stage)

        main_task.stage = self.done_stage
        with self.assertRaises(ValidationError):
            main_task.full_clean()

    @allure.story("业务规则")
    def test_can_close_main_task_without_active_subtask(self):
        """没有活跃子任务时，主任务可以关闭"""
        main_task = self._create_task(name="主任务")
        self._create_task(name="子任务", task=main_task, stage=self.done_stage)

        main_task.stage = self.done_stage
        main_task.full_clean()  # 不应报错