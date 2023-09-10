from typing import Union
import time


def getvalidvalue(self, func):
    def wrapper(*args, **kw):
        if self.valid is True:
            return func(*args, **kw)
        else:
            return None
    return wrapper


class timelimtited_cache:
    # __valid: bool = False
    _lasttime: Union[float, None] = None
    _validtime: Union[float, int, str, None] = None

    @property
    def valid(self):
        if self._validtime is str:
            if self._validtime == 'infinite':
                return True
            elif self._validtime == 'none':
                return False

        now = time.time()
        period = now - self._lasttime

        if self._validtime is float or self._validtime is int:
            if period < self._validtime:
                return True
        return False

    @valid.setter
    def valid(self, data: bool):
        """ 手动设置可用状态，这将会禁用过期验证。

        :param data: 可用状态，True/False
        :return: 无
        """
        # self.__valid = data
        if data is True:
            self._validtime = 'infinite'
        else:
            self._validtime = 'none'

    @property
    def validtime(self):
        return self._validtime

    @validtime.setter
    def validtime(self, data: Union[float, int, str, None]):
        if data is str:
            if data.isalnum():
                data = int(data)
            else:
                try:
                    data = float(data)
                except ValueError:
                    if data != 'infinite' and data != 'none':
                        raise ValueError(
                            'String type value "{string}" is illegal. Only "infinite" and "none" are allowed. '.format(
                                string=data))
                    pass
        self._validtime = data
        pass
