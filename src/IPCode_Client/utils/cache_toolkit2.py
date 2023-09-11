from typing import List, Any, Tuple, Union


class CacheBlock:
    cache_units: List[Any]

    @property
    def general_property(self):
        raise SyntaxError('This is a setter function and should never be called. ')

    @general_property.setter
    def general_property(self, _tuple0: Tuple[Union[str, Tuple], str, Any]):
        if len(_tuple0) < 3:
            raise SyntaxError('General Property Setter: 3 elements are expected, not {}'.format(len(_tuple0)))
        _tuple1: Union[str, Tuple] = _tuple0[0]
        _prop: str = _tuple0[-2]
        _value: Any = _tuple0[-1]
        if type(_tuple1) is str:
            _tuple1 = (_tuple1,)
        # print(f'_tuple1: {_tuple1}')
        # print(f'_prop: {_prop}')
        # print(f'_value: {_value}')
        # return
        indicator = _tuple1[0]
        if indicator == 'all':
            ttmp2 = self.cache_units
            pass
        elif indicator == 'index':
            ttmp = _tuple1[1:]
            if len(ttmp) == 0:
                raise RuntimeError('General Property Setter: missing indexes. ')
            ttmp = sorted(ttmp)
            if ttmp[-1] >= self.cache_units.__len__() or ttmp[0] < 0:
                raise ValueError('General Property Setter: Index {min_index}~{max_index} out of range'.format(
                    min_index=ttmp[0], max_index=ttmp[-1]))
            ttmp2 = [self.cache_units[x] for x in ttmp]
            pass
        else:
            raise ValueError('General Property Setter: "{indicator}" is not a valid indicator. '.format(
                indicator=indicator))

        # 实施
        for item in ttmp2:
            # print(item)
            exec(f'item.{_prop} = {_value}')

        return
