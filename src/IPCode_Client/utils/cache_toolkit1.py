from typing import Union
import time


def cls_getvalidvalue(value_on_failure=None):
    """ 使函数验证失败会返回指定值的修饰器。

    :param value_on_failure: 失败时返回的值。
    :return: 修饰过的验证失败会返回指定值的函数。
    """
    def wrapper0(func):
        def wrapper1(*args, **kw):
            self = args[0]
            if self.valid is True:
                return func(*args, **kw)
            else:
                # print('not valid')
                return value_on_failure
        return wrapper1
    return wrapper0


def cls_getvalidvalue_autorefresh(refresh_callback_function_name: str = '__str__', value_on_failure=None):
    """ 使函数验证失败会自动尝试刷新的修饰器。

    :param refresh_callback_function_name: (必选)指定用于刷新的成员函数。
    :param value_on_failure: (高级选项)(内部逻辑数值)失败时返回的值(cls_getvalidvalue的内部值)。
    :return: 修饰过的验证失败会自动尝试刷新的函数。
    """
    # 保留使用__str__()可能
    if refresh_callback_function_name == '__str__':
        raise AssertionError('No refresh function indicated. ')
    if refresh_callback_function_name is None:
        refresh_callback_function_name = '__str__'

    def wrapper0(func):
        def wrapper1(*args, **kw):
            retv0 = (cls_getvalidvalue(value_on_failure))(func)
            retv1 = retv0(*args, **kw)
            if retv1 == value_on_failure:
                self = args[0]  # 这一行是必须存在的，用于向locals添加变量，或者换成args[0]。
                refresh_callback = eval(f'self.{refresh_callback_function_name}')
                # print(f'refresh_callback: {refresh_callback}')
                refresh_callback.__call__()
                return func(*args, **kw)
            return retv1
        return wrapper1
    return wrapper0


class timelimtited_cache:
    # __valid: bool = False
    _lasttime: Union[float, None] = None
    _validtime: Union[float, int, str, None] = None
    _validtime_min: Union[float, int] = 1
    _validtime_v_none_disabled = True

    @property
    def valid(self):
        if self._lasttime is None:
            return False
        if type(self._validtime) is str:
            if self._validtime == 'infinite':
                return True and (self._lasttime is not None)
            elif self._validtime == 'none':
                if self._validtime_v_none_disabled is True:
                    self._validtime = self._validtime_min
                else:
                    return False

        if self._validtime == 'min':
            self._validtime = self._validtime_min

        now = time.time()

        if type(self._validtime) is float or type(self._validtime) is int:
            period = now - self._lasttime
            if period < self._validtime:
                return True
        return False

    @valid.setter
    def valid(self, data: bool):
        """ 手动设置可用状态，这将可能会禁用过期验证。

        :param data: 可用状态，True/False
        :return: 无
        """
        # self.__valid = data
        if data is True:
            self._validtime = 'infinite'
        else:
            if self._validtime_v_none_disabled is True:
                self._validtime = self._validtime_min
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
                    if data == 'min':
                        data = self._validtime_min
                    elif data != 'infinite' and data != 'none':
                        raise ValueError(
                            'String type value "{string}" is illegal. Only "infinite" and "none" are allowed. '.format(
                                string=data))
                    pass
        self._validtime = data
        pass
