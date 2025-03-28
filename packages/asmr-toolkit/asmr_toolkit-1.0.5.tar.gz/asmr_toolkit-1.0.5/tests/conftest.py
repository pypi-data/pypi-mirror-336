import os
import sys

import pytest

# 确保测试可以导入主包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# 全局测试设置
@pytest.fixture(autouse=True)
def setup_test_env():
    """设置测试环境"""
    # 保存原始环境变量
    original_env = os.environ.copy()

    # 设置测试环境变量
    os.environ["ASMR_TOOLKIT_TEST"] = "1"

    yield

    # 恢复原始环境变量
    os.environ.clear()
    os.environ.update(original_env)
