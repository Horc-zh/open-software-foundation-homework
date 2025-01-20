import simplejson as json
from hypothesis import given, strategies as st
import pytest

# 测试用例：测试loads函数的稳定性

@given(st.text())
def test_loads_valid_json(json_string):
    """测试loads函数的稳定性，处理有效的JSON字符串"""
    try:
        result = json.loads(json_string)
        assert isinstance(result, (dict, list, str, int, float, bool, type(None)))
    except ValueError:
        pass  # 如果是无效的JSON格式，ValueError是预期的

@given(st.lists(st.integers()))
def test_loads_valid_list(json_list):
    """测试loads函数的稳定性，处理有效的JSON列表"""
    json_string = json.dumps(json_list)
    result = json.loads(json_string)
    assert result == json_list

@given(st.dictionaries(st.text(), st.integers()))
def test_loads_valid_dict(json_dict):
    """测试loads函数的稳定性，处理有效的JSON字典"""
    json_string = json.dumps(json_dict)
    result = json.loads(json_string)
    assert result == json_dict

@given(st.text(min_size=10, max_size=100))
def test_loads_invalid_json(json_string):
    """测试loads函数对非法JSON字符串的处理"""
    if not json_string.startswith("{") and not json_string.startswith("["):
        with pytest.raises(ValueError):
            json.loads(json_string)

# 测试用例：测试dumps函数的稳定性

@given(st.lists(st.integers()))
def test_dumps_list(json_list):
    """测试dumps函数的稳定性，序列化JSON列表"""
    result = json.dumps(json_list)
    assert isinstance(result, str)
    # 验证是否能够成功反序列化
    assert json.loads(result) == json_list

@given(st.dictionaries(st.text(), st.integers()))
def test_dumps_dict(json_dict):
    """测试dumps函数的稳定性，序列化JSON字典"""
    result = json.dumps(json_dict)
    assert isinstance(result, str)
    # 验证是否能够成功反序列化
    assert json.loads(result) == json_dict

@given(st.text())
def test_dumps_string(json_string):
    """测试dumps函数的稳定性，序列化JSON字符串"""
    result = json.dumps(json_string)
    assert isinstance(result, str)

@given(st.integers())
def test_dumps_integer(json_integer):
    """测试dumps函数的稳定性，序列化整数"""
    result = json.dumps(json_integer)
    assert isinstance(result, str)
    # 验证反序列化
    assert json.loads(result) == json_integer

# 边界测试：测试极大数值、特殊字符等

@given(st.integers(min_value=-10**6, max_value=10**6))
def test_dumps_large_integer(json_integer):
    """测试dumps函数的稳定性，处理大数值"""
    result = json.dumps(json_integer)
    assert isinstance(result, str)
    # 验证反序列化
    assert json.loads(result) == json_integer

@given(st.text(min_size=1000))
def test_dumps_large_string(json_string):
    """测试dumps函数的稳定性，处理长字符串"""
    result = json.dumps(json_string)
    assert isinstance(result, str)
    # 验证反序列化
    assert json.loads(result) == json_string
