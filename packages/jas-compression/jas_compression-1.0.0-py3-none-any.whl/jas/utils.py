# jas/utils.py
import json
import struct

def write_binary_file(path, header_dict, binary_data):
    header_json = json.dumps(header_dict, separators=(",", ":"))
    header_bytes = header_json.encode("utf-8")
    with open(path, "wb") as f:
        f.write(struct.pack(">I", len(header_bytes)))
        f.write(header_bytes)
        f.write(binary_data)

def read_binary_file(path):
    with open(path, "rb") as f:
        header_len = struct.unpack(">I", f.read(4))[0]
        header_bytes = f.read(header_len)
        body = f.read()
    return header_bytes.decode("utf-8"), body

def minify_json(data):
    return json.dumps(data, separators=(",", ":"))