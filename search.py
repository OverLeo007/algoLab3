"""
Модуль, реализующий поиск подстрок в строке,
при помощи алгоритма Бойера-Мура-Хорспула
"""


from typing import Union, Optional, Any


def find_offset(string: str) -> dict[str, int]:
    """
    Функция поиска таблицы сдвига для шаблона

    :param string: строка для которой создаем таблицу сдвигов
    :return: таблица сдвига
    """
    indexes = list(reversed(range(len(string) - 1, -1, -1)))
    res = []

    for i, char in enumerate(list(reversed(string))[1:]):
        if char not in map(lambda x: x[1], res):
            res.append((indexes[i + 1], char))
        else:
            res.append((res[list(map(lambda x: x[1], res)).index(char)][0], char))
    if string[-1] not in map(lambda x: x[1], res):
        res = [(len(string), string[-1])] + res
    else:
        res = [(res[list(map(lambda x: x[1], res)).index(string[-1])][0], string[-1])] + res
    tmp = list(reversed(res)) + [(len(res), "*")]
    res = {}
    for offset, char in tmp:
        if (char, offset) not in res.values():
            res[char] = offset
    return res


def compare(comp_str: str, inp_str: str, offset_table: dict[str, int]) -> int:
    """
    Функция сравнения части строки с подстрокой

    :param comp_str: часть строки
    :param inp_str: шаблон
    :param offset_table: таблица сдвигов для шаблона
    :return: кол-во элементов на которые нужно сдвинуть шаблон
    """
    if comp_str[-1] != inp_str[-1]:
        return offset_table[comp_str[-1]] \
            if offset_table.get(comp_str[-1], False) \
            else offset_table["*"]

    ptr = -2
    while len(inp_str) >= abs(ptr):
        if comp_str[ptr] != inp_str[ptr]:
            return offset_table[inp_str[ptr]]
        ptr -= 1
    return 0


def find_substr(string: str, sub_string: str) -> Optional[tuple[int, str]]:
    """
    Функция поиска первого вхождения шаблона в строку

    :param string: строка
    :param sub_string: шаблон
    :return: индекс вхождения
    """
    if len(sub_string) > len(string):
        return None
    offset_table = find_offset(sub_string)
    index = 0
    while True:
        if len(sub_string) > len(string):
            return None
        next_sym = compare(string[:len(sub_string)], sub_string, offset_table)
        index += next_sym
        string = string[next_sym:]
        if next_sym == 0:
            if len(sub_string) == 1:
                string = string[offset_table["*"]:]
            else:
                string = string[offset_table["*"] - 1:]
            break

    return index, string


def get_all_indexes(string: str, substring: str,
                    case_sensitivity: bool = False,
                    method: str = "first", count: Optional[int] = None) -> \
        Optional[tuple[Union[int, Any], ...]]:
    """
    Функция получения индексов всех вхождений шаблона в строку

    :param string: строка
    :param substring: шаблон
    :param case_sensitivity: чувствительность к регистру букв
    :param method: метод поиска, либо с начала, либо с конца
    :param count: количество найденных вхождений
    :return: индексы вхождений
    """
    indexes = []
    if not case_sensitivity:
        string = string.lower()
        substring = substring.lower()

    if method == "last":
        str_len = len(string)
        string = reverse_str(string)
        substring = reverse_str(substring)

    while string:
        if count is not None and len(indexes) >= count:
            break
        res = find_substr(string, substring)
        if res:
            index, string = res
            indexes.append(index + (indexes[-1] + len(substring) -
                                    int(len(substring) != 1) if indexes else 0))
        else:
            break
    if indexes:
        if method == "last":
            return tuple(map(lambda x: str_len - len(substring) - x, indexes))
        return tuple(indexes)
    return None


def reverse_str(string: str) -> str:
    """
    Функция разворота строки
    :param string: строка
    :return: развернутая строка
    """
    return ''.join(reversed(string))


def search(string: str, sub_string: Union[str, list[str]],
           case_sensitivity: bool = False,
           method: str = 'first',
           count: Optional[int] = None) -> \
        Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Функция поиска вхождений любого количества шаблонов в строку

    :param string: строка
    :param sub_string: шаблон(ы)
    :param case_sensitivity: чувствительность к регистру
    :param method: метод поиска (сначала либо с конца)
    :param count: количество найденных индексов подстрок для каждого шаблона
    :return: либо кортеж с индексами вхождений, если sub_string - str, либо словарь,
    где элементы (шаблон: кортеж с индексами вхождений), если sub_string - list
    """
    if isinstance(sub_string, str):
        return get_all_indexes(string, sub_string, case_sensitivity, method, count)
    res = {subs: get_all_indexes(string, subs, case_sensitivity, method, count)
           for subs in sub_string}
    if (rvals := list(res.values())).count(None) == len(rvals):
        return None
    return res


if __name__ == '__main__':
    print(search("aAbCbccaabc", "AbC", method="last", count=None, case_sensitivity=False))
    # print(compare("данные", "данные", find_offset("данные")))
