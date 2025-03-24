from ageless.operators.contains import AgeContains
from ageless.operators.ends_with import AgeEndsWith
from ageless.operators.eq import AgeEqual
from ageless.operators.is_not_null import AgeIsNotNull
from ageless.operators.is_null import AgeIsNull
from ageless.operators.manager import AgeOperatorManager
from ageless.operators.ne import AgeNotEqual
from ageless.operators.raw import AgeRaw
from ageless.operators.regex import AgeRegex
from ageless.operators.starts_with import AgeStartsWith

operator_cls_list = [
    AgeEqual,
    AgeNotEqual,
    AgeContains,
    AgeStartsWith,
    AgeEndsWith,
    AgeIsNull,
    AgeIsNotNull,
    AgeRegex,
    AgeRaw,
]

operator_manager = AgeOperatorManager()

for operator_cls in operator_cls_list:
    operator_manager.register(operator_cls)
