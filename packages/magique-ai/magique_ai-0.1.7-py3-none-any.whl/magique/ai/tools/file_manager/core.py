from pathlib import Path
import shutil
import base64

from ...toolset import ToolSet, tool


class FileManagerToolSetBase(ToolSet):
    def __init__(
            self,
            name: str,
            path: str | Path,
            worker_params: dict | None = None,
            ):
        super().__init__(name, worker_params)
        self.path = Path(path)

    @tool
    async def list_files(self, sub_dir: str | None = None) -> list[dict]:
        """List all files in the directory."""
        if not self.path.exists():
            return {"success": False, "error": "Directory does not exist"}
        if '..' in sub_dir:
            return {"success": False, "error": "Sub directory cannot contain '..'"}
        if sub_dir is None:
            files = list(self.path.glob("*"))
        else:
            files = list(self.path.glob(f"{sub_dir}/*"))
        return [
            {
                "name": file.name,
                "size": file.stat().st_size if file.is_file() else 0,
                "type": "file" if file.is_file() else "directory",
            }
            for file in files
        ]

    @tool
    async def create_directory(self, sub_dir: str):
        """Create a new directory."""
        if '..' in sub_dir:
            return {"success": False, "error": "Sub directory cannot contain '..'"}
        new_dir = self.path / sub_dir
        new_dir.mkdir(parents=True, exist_ok=True)
        return {"success": True}

    @tool
    async def delete_directory(self, sub_dir: str):
        """Delete a directory and all its contents recursively."""
        if '..' in sub_dir:
            return {"success": False, "error": "Sub directory cannot contain '..'"}
        dir_path = self.path / sub_dir
        if not dir_path.exists():
            return {"success": False, "error": "Directory does not exist"}
        
        shutil.rmtree(dir_path)
        return {"success": True}

    @tool
    async def delete_file(self, file_name: str):
        """Delete a file."""
        if '..' in file_name:
            return {"success": False, "error": "File name cannot contain '..'"}
        file_path = self.path / file_name
        if not file_path.exists():
            return {"success": False, "error": "File does not exist"}
        file_path.unlink()
        return {"success": True}


class FileManagerToolSet(FileManagerToolSetBase):
    @tool
    async def list_file_tree(self, sub_dir: str | None = None) -> list[dict]:
        """List all files in the directory recursively."""
        if not self.path.exists():
            return {"success": False, "error": "Directory does not exist"}
        if sub_dir and '..' in sub_dir:
            return {"success": False, "error": "Sub directory cannot contain '..'"}

        def _list_tree(path: Path) -> dict:
            """Helper function to recursively build the tree structure."""
            result = {
                "name": path.name,
                "type": "directory" if path.is_dir() else "file",
                "size": path.stat().st_size if path.is_file() else 0,
            }
            if path.is_dir():
                result["children"] = []
                for item in sorted(path.iterdir()):
                    result["children"].append(_list_tree(item))
            return result

        target_path = self.path / sub_dir if sub_dir else self.path
        if not target_path.exists():
            return {"success": False, "error": "Target directory does not exist"}

        return _list_tree(target_path)

    @tool
    async def read_file(self, file_name: str) -> dict:
        """Read a file."""
        if '..' in file_name:
            return {"success": False, "error": "File name cannot contain '..'"}
        file_path = self.path / file_name
        if not file_path.exists():
            return {"success": False, "error": "File does not exist"}
        with open(file_path, "r") as f:
            return {
                "success": True,
                "content": f.read(),
                "format": file_path.suffix.lower(),
            }

    @tool
    async def read_binary_file(self, file_name: str) -> dict:
        """Read a binary file."""
        if '..' in file_name:
            return {"success": False, "error": "File name cannot contain '..'"}
        file_path = self.path / file_name
        if not file_path.exists():
            return {"success": False, "error": "File does not exist"}
        with open(file_path, "rb") as f:
            return {
                "success": True,
                "content": f.read(),
                "format": file_path.suffix.lower(),
            }

    @tool
    async def display_image(self, image_path: str) -> dict:
        """Display an image. return the base64 encoded image."""
        if '..' in image_path:
            return {"success": False, "error": "Image path cannot contain '..'"}
        image_path = self.path / image_path
        if not image_path.exists():
            return {"success": False, "error": "Image does not exist"}
        format = image_path.suffix.lower()
        if format not in ["jpg", "jpeg", "png", "gif"]:
            return {"success": False, "error": "Image format must be jpg, jpeg, png or gif"}
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            data_uri = f"data:image/{format};base64,{b64}"
        return {
            "success": True,
            "data_uri": data_uri,
        }

    @tool
    async def write_file(self, file_name: str, content: str) -> dict:
        """Write to a file."""
        if '..' in file_name:
            return {"success": False, "error": "File name cannot contain '..'"}
        file_path = self.path / file_name
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
        return {"success": True}
