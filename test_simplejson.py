import simplejson
from hypothesis import given, strategies as st
from hypothesis.errors import InvalidArgument

# 1. 测试 simplejson.loads() 的随机字符串输入
@given(st.text())
def test_loads_random_input(input_data):
    try:
        # 尝试解析随机生成的 JSON 字符串
        simplejson.loads(input_data)
    except simplejson.errors.JSONDecodeError:
        pass  # 忽略无效的 JSON 格式
    except Exception as e:
        assert False, f"Unexpected error in loads: {e}"

# 2. 测试 simplejson.loads() 处理非法字符的情况
@given(st.text())
def test_loads_invalid_characters(input_data):
    # 在随机文本中加入非法字符（如非 UTF-8 编码字符）
    invalid_json = input_data + "\x80"  # \x80 是非法的 ASCII 字符
    try:
        simplejson.loads(invalid_json)
    except simplejson.errors.JSONDecodeError:
        pass  # 预期抛出 JSONDecodeError 异常
    except Exception as e:
        assert False, f"Unexpected error in loads with invalid char: {e}"

# 3. 测试 simplejson.loads() 处理边界值（如空字符串和极大数字）
@given(st.one_of(st.text(), st.integers(), st.floats(), st.none()))
def test_loads_edge_cases(input_data):
    try:
        # 尝试解析不同类型的边界值
        simplejson.loads(str(input_data))
    except simplejson.errors.JSONDecodeError:
        pass  # 忽略无效的 JSON 格式
    except Exception as e:
        assert False, f"Unexpected error in loads with edge cases: {e}"

# 4. 测试 simplejson.dumps() 能否正确序列化基本类型（数字、列表、字典等）
@given(st.integers() | st.floats() | st.booleans() | st.text() | st.lists(st.integers()) | st.dictionaries(st.text(), st.integers()))
def test_dumps_basic_types(input_data):
    try:
        result = simplejson.dumps(input_data)
        assert isinstance(result, str)  # 确保返回的结果是字符串
    except Exception as e:
        assert False, f"Unexpected error in dumps with basic types: {e}"

# 5. 测试 simplejson.dumps() 处理无法序列化的对象（如自定义类对象）
class CustomClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"CustomClass({self.value})"

# 测试无法序列化的对象
@given(st.builds(CustomClass, st.text()))
def test_dumps_non_serializable_objects(custom_obj):
    try:
        # 尝试序列化自定义类对象
        result = simplejson.dumps(custom_obj)
        assert False, "Expected TypeError for non-serializable object"
    except TypeError:
        pass  # 预期抛出 TypeError 异常
    except Exception as e:
        assert False, f"Unexpected error in dumps with non-serializable object: {e}"

