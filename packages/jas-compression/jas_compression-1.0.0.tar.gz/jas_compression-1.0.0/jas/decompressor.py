import json
import logging
from .utils import read_binary_file
from .huffman import rebuild_tree_from_freq_map, decode_tokens

logger = logging.getLogger(__name__)

def read_jas_file(input_path):
    header_data, binary_data = read_binary_file(input_path)
    header = json.loads(header_data)
    logger.info("Loaded header from file.")

    if header.get("version") != "JAS1.0":
        raise ValueError("Invalid .jas file")

    freq_map = header["freq"]
    specials = header.get("specials", {})

    logger.info("Rebuilding Huffman tree from frequency map.")
    tree = rebuild_tree_from_freq_map(freq_map)
    is_verbose = logger.isEnabledFor(logging.INFO)
    logger.info("Decoding tokens from binary data.")
    tokens = decode_tokens(binary_data, tree, verbose=is_verbose)

    reverse_specials = {v: k for k, v in specials.items()}
    text = "".join(reverse_specials.get(t, t) for t in tokens)
    logger.info("Decompression completed successfully.")
    return text