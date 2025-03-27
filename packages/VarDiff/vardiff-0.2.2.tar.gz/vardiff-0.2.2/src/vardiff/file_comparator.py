import json

class FileDiff:
    def compare(self, file1_path, file2_path):
        """Compare two files line by line and return differences with line numbers."""
        differences = {"match": False, "file_differences": []}
        try:
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                for lineno, (line1, line2) in enumerate(zip(file1, file2), start=1):
                    if line1 != line2:
                        differences["file_differences"].append({
                            "line": lineno,
                            "line_a": line1.strip(),
                            "line_b": line2.strip()
                        })

                # Handling extra lines in files if they have different lengths
                for lineno, line in enumerate(file1, start=lineno+1):
                    differences["file_differences"].append({
                        "line": lineno, "line_a": line.strip(), "line_b": None
                    })

                for lineno, line in enumerate(file2, start=lineno+1):
                    differences["file_differences"].append({
                        "line": lineno, "line_a": None, "line_b": line.strip()
                    })

            if not differences["file_differences"]:
                return True

            return json.dumps(differences, indent=4)

        except FileNotFoundError as e:
            return json.dumps({
                "match": False,
                "error": str(e)
            }, indent=4)
