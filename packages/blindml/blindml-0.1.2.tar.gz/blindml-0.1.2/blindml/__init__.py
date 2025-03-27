import sys
from types import ModuleType
from .client import BlindML

class CallableModule(ModuleType):
    """
    확장된 모듈 클래스: 호출 시 BlindML 객체를 반환하도록 설정.
    """
    def __call__(self, *args, **kwargs):
        return BlindML(*args, **kwargs)

# 기존 모듈을 CallableModule로 대체
sys.modules[__name__].__class__ = CallableModule
