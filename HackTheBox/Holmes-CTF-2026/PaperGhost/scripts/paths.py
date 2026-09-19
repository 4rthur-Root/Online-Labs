"""Shared artifact paths for the PaperGhost (Sherlock 04) triage.

All paths are relative to the repository so the scripts stay reproducible.
"""

from pathlib import Path

PAPERGHOST = Path(__file__).resolve().parent.parent
TRIAGE = PAPERGHOST / "artifacts" / "Triage"
ANALYSIS = PAPERGHOST / "analysis"

ARTIFACTS = {
    "SYSTEM": TRIAGE / "C/Windows/System32/config/SYSTEM",
    "SOFTWARE": TRIAGE / "C/Windows/System32/config/SOFTWARE",
    "SAM": TRIAGE / "C/Windows/System32/config/SAM",
    "DEFAULT": TRIAGE / "C/Windows/System32/config/DEFAULT",
    "NTUSER_cvoss": TRIAGE / "C/Users/cvoss/NTUSER.DAT",
    "UsrClass_cvoss": TRIAGE / "C/Users/cvoss/AppData/Local/Microsoft/Windows/UsrClass.dat",
    "NTUSER_CyberJunkie": TRIAGE / "C/Users/CyberJunkie/NTUSER.DAT",
    "UsrClass_CyberJunkie": TRIAGE / "C/Users/CyberJunkie/AppData/Local/Microsoft/Windows/UsrClass.dat",
    "SRUDB": TRIAGE / "C/Windows/System32/SRU/SRUDB.dat",
    "WINDOWS_EDB": TRIAGE / "C/ProgramData/Microsoft/search/data/applications/windows/Windows.edb",
    "RECENT": TRIAGE / "C/Users/cvoss/AppData/Roaming/Microsoft/Windows/Recent",
}

ANALYSIS.mkdir(exist_ok=True)