from pathlib import Path

replacements = {
    "README.md": [
        ("https://github.com/XiaoDuoYa/codex-with-chatgpt", "https://github.com/ksera2w1m-maker/codex-with-chatgpt"),
        ("vitest: 76 tests", "vitest: 93 tests"),
    ],
    "README.zh-CN.md": [
        ("https://github.com/XiaoDuoYa/codex-with-chatgpt", "https://github.com/ksera2w1m-maker/codex-with-chatgpt"),
        ("vitest：76 个测试", "vitest：93 个测试"),
    ],
}

for filename, pairs in replacements.items():
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in text:
            raise SystemExit(f"expected text not found in {filename}: {old}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

print("final documentation replacements applied")
