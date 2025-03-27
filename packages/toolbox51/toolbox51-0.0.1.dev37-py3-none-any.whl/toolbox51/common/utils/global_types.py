__all__ = []


from toolbox51.common.singleton import SingletonMeta


__all__ += ['NotGiven', 'NOT_GIVEN']
class NotGiven(metaclass=SingletonMeta):
    def __bool__(self):
        return False
NOT_GIVEN = NotGiven()