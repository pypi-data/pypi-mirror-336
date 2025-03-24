import uuid
from pathlib import Path

from ...toolset import ToolSet, tool


class FileManagerToolSet(ToolSet):
    def __init__(
            self,
            name: str,
            path: str | Path,
            worker_params: dict | None = None,
            ):
        super().__init__(name, worker_params)
        self.path = Path(path)
        self._handles = {}

    @tool
    async def list_files(self, sub_dir: str | None = None) -> list[dict]:
        """List all files in the directory."""
        if not self.path.exists():
            return {"error": "Directory does not exist"}
        if '..' in sub_dir:
            return {"error": "Sub directory cannot contain '..'"}
        if sub_dir is None:
            files = list(self.path.glob("*"))
        else:
            files = list(self.path.glob(f"{sub_dir}/*"))
        return [
            {
                "name": file.name,
                "size": file.stat().st_size,
                "type": "file" if file.is_file() else "directory",
            }
            for file in files
        ]

    @tool
    async def create_directory(self, sub_dir: str):
        """Create a new directory."""
        if '..' in sub_dir:
            return {"error": "Sub directory cannot contain '..'"}
        new_dir = self.path / sub_dir
        new_dir.mkdir(parents=True, exist_ok=True)
        return {"success": True}

    @tool
    async def delete_directory(self, sub_dir: str):
        """Delete a directory."""
        if '..' in sub_dir:
            return {"error": "Sub directory cannot contain '..'"}
        new_dir = self.path / sub_dir
        if not new_dir.exists():
            return {"error": "Directory does not exist"}
        new_dir.rmdir()
        return {"success": True}

    @tool
    async def delete_file(self, file_name: str):
        """Delete a file."""
        if '..' in file_name:
            return {"error": "File name cannot contain '..'"}
        file_path = self.path / file_name
        if not file_path.exists():
            return {"error": "File does not exist"}
        file_path.unlink()
        return {"success": True}

    @tool
    async def open_file_for_write(self, file_name: str):
        """Open a file for writing."""
        if '..' in file_name:
            return {"error": "File name cannot contain '..'"}
        file_path = self.path / file_name
        handle_id = str(uuid.uuid4())
        try:
            handle = open(file_path, "wb")
            self._handles[handle_id] = handle
            return {"success": True, "handle_id": handle_id}
        except Exception as e:
            return {"error": str(e)}

    @tool
    async def write_chunk(self, handle_id: str, data: bytes):
        """Write a chunk to a file."""
        if handle_id not in self._handles:
            return {"error": "Handle not found"}
        handle = self._handles[handle_id]
        handle.write(data)
        return {"success": True}

    @tool
    async def close_file(self, handle_id: str):
        """Close a file."""
        if handle_id not in self._handles:
            return {"error": "Handle not found"}
        handle = self._handles[handle_id]
        handle.close()
        del self._handles[handle_id]
        return {"success": True}

    @tool
    async def read_file(self, file_name: str, receive_chunk, chunk_size: int = 1024):
        """Read a file."""
        if '..' in file_name:
            return {"error": "File name cannot contain '..'"}
        file_path = self.path / file_name
        if not file_path.exists():
            return {"error": "File does not exist"}
        with open(file_path, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                await receive_chunk(data)
        return {"success": True}
