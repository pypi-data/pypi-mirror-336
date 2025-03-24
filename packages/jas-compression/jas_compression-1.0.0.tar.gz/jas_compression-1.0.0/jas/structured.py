import json
import csv
import io
import xml.etree.ElementTree as ET
import yaml

def detect_file_type(text):
    text = text.strip()
    # Check for JSON
    if text.startswith('{') or text.startswith('['):
        try:
            json.loads(text)
            return "json"
        except:
            pass
    # Check for CSV
    if "," in text and "\n" in text:
        try:
            csv.Sniffer().sniff(text)
            return "csv"
        except:
            pass
    # Check for XML
    if text.startswith("<?xml") or text.startswith("<"):
        try:
            ET.fromstring(text)
            return "xml"
        except:
            pass
    # Check for YAML: Only consider it YAML if the parsed data is a dict or list.
    try:
        data = yaml.safe_load(text)
        if isinstance(data, (dict, list)):
            return "yaml"
    except:
        pass
    # Fallback to plain text
    return "plain"

def preprocess_json(text):
    try:
        obj = json.loads(text)
        return json.dumps(obj, sort_keys=True)
    except:
        return text

def preprocess_csv(text):
    try:
        f = io.StringIO(text)
        reader = csv.reader(f)
        rows = list(reader)
        rows.sort()
        return "\n".join([",".join(row) for row in rows])
    except:
        return text

def preprocess_xml(text):
    try:
        root = ET.fromstring(text)
        # Re-serialize the XML to a canonical form.
        return ET.tostring(root, encoding="unicode")
    except:
        return text

def preprocess_yaml(text):
    try:
        data = yaml.safe_load(text)
        # Dump back to YAML; some versions support sort_keys.
        return yaml.dump(data, sort_keys=True)
    except:
        return text

def preprocess_plain(text):
    # No normalization needed.
    return text

def preprocess_text(text, file_type):
    if file_type == "json":
        return preprocess_json(text)
    elif file_type == "csv":
        return preprocess_csv(text)
    elif file_type == "xml":
        return preprocess_xml(text)
    elif file_type == "yaml":
        return preprocess_yaml(text)
    else:
        return preprocess_plain(text)