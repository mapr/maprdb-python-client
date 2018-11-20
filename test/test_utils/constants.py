from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from ojai.types.OTime import OTime
from ojai.types.OTimestamp import OTimestamp

URL = '192.168.33.11'
PORT = '5678'
AUTH = 'basic'
USER = 'mapr'
PASSWORD = 'mapr'
SSL = 'true'
SSL_CA = '/opt/mapr/conf/ssl_truststore.pem'
SSL_TARGET_NAME_OVERRIDE = 'node1.cluster.com'

CONNECTION_STR = 'ojai:mapr:thin:v1@{0}:{1}?auth={2};user={3};password={4};' \
                 'ssl={5};' \
                 'sslCA={6};' \
                 'sslTargetNameOverride={7}'.format(URL,
                                                    PORT,
                                                    AUTH,
                                                    USER,
                                                    PASSWORD,
                                                    SSL,
                                                    SSL_CA,
                                                    SSL_TARGET_NAME_OVERRIDE)

CONNECTION_OPTIONS = {
    'wait_exponential_multiplier': 5,
    'wait_exponential_max': 50,
    'stop_max_attempt_number': 5
}

# ===== CHECK AND DELETE / CHECK AND REPLACE / DELETE / INSERT REPLACE ======
DICT_STREAM = [{'_id': "id01", 'test_int': 51, 'test_str': 'strstr'},
               {'_id': 'id02', 'mystr': 'str', 'test_int': 51, 'test_str': 'strstr'},
               {'_id': 'id03', 'test_int': 51, 'test_otime': OTime(timestamp=1518689532), 'test_str': 'strstr'},
               {'_id': 'id04', 'test_int': 51, 'test_timestamp': OTimestamp(millis_since_epoch=29877132000),
                'test_str': 'strstr'},
               {'_id': 'id05', 'test_int': 51, 'test_bool': True, 'test_str': 'strstr'},
               {'_id': 'id06', 'test_int': 51, 'test_str': 'strstr'},
               {'_id': 'id07', 'test_int': 51, 'test_str': 'strstr'},
               {'_id': 'id08', 'test_int': 51, 'test_str': 'strstr', 'test_dict': {'test_int': 5}},
               {'_id': 'id09', 'test_int': 51, 'test_str': 'strstr', 'test_list': [5, 6]},
               {'_id': 'id10', 'test_int': 51, 'test_str': 'strstr', 'test_null': None}]

# ===== INSERT REPLACE =====
DICT_STREAM_REPLACE = [{'_id': "id01", 'test_int': 52, 'test_str': 'strstr'},
                       {'_id': 'id02', 'mystr': 'str', 'test_int': 51, 'test_str': 'strstr'},
                       {'_id': 'id03', 'test_int': 52, 'test_otime': OTime(timestamp=1518689532),
                        'test_str': 'strstr'},
                       {'_id': 'id04', 'test_int': 52,
                        'test_timestamp': OTimestamp(millis_since_epoch=29877132000),
                        'test_str': 'strstr'},
                       {'_id': 'id05', 'test_int': 52, 'test_bool': True, 'test_str': 'strstr'},
                       {'_id': 'id06', 'test_int': 52, 'test_str': 'strstr'},
                       {'_id': 'id07', 'test_int': 52, 'test_str': 'strstr'},
                       {'_id': 'id08', 'test_int': 52, 'test_str': 'strstr', 'test_dict': {'test_int': 5}},
                       {'_id': 'id09', 'test_int': 52, 'test_str': 'strstr', 'test_list': [5, 6]},
                       {'_id': 'id10', 'test_int': 52, 'test_str': 'strstr', 'test_null': None}]

# ===== UPDATE =====

DICT_STREAM_UPDATE = [{'_id': "id01", 'test_int': 51, 'test_str': 'strstr'},
                      {'_id': 'id02', 'mystr': 'str', 'test_int': 51,
                       'test_str': 'strstr'},
                      {'_id': 'id03', 'test_int': 51,
                       'test_otime': OTime(timestamp=1518689532),
                       'test_str': 'strstr'},
                      {'_id': 'id04', 'test_int': 51,
                       'test_timestamp': OTimestamp(
                           millis_since_epoch=29877132000),
                       'test_str': 'strstr'},
                      {'_id': 'id05', 'test_int': 51, 'test_bool': True,
                       'test_str': 'strstr'},
                      {'_id': 'id06', 'test_int': 51, 'test_str': 'strstr'},
                      {'_id': 'id07', 'test_int': 51, 'test_str': 'strstr'},
                      {'_id': 'id08', 'test_int': 51, 'test_str': 'strstr',
                       'test_dict': {'test_int': 5}},
                      {'_id': 'id09', 'test_int': 51, 'test_str': 'strstr',
                       'test_list': [5, 6]},
                      {'_id': 'id10', 'test_int': 51, 'test_str': 'strstr',
                       'test_null': None},
                      {'_id': 'id11', 'test_int': 51, 'test_str': 'strstr',
                       'test_dict': {'test_int': 5}}
                      ]
