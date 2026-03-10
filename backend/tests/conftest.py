# Config inicial para testes
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


root = Path(__file__).resolve().parent.parent.parent
print("root-path-conftest", root)
sys.path.append(str(root))