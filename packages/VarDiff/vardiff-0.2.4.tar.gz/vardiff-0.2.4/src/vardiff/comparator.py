import json

class VarDiff:
    def __init__(self):
        pass

    def compare(self, a, b):
        """Compare two variables or files."""
        return self._compare_variables(a, b)

    def _compare_variables(self, a, b):
        """Compare two variables (numbers, strings, lists, dicts) and return differences."""
        if a == b:
            return True
        
        if type(a) != type(b):
            return json.dumps({
                "match": False,
                "reason": "Different data types",
                "type_a": str(type(a)),
                "type_b": str(type(b))
            }, indent=4)
        
        differences = {"match": False, "differences": []}

        if isinstance(a, list) and isinstance(b, list):
            for idx, (item_a, item_b) in enumerate(zip(a, b)):
                if item_a != item_b:
                    differences["differences"].append({
                        "index": idx,
                        "value_a": item_a,
                        "value_b": item_b
                    })
            if len(a) != len(b):
                differences["reason"] = "Lists have different lengths"
            return json.dumps(differences, indent=4)

        if isinstance(a, dict) and isinstance(b, dict):
            keys_a = set(a.keys())
            keys_b = set(b.keys())
            for key in keys_a.union(keys_b):
                if a.get(key) != b.get(key):
                    differences["differences"].append({
                        "key": key,
                        "value_a": a.get(key),
                        "value_b": b.get(key)
                    })
            return json.dumps(differences, indent=4)

        return json.dumps({
            "match": False,
            "value_a": a,
            "value_b": b
        }, indent=4)
