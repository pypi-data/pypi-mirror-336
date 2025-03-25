"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
import time
from datetime import datetime

from nomenclators_archetype.domain.loggers import default_logger as logger

tw_epoch = int(datetime.now().timestamp())

WORKER_ID_BITS = 5
DATA_CENTER_ID_BITS = 5
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
MAX_DATA_CENTER_ID = -1 ^ (-1 << DATA_CENTER_ID_BITS)
SEQUENCE_BITS = 12
WORKER_ID_SHIFT = SEQUENCE_BITS
DATA_CENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATA_CENTER_ID_BITS
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)


def snowflake_to_timestamp(_id):
    """convert a snowflake id to a timestamp"""

    _id = _id >> 22     # strip the lower 22 bits
    _id += tw_epoch     # adjust for twitter epoch
    _id = _id / 1000    # convert from milliseconds to seconds

    return _id


def generator(worker_id, data_center_id, sleep=lambda x: time.sleep(x / 1000.0)):
    """generate a snowflake id"""

    assert 0 <= worker_id <= MAX_WORKER_ID
    assert 0 <= data_center_id <= MAX_DATA_CENTER_ID

    last_timestamp = -1
    sequence = 0

    while True:
        timestamp = int(time.time() * 1000)

        if last_timestamp > timestamp:
            logger.warning(
                "clock is moving backwards. waiting until %s", last_timestamp)
            sleep(last_timestamp - timestamp)
            continue

        if last_timestamp == timestamp:
            sequence = (sequence + 1) & SEQUENCE_MASK
            if sequence == 0:
                logger.warning("sequence overrun")
                sequence = -1 & SEQUENCE_MASK
                sleep(1)
                continue
        else:
            sequence = 0

        last_timestamp = timestamp

        yield (((timestamp - tw_epoch) << TIMESTAMP_LEFT_SHIFT) | (data_center_id << DATA_CENTER_ID_SHIFT) |
               (worker_id << WORKER_ID_SHIFT) | sequence)


seq = generator(1, 1)
