from __future__ import annotations

from pathlib import Path


class DocsPackager:
    """检查一个交付包是否具备最小文档集合。"""

    required_docs = [
        "quickstart.md",
        "user-guide.md",
        "trainer-guide.md",
    ]

    def validate(self, docs_dir: Path) -> list[str]:
        if not docs_dir.exists():
            return ["docs/ 目录不存在"]
        missing = []
        for name in self.required_docs:
            if not (docs_dir / name).exists():
                missing.append(name)
        return missing
