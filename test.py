# from aenum import enum
# from enum import Enum

# from struct import *
# t = long(2555)
# # a = bytearray(t)
# a = pack('h', t)
# print(a)
# g = unpack('h', a)[0]
# print(g)
# print(type(g))
# g = unpack('<H', a)[0]

# Numbers = enum('ZERO', 'ONE', 'TWO')
#
# print(Numbers.ZERO)
#
# def bytes_to_int(bytes):
#     result = 0
#
#     for b in bytes:
#         result = result * 256 + int(b)
#
#     return result
#
# def int_to_bytes(value, length):
#     result = []
#
#     for i in range(0, length):
#         result.append(value >> (i * 8) & 0xff)
#
#     result.reverse()
#
#     return result

# r = int_to_bytes(str(55), str(55).__len__())
# print(r)

# test = 55
#
# for i in range(0, 5):
#     print(55 >> (i * 8) & 0xff)
#

# b = '%3$#sd'.encode()
# print  type(b)
# g = b.decode()
# print b
# print g

# ($s1.start == null ? ($s2.start == null ? null : $s2.seg) : $s1.seg)
# g = True
# s = 13
# b = None if $s1.start is None and $s2.start is None else $s2.seg if $s1.start is None and $s2.start is not None else $s1.seg
# s = None
##############################################################


# ($s1.start == null ? ($s2.start == null ? null : $s2.seg) : $s1.seg)

# b = None if $s1.start is None and $s2.start is None else $s2.seg if $s1.start is None and $s2.start is not None else $s1.seg
# print(b)

# from ojai.values.Value import ValueType
#
# a = ValueType.FLOAT
# b = ValueType.INT
# c = ValueType.DECIMAL
# d = ValueType.DATE
#
# print(type(a))
# print(type(b))
# print(type(c))
# print(type(d))


# from entity.values.Value import ValueType
#
# b = True
#
# a = long(1) if b else long(0)
# q = ValueType.TIMESTAMP
#
#
#
#
# print(type(q))
# print(isinstance(q, ValueType))
#
# if isinstance(b, bool):
#     print("bool")
#
# print(a)
# print(type(a))

# class Animal(Enum):
#     ant = 1
#     bee = 2
#     cat = 3
#     dog = 4
#
# print(Animal.ant)
# print(Animal.cat)


# g = dateutil.parser.parse("1970-01-01 12:12:12")

# print(g)

# import datetime
# import time
#
# import dateutil.parser
# # yourdate = dateutil.parser.parse("1970-01-01T16:15:00").time()
# yourdate = datetime.datetime.fromtimestamp(63479.6).time()
# # yourtime = yourdate.time()
# test = yourdate.strftime("%H:%M:%S:%f")
#
# print(type(yourdate))
# print(yourdate)
# print(test)
# # print(type(yourtime))


# print(yourdate)
# print(type(yourdate))
# print(yourdate.time())
# print(type(yourdate.time()))
# a = long((yourtime.hour * 60 * 60 + yourtime.second) * 1000 + yourtime.microsecond / 1000.0)
#
#
# print(a)


# date = datetime.datetime(2015, 1, 25)
# date2 = datetime.datetime.fromtimestamp(54332325)
# # dt = datetime.datetime()
# # datetime.datetime.fromtimestamp(self.__days_since_epoch)
#
# print date
# print date2
# # print date - date2
#
# EPOCH_DATE = datetime.datetime(1970, 1, 1)
# date = datetime.datetime(2018, 1, 5)
# days_since_epoch = (date - EPOCH_DATE).days
#
# print(EPOCH_DATE)
# print(date.strftime('%Y-%m-%d'))"%H:%M:%S:%f"
# print(days_since_epoch)
#
#
# # b = EPOCH_DATE + datetime.datetime.fromtimestamp(days_since_epoch)
# g = EPOCH_DATE.date()
# g2 = EPOCH_DATE.today()
# b = EPOCH_DATE + datetime.timedelta(days_since_epoch)
#
# print(g)
# print(g2)
# # print(b)
# def a(l):
#     print(l)
#
# def f(x):
#     a(lambda x: x**2)
#
#
# f(4)
# from mapr.ojai.o_types.OInterval import OInterval
#
# b = OInterval(milli_seconds=300)
# print(b)

# sss = "testte"
#
# for index in range(len(sss)):
#     print(str(index) + " : " + sss[index])

ch = '"'
# if ch in any(x == ch for x in ['"', '`', '\\', '/', '.', '[', ']']):
if any(x == ch for x in ['"', '`', '\\', '/', '.', '[', ']']):
    print("hohoho")