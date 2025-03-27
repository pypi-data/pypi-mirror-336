from io import BytesIO

from ios_device.util.kperf_data import KperfData


with open('trace_codes','rb') as f:

    data = BytesIO(f.read())
    for i in KperfData()._parse_v2(data):
        print(i)