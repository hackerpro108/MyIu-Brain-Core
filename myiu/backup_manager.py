# myiu/backup_manager.py
import asyncio
import os
import tarfile  # Để nén file
import uuid  # Để tạo ID duy nhất cho backup
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, TYPE_CHECKING

from myiu.base_module import AsyncModule
    ThoughtChunkModel,
    ThoughtIntent,
    ThoughtSentiment,
)  # Cần để phát Thought về trạng thái backup  # TODO: Refactor long line

# Thư viện Google Drive API - sẽ được xử lý bởi try-except để không gây crash nếu thiếu  # TODO: Refactor long line  # TODO: Refactor long line
try:
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive

    PYDRIVE_INSTALLED = True
except ImportError:
    PYDRIVE_INSTALLED = False
    logging.getLogger(__name__).warning(
"PyDrive2 is not installed. BackupManager will operate in a simulated mode."  # TODO: Refactor long line
    )  # TODO: Refactor long line


if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.thought_streamer import ThoughtStreamer

logger = logging.getLogger(__name__)


class BackupManager(AsyncModule):
    """
    Tự động nén và đẩy backup dữ liệu của MyIu lên Google Drive.
    """

    def __init__(
        self,
        event_bus: "EventBus",
        thought_streamer: "ThoughtStreamer",  # TODO: Refactor long line
        interval_hours: int = 1,
        creds_file_path: str = "mycreds.txt",
        backup_folder_name: str = "MyIu_Backups",
        max_backups_to_keep: int = 5,
    ):  # Tiêm đầy đủ phụ thuộc  # TODO: Refactor long line
        super().__init__()
# Module này sẽ chạy nền nếu PyDrive được cài đặt, hoặc giả lập nếu không  # TODO: Refactor long line  # TODO: Refactor long line
        self.is_background_service = True
        self.event_bus = event_bus
        self.thought_streamer = thought_streamer

        self.drive: Optional[GoogleDrive] = None
        self.backup_interval = timedelta(hours=interval_hours)
self.creds_file_path = creds_file_path  # Đường dẫn tới file mycreds.txt  # TODO: Refactor long line
        self.backup_folder_name = backup_folder_name
        self.max_backups_to_keep = max_backups_to_keep
        self.last_backup_time: Optional[datetime] = None

        if not PYDRIVE_INSTALLED:
            logger.warning(
"BackupManager: 'PyDrive2' is not installed. BackupManager will be disabled and run in simulated mode."  # TODO: Refactor long line
            )  # TODO: Refactor long line
