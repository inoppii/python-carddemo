import os
import re

for root, dirs, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
                if "Optional" in content and "from typing import" in content:
                    if "Optional" not in re.search(r"from typing import.*", content).group():
                        print(f"File missing Optional in typing import: {path}")
                elif "Optional" in content and "import typing" not in content:
                     print(f"File missing typing import for Optional: {path}")
