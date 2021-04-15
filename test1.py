import pyupbit
import math
import auth

upbit = pyupbit.Upbit(auth.access, auth.secret)

coin = "KRW-BTC"
count = 5
interval = "minute15"
fees = 0.0005

af = [{'uuid': '0694def7-5ada-405f-b0f3-053801d5b190',
  'side': 'ask',
  'ord_type': 'market',
  'price': None,
  'state': 'done',
  'market': 'KRW-LTC',
  'created_at': '2021-03-21T14:43:40+09:00',
  'volume': '0.07336815',
  'remaining_volume': '0.0',
  'reserved_fee': '0.0',
  'remaining_fee': '0.0',
  'paid_fee': '8.39331636',
  'locked': '0.0',
  'executed_volume': '0.07336815',
  'trades_count': 1},
 {'uuid': '48d6d451-3db5-4357-9d5a-bfb8f417c943',
  'side': 'ask',
  'ord_type': 'limit',
  'price': '230000.0',
  'state': 'done',
  'market': 'KRW-LTC',
  'created_at': '2021-03-17T01:06:55+09:00',
  'volume': '0.5',
  'remaining_volume': '0.0',
  'reserved_fee': '0.0',
  'remaining_fee': '0.0',
  'paid_fee': '58.775',
  'locked': '0.0',
  'executed_volume': '0.5',
  'trades_count': 2}]

#print(af[1]['uuid'])
for i in af :
    print(i['uuid'])