self.is_background_service = False  # Tắt dịch vụ nền nếu không có PyDrive  # TODO: Refactor long line  # TODO: Refactor long line
        else:
            logger.info(
f"BackupManager: Initialized (backup every {interval_hours} hour(s))."  # TODO: Refactor long line
            )  # TODO: Refactor long line

    async def _setup_async_tasks(self):
        """Thiết lập tác vụ nền để chạy backup định kỳ."""
        if not PYDRIVE_INSTALLED:
            logger.warning(
"BackupManager: PyDrive2 not installed, skipping async tasks setup."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            return

        # Xác thực Google Drive API
        gauth = GoogleAuth()
        # Cố gắng tải credentials từ file
        if os.path.exists(self.creds_file_path):
            gauth.LoadCredentialsFile(self.creds_file_path)

        if gauth.credentials is None:
            # Nếu không có credentials hoặc hết hạn, thực hiện xác thực lại
            # Đây thường yêu cầu tương tác người dùng qua trình duyệt,
# nên sẽ gặp khó khăn trên VPS. Cần tạo file mycreds.txt từ máy cục bộ.  # TODO: Refactor long line  # TODO: Refactor long line
            logger.error(
f"BackupManager: No valid credentials found at '{self.creds_file_path}'. Please ensure it exists and is valid. Backups will not run."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            self.is_background_service = (
False  # Vô hiệu hóa nếu không xác thực được  # TODO: Refactor long line  # TODO: Refactor long line
            )
            return
        elif gauth.access_token_expired:
            logger.info(
"BackupManager: Google Drive Access Token expired. Refreshing..."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            gauth.Refresh()
            gauth.SaveCredentialsFile(self.creds_file_path)
            logger.info("BackupManager: Access Token refreshed.")
        else:
            logger.info(
                "BackupManager: Google Drive credentials loaded successfully."
            )  # TODO: Refactor long line

        self.drive = GoogleDrive(gauth)

        self.add_task(self._start_backup_loop(), name="periodic_backup_loop")
        logger.info("BackupManager: Periodic backup loop started.")

        # Lắng nghe các sự kiện cần backup khẩn cấp
        self.event_bus.subscribe(
            "critical_data_change", self._handle_critical_data_change
        )  # TODO: Refactor long line
        logger.info(
"BackupManager: Subscribed to 'critical_data_change' for urgent backups."  # TODO: Refactor long line
        )  # TODO: Refactor long line

    async def _start_backup_loop(self):
        """Vòng lặp chính để thực hiện backup định kỳ."""
        while (
            self._running and self.is_background_service
        ):  # Chỉ chạy nếu service được kích hoạt  # TODO: Refactor long line
            await asyncio.sleep(self.backup_interval.total_seconds())
            logger.info("BackupManager: Running periodic backup...")
            await self.perform_backup()

    async def _handle_critical_data_change(self, message: Dict[str, Any]):
"""Xử lý sự kiện thay đổi dữ liệu quan trọng, kích hoạt backup khẩn cấp."""  # TODO: Refactor long line  # TODO: Refactor long line
        logger.warning(
f"BackupManager: Received critical data change event: {message.get('type')}. Initiating urgent backup."  # TODO: Refactor long line
        )  # TODO: Refactor long line
        await self.perform_backup(is_urgent=True)

    async def perform_backup(self, is_urgent: bool = False):
        """Thực hiện quy trình backup."""
        if not self.is_background_service:
            logger.warning(
                "BackupManager: Backup service is disabled. Skipping backup."
            )  # TODO: Refactor long line
            return
        if not self.drive:
            logger.error(
"BackupManager: Google Drive not authenticated. Skipping backup."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            await self._publish_backup_thought(
False, "Google Drive authentication failed. Cannot perform backup."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            return

        current_time = datetime.utcnow()
        if (
            not is_urgent
            and self.last_backup_time
            and (current_time - self.last_backup_time) < self.backup_interval
        ):  # TODO: Refactor long line
            logger.debug("BackupManager: Skipping periodic backup, too soon.")
            return

        logger.info("BackupManager: Starting data backup process...")
backup_file_name = f"MyIu_Brain_Core_Backup_{current_time.strftime('%Y%m%d_%H%M%S')}.tar.gz"  # TODO: Refactor long line  # TODO: Refactor long line
        backup_path = f"/tmp/{backup_file_name}"  # Lưu tạm vào /tmp

        # Danh sách các thư mục/file cần backup
        # Cần đảm bảo các đường dẫn này là chính xác trên VPS
        files_to_backup = [
            "genome_dynamic.json",
            "genome_static.json",
"data/memory_vector.db",  # Nếu memory_vector.db vẫn được dùng như file backup của postgres, hoặc thay bằng dump của DB  # TODO: Refactor long line  # TODO: Refactor long line
            "data/reflection_log.txt",
            "myiu/",  # Thư mục mã nguồn MyIu (không có myiu_env)
        ]

        # Đảm bảo thư mục 'data' tồn tại
        os.makedirs("data", exist_ok=True)

        try:
            # Tạo file tar.gz
            with tarfile.open(backup_path, "w:gz") as tar:
                for file_or_dir in files_to_backup:
                    if os.path.exists(file_or_dir):
                        tar.add(
                            file_or_dir, arcname=os.path.basename(file_or_dir)
                        )  # TODO: Refactor long line
                        logger.debug(
                            f"BackupManager: Added {file_or_dir} to archive."
                        )  # TODO: Refactor long line
                    else:
                        logger.warning(
f"BackupManager: Path {file_or_dir} not found for backup."  # TODO: Refactor long line
                        )  # TODO: Refactor long line

            logger.info(
f"BackupManager: Archive created at {backup_path}. Uploading to Google Drive..."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            await self._upload_to_google_drive(backup_path, backup_file_name)

            self.last_backup_time = current_time
            logger.info(
                "BackupManager: Backup process completed successfully."
            )  # TODO: Refactor long line
            await self._publish_backup_thought(
                True, f"Backup completed: {backup_file_name}."
            )  # TODO: Refactor long line

        except Exception as e:
            logger.error(
f"BackupManager: Error during backup process: {e}", exc_info=True  # TODO: Refactor long line
            )  # TODO: Refactor long line
            await self._publish_backup_thought(False, f"Backup failed: {e}.")
        finally:
            # Dọn dẹp file tạm
            if os.path.exists(backup_path):
                os.remove(backup_path)
                logger.debug(
f"BackupManager: Cleaned up temporary backup file: {backup_path}."  # TODO: Refactor long line
                )  # TODO: Refactor long line

    async def _upload_to_google_drive(self, file_path: str, file_name: str):
        """Tải file backup lên Google Drive."""
        # Kiểm tra và tạo thư mục backup trên Drive
        folder_list = self.drive.ListFile(
            {
"q": f"title='{self.backup_folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"  # TODO: Refactor long line
            }
        ).GetList()  # TODO: Refactor long line
        backup_folder = (
            folder_list[0]
            if folder_list
            else self.drive.CreateFile(
                {
                    "title": self.backup_folder_name,
                    "mimeType": "application/vnd.google-apps.folder",
                }
            ).Upload()
        )  # TODO: Refactor long line

        file_drive = self.drive.CreateFile(
            {"title": file_name, "parents": [{"id": backup_folder["id"]}]}
        )  # TODO: Refactor long line
        file_drive.SetContentFile(file_path)
        file_drive.Upload()
        logger.info(
            f"BackupManager: Upload successful. File ID: {file_drive['id']}"
        )  # TODO: Refactor long line

        # Quản lý các bản backup cũ
        file_list = self.drive.ListFile(
            {
                "q": f"'{backup_folder['id']}' in parents and trashed=false",
                "orderBy": "createdTime desc",
            }
        ).GetList()  # TODO: Refactor long line
        if len(file_list) > self.max_backups_to_keep:
            for old_file in file_list[self.max_backups_to_keep :]:
                old_file.Trash()
                logger.info(
                    f"BackupManager: Deleted old backup '{old_file['title']}'."
                )  # TODO: Refactor long line

    async def _publish_backup_thought(self, success: bool, message: str):
        """Tạo ThoughtChunk thông báo về trạng thái backup."""
# from myiu.models import ThoughtIntent, ThoughtSentiment # Import cục bộ  # TODO: Refactor long line  # TODO: Refactor long line
        intent = (
            ThoughtIntent.DATA_INTEGRITY_REFLECTION
            if success
            else ThoughtIntent.SYSTEM_ERROR
        )  #  # TODO: Refactor long line
        sentiment = (
            ThoughtSentiment.POSITIVE if success else ThoughtSentiment.NEGATIVE
        )  # TODO: Refactor long line

        await self.thought_streamer.publish_thought_chunk(
id=f"BACKUP-STATUS-{datetime.utcnow().isoformat('T', 'seconds')}-{uuid.uuid4().hex[:4]}",  # TODO: Refactor long line  # TODO: Refactor long line
            timestamp=datetime.utcnow(),
            content=f"Quản lý Backup: {message}",
            source="BackupManager",
            intent=intent,
            sentiment=sentiment,
            metadata={"backup_success": success, "message": message},
        )

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi BackupManager tắt."""
        if self._running and PYDRIVE_INSTALLED:
# Không cần unsubscribe EventBus vì đây là task nền có thể dừng linh hoạt  # TODO: Refactor long line  # TODO: Refactor long line
            logger.info("BackupManager: Cleanup complete.")
        await super().cleanup()
