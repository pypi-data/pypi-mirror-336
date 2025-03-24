import json
import logging
from .tokenizer import smart_tokenize, weighted_frequencies
from .huffman import build_huffman_tree, build_codes, encode_tokens
from .utils import write_binary_file
from .structured import detect_file_type, preprocess_text

logger = logging.getLogger(__name__)

def write_jas_file(text, output_path):
    # Detect file type and normalize the text.
    filetype = detect_file_type(text)
    preprocessed_text = preprocess_text(text, filetype)
    
    # Tokenize the preprocessed text.
    tokens, specials = smart_tokenize(preprocessed_text)

    freq_map = weighted_frequencies(tokens)
    tree = build_huffman_tree(freq_map)
    codes = build_codes(tree)
    # Determine verbosity from the logger configuration.
    is_verbose = logger.isEnabledFor(logging.INFO)
    binary_data = encode_tokens(tokens, codes, verbose=is_verbose)

    # Build the header with metadata.
    header = {
        "version": "JAS1.0",
        "type": filetype,
        "freq": freq_map,
        "specials": specials,
        "preprocessed": True,
    }

    if is_verbose:
        logger.info(f"Detected file type: {filetype}")
        logger.info(f"Token count: {len(tokens)}")
        logger.info("Chunk count: 1")
        logger.info(f"Compression ratio: {round((1 - len(binary_data) / len(preprocessed_text.encode('utf-8'))) * 100, 2)}%")

    write_binary_file(output_path, header, binary_data)