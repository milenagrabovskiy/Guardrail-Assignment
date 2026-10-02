import sys
from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent / "app" / "MGLabAgent"
sys.path.insert(0, str(AGENT_DIR))