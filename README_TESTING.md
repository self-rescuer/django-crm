# django-crm 测试开发实践

## 项目简介

本项目是对开源 CRM 系统 [django-crm](https://github.com/DjangoCRM/django-crm) 的测试开发实践。
在原始项目基础上，我独立设计并实现了 CRM 和 Tasks 两个核心模块的自动化测试。

## 测试范围

| 模块 | 测试文件 | 用例数 | 覆盖内容 |
|------|---------|--------|---------|
| CRM - 客户管理 | test_my_first.py | 5 | 公司创建、字段校验、唯一约束 |
| CRM - 线索转化 | test_my_lead_conversion.py | 2 | 线索转化为公司和联系人 |
| CRM - 交易管理 | test_my_deal.py | 5 | 交易创建、字段校验、关联查询 |
| CRM - 客户请求 | test_my_request.py | 3 | 请求校验、业务规则 |
| CRM - 端到端 | test_my_e2e.py | 1 | 从请求到交易的完整流程 |
| Tasks - 任务 | test_my_task.py | 5 | 任务创建、状态联动、业务规则 |
| Tasks - 项目 | test_my_project.py | 3 | 项目创建、状态联动 |
| **合计** | | **24** | |

## 测试分层

- **模型层测试**：字段校验、字符串表示、唯一约束
- **业务规则测试**：线索转化、联系人与公司匹配、任务关闭规则
- **端到端测试**：跨模型的完整业务流程

## 技术栈

- Python 3.12
- Django 6.0
- pytest + pytest-django
- Allure 报告
- GitHub Actions CI

## 运行测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行全部自定义测试
pytest tests/crm/test_my_*.py tests/tasks/test_my_*.py -v

# 生成 Allure 报告
allure serve allure-results
```
## 项目结构
```text
tests/
├── crm/
│   ├── test_my_first.py            # Company 测试
│   ├── test_my_lead_conversion.py  # 线索转化测试
│   ├── test_my_deal.py             # Deal 测试
│   ├── test_my_request.py          # Request 测试
│   └── test_my_e2e.py              # 端到端测试
├── tasks/
│   ├── test_my_task.py             # Task 测试
│   └── test_my_project.py          # Project 测试
└── utils/
    └── factories.py                # 测试数据工厂

```
## CI/CD

配置了 GitHub Actions，每次 push 自动运行全部测试。
工作流文件：.github/workflows/test.yml

## 遇到的典型问题
1.Lead 创建缺少 department_id：导致 Admin 页面渲染失败，无法获取表单数据。

解决：创建 Lead 时传入 department_id=get_department_id(owner)。

2.pytest-django 无法加载 settings：.gitignore 误将 pytest.ini 忽略，CI 环境无配置。

解决：从 .gitignore 移除 pytest.ini，提交到仓库。



3.数据工厂类名触发 pytest 警告：类名以 Test 开头被误判为测试类。

解决：改名为 DataFactory。