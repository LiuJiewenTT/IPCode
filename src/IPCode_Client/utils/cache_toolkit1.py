from typing import Union
import time


def cls_getvalidvalue(func):
    def wrapper(*args, **kw):
        self = args[0]
        # print(f'args: [{args}]')
        if self.valid is True:
            return func(*args, **kw)
        else:
            # print('not valid')
            return None
    return wrapper


def cls_getvalidvalue_autorefresh(refresh_callback_function_name):
    def wrapper0(func):
        def wrapper1(*args, **kw):
            retv0 = cls_getvalidvalue(func)
            retv1 = retv0(*args, **kw)
            if retv1 is None:
                self = args[0]
                # print(f'args: [{args}]')
                refresh_callback = eval(f'self.{refresh_callback_function_name}')
                # refresh_callback = self.refresh_callback_function
                # print(f'refresh_callback: {refresh_callback}')
                refresh_callback.__call__()
                return retv0(*args, **kw)
            return retv1
        return wrapper1
    return wrapper0


class timelimtited_cache:
    # __valid: bool = False
    _lasttime: Union[float, None] = None
    _validtime: Union[float, int, str, None] = None

    @property
    def valid(self):
        if self._lasttime is None:
            return False
        if type(self._validtime) is str:
            if self._validtime == 'infinite':
                return True and (self._lasttime is not None)
            elif self._validtime == 'none':
                return False

        now = time.time()
        period = now - self._lasttime

        if type(self._validtime) is float or type(self._validtime) is int:
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
        if type(data) is str:
            if data.isnumeric():
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
