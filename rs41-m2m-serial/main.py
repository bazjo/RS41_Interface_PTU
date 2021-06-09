import re
import serial

from typing import Union
from typing import Tuple

CRC16_INITIAL_VALUE = 0xFFFF
CRC16_XOR_OUT = 0x0000
CRC16_POLYNOMIAL = 0x1021

M2M_FIELD_SEPARATOR = ' '
M2M_COMMAND_SEPARATOR = '\r'
M2M_VALID_RESPONSE_REGEX = '([0-F]{1,2}) (.{1,8}) ([0-F]+)(?: (.*))? ([0-F]{4})'
M2M_BODY_CRC_SEPARATION_REGEX = '([0-F]{1,2} .{1,8} [0-F]+(?: .*)?) (?:[0-F]{4})'


def crc16(data: bytes):
    xor_in = CRC16_INITIAL_VALUE  # initial value
    xor_out = CRC16_XOR_OUT  # final XOR value
    poly = CRC16_POLYNOMIAL  # generator polinom (normal form)

    reg = xor_in
    for octet in data:
        # reflect in
        for i in range(8):
            topbit = reg & 0x8000
            if octet & (0x80 >> i):
                topbit ^= 0x8000
            reg <<= 1
            if topbit:
                reg ^= poly
        reg &= 0xFFFF
        # reflect out
    return reg ^ xor_out


def encode_request(request_command_id: int, request_serial_no: str, request_payload: Union[int, str]) -> str:
    request_payload_string = str(request_payload)
    request_body = format(request_command_id, 'X') + M2M_FIELD_SEPARATOR \
                   + request_serial_no + M2M_FIELD_SEPARATOR \
                   + format(len(request_payload_string), 'X') + M2M_FIELD_SEPARATOR \
                   + request_payload_string
    request_crc = crc16(bytes(request_body, encoding='utf8'))
    request = request_body + M2M_FIELD_SEPARATOR + format(request_crc, 'X') + M2M_COMMAND_SEPARATOR

    return request


def decode_response(response: str,
                    correct_command_id=None, correct_serial_no=None,
                    check_command_id=True, check_serial_no=True) -> Tuple[int, str, int, str]:
    match = re.search(M2M_VALID_RESPONSE_REGEX, response)

    if match is None:
        raise ValueError('No Valid Response was found in the given String')

    response_body = re.search(M2M_BODY_CRC_SEPARATION_REGEX, response).group(1)

    response_command_id = int(match.group(1), 16)
    response_serial_no = match.group(2)
    response_payload_length = int(match.group(3), 16)
    response_payload = match.group(4)
    response_crc = int(match.group(5), 16)

    calculated_crc = crc16(bytes(response_body, encoding='utf8'))

    if not response_crc == calculated_crc:
        raise ValueError('Mismatch Between Received Response Body and CRC indicating a Transmission Error')

    if check_command_id and correct_command_id != response_command_id:
        raise ValueError('Received Command ID does not match provided Reference')

    if check_serial_no and correct_serial_no != response_serial_no:
        raise ValueError('Received Serial Number does not match provided Reference')

    return response_command_id, response_serial_no, response_payload_length, response_payload


if __name__ == '__main__':
    port = '/dev/ttyACM0'
    serial = serial.Serial(port, 9600)

    print(serial.name)  # check which port was really used
    serial.write(b'hello')  # write a string
    serial.close()

    request = encode_request(0x31, 'P0110001', 4)

    print('Request:', request)

    command_id, serial_no, payload_length, payload = decode_response(request,
                                                                     check_command_id=False,
                                                                     check_serial_no=False)

    print('Response:', command_id, serial_no, payload_length, payload)
