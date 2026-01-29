# Space Dodger (小飞船躲陨石)

用方向键操控小飞船躲避陨石，存活越久分数越高，失败后按 **R** 可重开。

## 运行

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python src/main.py
```

## 本地打包（Windows）

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole -n SpaceDodger src/main.py
```

生成的可执行文件在 `dist/SpaceDodger.exe`。

## GitHub Actions 打包与下载 exe

1. 推送代码到 GitHub。
2. 在仓库的 **Actions** 中运行 `Build Windows exe` workflow。
3. 构建完成后，在 workflow 详情页下载 `SpaceDodger-windows` artifact，里面包含 `SpaceDodger.exe`。
