import heapq
import itertools
from .bitstream import BitWriter, BitReader

# Global counter for deterministic tie-breaking.
_counter = itertools.count()

class Node:
    def __init__(self, token, freq):
        self.token = token
        self.freq = freq
        self.left = None
        self.right = None
        self.order = next(_counter)

    def __lt__(self, other):
        # Compare by frequency first; if equal, use the insertion order.
        if self.freq == other.freq:
            return self.order < other.order
        return self.freq < other.freq

def build_huffman_tree(freq_map):
    heap = [Node(token, freq) for token, freq in freq_map.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        parent = Node(None, lo.freq + hi.freq)
        parent.left, parent.right = lo, hi
        heapq.heappush(heap, parent)
    return heap[0] if heap else None

def build_codes(root):
    codes = {}
    def walk(node, path=""):
        if node.token is not None:
            codes[node.token] = path if path != "" else "0"
        else:
            walk(node.left, path + "0")
            walk(node.right, path + "1")
    walk(root)
    return codes

def encode_tokens(tokens, codes, verbose=False):
    writer = BitWriter()
    try:
        if verbose:
            from tqdm import tqdm
            tokens_iter = tqdm(tokens, desc="Encoding tokens")
        else:
            tokens_iter = tokens
    except ImportError:
        tokens_iter = tokens

    for token in tokens_iter:
        writer.write_bits(codes[token])
    return writer.get_bytes()

def decode_tokens(binary_data, tree, verbose=False):
    reader = BitReader(binary_data)
    output = []
    node = tree
    total = len(reader.bits)  # Total bits to process.
    if verbose:
        try:
            from tqdm import tqdm
            pbar = tqdm(total=total, desc="Decoding bits")
        except ImportError:
            pbar = None
    while not reader.is_end():
        bit = reader.read_bit()
        if verbose and pbar is not None:
            pbar.update(1)
        node = node.left if bit == "0" else node.right
        if node.token is not None:
            output.append(node.token)
            node = tree
    if verbose and pbar is not None:
        pbar.close()
    return output

def rebuild_tree_from_freq_map(freq_map):
    return build_huffman_tree(freq_map)