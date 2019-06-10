import re
from .backend_object import BackendObject
from .bv import BVV


class StringV(BackendObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'StringV(%s)' % (self.value)


def StrConcat(*args):
    """
    Create a concrete version of the concatenated string.

    :param args:                    list of string that has to be concatenated

    :return:                        a concrete version of the concatenated string
    """
    new_value = ''.join([arg.value for arg in args])
    return StringV(new_value)


def StrSubstr(start_idx, count, initial_string):
    """
    Create a concrete version of the substring.

    :param start_idx:               starting index of the substring
    :param count:                   length of the substring in bytes
    :param initial_string:          original string

    :return:                        a concrete version of the substring
    """
    new_value = initial_string.value[start_idx.value:start_idx.value + count.value]
    return StringV(new_value)


def StrExtract(high, low, str_val):
    return StrSubstr(low, high + 1 - low, str_val)


def StrReplace(initial_string, pattern_to_be_replaced, replacement_pattern):
    """
    Create a concrete version of the replaced string.
    (replace ONLY the first occurrence of the pattern)

    :param initial_string:          string in which the pattern needs to be replaced
    :param pattern_to_be_replaced:  substring that has to be replaced inside initial_string
    :param replacement_pattern:     pattern that has to be inserted in initial_string to replace
                                    pattern_to_be_replaced

    :return:                        a concrete representation of the replaced string
    """
    new_value = initial_string.value.replace(pattern_to_be_replaced.value,
                                             replacement_pattern.value,
                                             1)
    return StringV(new_value)


def StrLen(input_string, bitlength):
    """
    Return length of the string in bytes.

    :param input_string:            the string we want to calculate the length
    :param bitlength:               length of the bitvector representing the length of the string

    :return:                        bitvector holding the size of the string in bytes
    """
    return BVV(len(input_string.value), bitlength)


def StrContains(input_string, substring):
    """
    Check if substring is contained in input_string.

    :param input_string:            the string we want to check
    :param substring:               the string we want to check if it's contained inside the
                                    input_string

    :return:                        True if substring is contained in input_string else False
    """
    return substring.value in input_string.value


def StrPrefixOf(prefix, input_string):
    """
    Check if input_string starts with prefix.

    :param prefix:                  prefix we want to check
    :param input_string:            the string we want to check

    :return:                        True if the input_string starts with prefix else False
    """
    return re.match(r'^' + prefix.value, input_string.value) is not None


def StrSuffixOf(suffix, input_string):
    """
    Check if input_string ends with suffix.

    :param suffix:                  suffix we want to check
    :param input_string:            the string we want to check

    :return :                       True if the input_string ends with suffix else False
    """
    return re.match(r'.*' + suffix.value + '$', input_string.value) is not None


def StrIndexOf(input_string, substring, startIndex, bitlength):
    """
    Return the index of the first occurrence of substring at or after the startIndex, or -1 if it
    is not found.

    :param input_string:            the string we want to check
    :param substring:               the substring we want to find the index
    :param startIndex:              the index to start searching at
    :param bitlength:               length of the bitvector representing the index of the substring

    :return BV:                     index of the substring or -1 in bitvector
    """
    try:
        s = input_string.value
        t = substring.value
        i = startIndex.value
        return BVV(i + s[i:].index(t), bitlength)
    except ValueError:
        return BVV(-1, bitlength)


def StrToInt(input_string, bitlength):
    """
    Return the integer representation of the string.

    :param input_string:            the string we want to transform in an integer
    :param bitlength:               length of the bitvector representing the index of the substring

    :return BV:                     bitvector of the integer resulting from the string or -1 in
                                    bitvector if the string cannot be transformed into an integer
    """
    try:
        return BVV(int(input_string.value), bitlength)
    except ValueError:
        return BVV(-1, bitlength)


def StrIsDigit(input_string):
    """
    Determine whether the given string is entirely numeric.

    :param input_string:            the string we want to check

    :return:                        True if the string is entirely numeric otherwise False
    """
    return input_string.value.isdigit()


def IntToStr(input_bvv):
    """
    Return the string representation of the integer.

    :param input_bvv:               the integer expressed as a string

    :return:                        the string representation of the integer
    """
    return StringV(str(input_bvv.value))
