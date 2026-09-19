"""Extract USB device history from the SYSTEM hive.

Implements a proper registry walk (via regipy) of:
  HKLM\\SYSTEM\\ControlSet001\\Enum\\USBSTOR
  HKLM\\SYSTEM\\ControlSet001\\Enum\\USB
and reports the instance path, FriendlyName, serial and the well-known
device property time stamps written by the USB hub / PnP manager:
    {83da6326-97a6-4088-9453-a1923f573b29}:0064 FirstInstallDate
    {83da6326-97a6-4088-9453-a1923f573b29}:0065 LastArrivalDate
    {83da6326-97a6-4088-9453-a1923f573b29}:0066 LastRemovalDate
Also lists MountedDevices for cross-referencing volume GUIDs.

Usage:
    uv run python scripts/extract_usbstor.py
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

from regipy import RegistryHive

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import ARTIFACTS  # noqa: E402

# Device property class for time stamps (PKEY_Device_FirstInstallDate etc.)
TIME_PROPERTIES = {
    "0064": "FirstInstallDate",
    "0065": "LastArrivalDate",
    "0066": "LastRemovalDate",
    "0067": "LocationInformation",
    "0068": "PropertyKeyDevice_LastArrival",
}

INSTALL_GUID = "{83da6326-97a6-4088-9453-a1923f573b29}"


def from_filetime(ft: int) -> str | None:
    # regipy decodes the QWORD FILETIME into a timezone-aware datetime in
    # recent versions; accept both the raw int and the pre-decoded datetime.
    if isinstance(ft, datetime):
        return ft.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    if not ft:
        return None
    try:
        return (
            datetime(1601, 1, 1, tzinfo=timezone.utc)
            + timedelta(microseconds=ft / 10)
        ).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    except Exception:
        return None


from datetime import timedelta  # noqa: E402


def walk_enum(hive: RegistryHive, enum_key: str) -> None:
    print(f"\n===== {enum_key} =====")
    for class_key in hive.get_key(enum_key).iter_subkeys():
        print(f"\n-- [class] {class_key.name}")
        for inst in class_key.iter_subkeys():
            friendly = inst.get_value("FriendlyName") or ""
            print(f"\n  [instance] {inst.name}")
            print(f"    FriendlyName      = {friendly}")
            for val in ("DeviceDescription", "Manufacturer", "SerialNumber"):
                v = inst.get_value(val)
                if v:
                    print(f"    {val:<18} = {v}")
            try:
                props = inst.get_subkey("Properties")
            except Exception:
                props = None
            if props is None:
                continue
            for pkey in props.iter_subkeys():
                if pkey.name.lower() != INSTALL_GUID.lower():
                    continue
                for vid in pkey.iter_subkeys():
                    label = TIME_PROPERTIES.get(vid.name, f"property-{vid.name}")
                    val = None
                    for v in vid.iter_values():
                        if v.name in ("(default)", ""):
                            val = v.value
                            break
                    ts = from_filetime(val) if isinstance(val, (int, datetime)) else val
                    print(f"    {label:<20} = {ts}   (raw {val})")
                    if label == "LastArrivalDate":
                        print(f"    DeviceInstance_Path? = {inst.name}")


def main() -> None:
    system = str(ARTIFACTS["SYSTEM"])
    hive = RegistryHive(system)
    walk_enum(hive, r"\ControlSet001\Enum\USBSTOR")
    walk_enum(hive, r"\ControlSet001\Enum\USB")


if __name__ == "__main__":
    main()