from .rules import BusinessRule
from .exceptions import BusinessRuleException

class ValidateRulesMixin:
    def validate_rule(self, rule: BusinessRule) -> None:
        if not rule.is_valid():
          raise BusinessRuleException(rule)