import os
import tempfile
import unittest
from jas import compressor, decompressor

class TestJAS(unittest.TestCase):
    def test_roundtrip_plain_text(self):
        # Use a simple plain text input for testing
        original_text = (
            "This is a test of the JAS compression system. "
            "It should roundtrip correctly and produce the same text."
        )
        # Create temporary files for the compressed data
        with tempfile.NamedTemporaryFile(delete=False) as tmp_out:
            out_path = tmp_out.name

        try:
            # Compress the text
            compressor.write_jas_file(original_text, out_path)
            # Decompress the file
            result_text = decompressor.read_jas_file(out_path)
            # Assert that decompressed text equals the original
            self.assertEqual(result_text, original_text)
        finally:
            # Clean up temporary file
            os.unlink(out_path)

    def test_tokenizer_basic(self):
        # Test basic tokenization functionality
        from jas.tokenizer import smart_tokenize
        sample_text = "Hello, world! This is a test."
        tokens, specials = smart_tokenize(sample_text)
        # Ensure we get a non-empty list of tokens and an empty specials dict for this input
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)
        self.assertIsInstance(specials, dict)

if __name__ == "__main__":
    unittest.main()