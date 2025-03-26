import ctypes.wintypes
import os
import platform
from pathlib import Path

import yaml

if platform.system() == "Windows":
    import win32evtlog  # pyright: ignore # noqa: PGH003
    import win32evtlogutil  # pyright: ignore # noqa: PGH003

from vespricetracker.dto.bootstrap_paths_dto import BootstrapPathsDTO
from vespricetracker.exception.bootstrap_error import BootstrapError
from vespricetracker.util.static import Static


class FileImporter(Static):
    encoding = "utf-8"

    @staticmethod
    def bootstrap() -> BootstrapPathsDTO:
        try:
            home_folder = Path()
            system = platform.system()

            if system == "Windows":
                csidl_personal = 5
                shgfp_type_current = 0

                buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(  # pyright: ignore # noqa: PGH003
                    None, csidl_personal, None, shgfp_type_current, buf
                )
                home_folder = buf.value or ""
                if not home_folder:
                    description = "Could not locate Documents folder"
                    raise FileNotFoundError(description)  # noqa: TRY301
            elif system == "Linux":
                home_folder = os.getenv("HOME") or ""
            else:
                description = f"Unsupported OS: {system}"
                raise OSError(description)  # noqa: TRY301

            crcutil_dir = Path(home_folder) / "vespricetracker"
            log_dir = crcutil_dir / "log"

            crcutil_dir.mkdir(exist_ok=True)
            log_dir.mkdir(exist_ok=True)

            return BootstrapPathsDTO(log_dir=log_dir)

        except Exception as e:
            if platform.system == "Windows":
                win32evtlogutil.ReportEvent(  # pyright: ignore # noqa: PGH003
                    "plexutil",
                    eventID=1,
                    eventType=win32evtlog.EVENTLOG_ERROR_TYPE,  # pyright: ignore # noqa: PGH003
                    strings=[""],
                )
            if e.args and len(e.args) >= 0:
                raise BootstrapError(e.args[0]) from e

            raise BootstrapError from e

    @staticmethod
    def get_project_root() -> Path:
        """
        Gets the root of this project

        Returns:
            pathlib.Path: The project's root
        """
        return Path(__file__).parent.parent.parent

    @staticmethod
    def get_logging_config(logging_config_path: Path) -> dict:
        with logging_config_path.open(
            "r", errors="strict", encoding=FileImporter.encoding
        ) as file:
            return yaml.safe_load(file)
