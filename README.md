# 🎧 yt2mp3 - YouTube 音樂下載與轉檔工具

本專案是一個輕量級的 YouTube 音樂下載與轉檔工具，使用 `yt-dlp` 下載音訊，並自動透過內建的 `static-ffmpeg` 將其轉檔為高品質的音訊格式（如 MP3、FLAC、WAV 等）。

## ✨ 特色功能

- **預設整組清單下載**：只要輸入播放清單網址，預設會自動下載整組播放清單。
- **清單範圍下載**：支援指定下載範圍（例如下載第 `1-10` 首，或特定歌曲如 `1,3,5`）。
- **自動分類儲存**：下載播放清單時，會自動讀取清單名稱並建立同名子資料夾進行分類儲存。
- **即時進度與歌名顯示**：在下載每首歌曲前會先印出歌名，並提供包含速度、預估時間的進度列，讓您隨時掌握進度。
- **免手動安裝 FFmpeg**：採用 `static-ffmpeg` 技術，首次執行時會自動在背景下載並配置適合您作業系統的影音轉換程式，省去繁瑣的環境變數設定。
- **防重複下載**：內建 `downloaded.txt` 紀錄檔，再次下載相同影片或清單時會自動跳過已下載的檔案，節省流量。

## 🛠️ 安裝步驟

本專案已配置好虛擬環境與套件清單，請在新電腦上執行以下步驟進行安裝：

1. **複製檔案**：將 `yt2mp3.py`、`requirements.txt` 和 `yt2mp3.bat` 複製到新電腦的資料夾中。
2. **建立虛擬環境**：開啟終端機（如 Git Bash 或命令提示字元）進入該資料夾，執行：
   ```bash
   python -m venv venv
   ```
3. **安裝依賴套件**：執行以下指令安裝所需套件：
   ```bash
   # Windows 命令提示字元 (CMD/PowerShell)
   .\venv\Scripts\python -m pip install -r requirements.txt

   # Git Bash 終端機
   ./venv/Scripts/python -m pip install -r requirements.txt
   ```

## ⚙️ 常用指令與使用方法

### 1. 互動模式（最推薦）
- **雙擊執行** `yt2mp3.bat`，或是直接在終端機中執行：
  ```bash
  .\yt2mp3.bat
  ```
- 系統會提示您貼上 YouTube 網址，並詢問是否下載整組清單、下載範圍、音訊格式及音質，非常直覺。

### 2. 單一影片下載
直接下載指定影片並轉換為預設的 MP3（192kbps）格式：
```bash
.\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼"
```

### 3. 下載指定影片並自訂檔名
```bash
.\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼" -o "自訂歌名.mp3"
```

### 4. 下載整個播放清單
只要輸入播放清單網址，預設即為下載整組清單，並會建立以清單標題為名的資料夾：
```bash
.\yt2mp3.bat -u "https://www.youtube.com/playlist?list=清單代碼"
```

### 5. 下載播放清單的指定範圍
只下載清單中第 1 到第 10 首的歌曲：
```bash
.\yt2mp3.bat -u "https://www.youtube.com/playlist?list=清單代碼" -r "1-10"
```

### 6. 自訂格式與音質
下載影片並轉換為 FLAC 格式、最高品質 320kbps：
```bash
.\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼" -f flac -q 320
```

### 7. 下載清單中的單一影片（不下載整組清單）
如果您輸入播放清單網址，但只想下載清單中的第一首歌曲：
```bash
.\yt2mp3.bat -u "https://www.youtube.com/playlist?list=清單代碼" --no-playlist
```

## 📝 專案結構與版本控制

為了保持專案乾淨，已設定 `.gitignore` 過濾規則，請避免將以下檔案上傳至您的 GitHub 儲存庫：
- `venv/`（本機虛擬環境）
- `music/`（下載的音樂資料夾）
- `downloaded.txt`（下載歷史紀錄檔）
- 所有 `.mp3` 等實體音訊檔案
