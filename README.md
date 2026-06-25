# 🎧 yt2mp3 - YouTube 影音與音樂下載轉檔工具

本專案是一個輕量級的 YouTube 影音與音樂下載轉檔工具，支援下載為音樂（如 MP3、FLAC、WAV 等）或影片（如 MP4、MKV 等）格式。工具會自動透過內建的 `static-ffmpeg` 進行高品質轉檔與封裝，省去繁瑣的環境變數設定。

## ✨ 特色功能

- **支援音訊與影音下載**：可選擇純音樂（預設為 MP3）或影片檔案（預設為 MP4）。
- **自訂品質與自動降級**：
  - **音訊品質**：支援 128、192、256、320 kbps 等位元率選項（預設為通用且不失真的 192 kbps）。
  - **影片品質**：支援 480p、720p、1080p、2K、4K 等解析度選項（預設為 1080p）。若影片來源最高解析度低於選擇的值，系統會自動選取該來源的最高畫質下載。
- **預設整組清單下載**：只要輸入播放清單網址，預設會自動下載整組播放清單。
- **清單範圍下載**：支援指定下載範圍（例如下載第 `1-10` 首，或特定歌曲如 `1,3,5`）。
- **自動分類儲存**：
  - 音訊檔案預設儲存於 `./music` 資料夾中。
  - 影片檔案預設儲存於 `./video` 資料夾中。
  - 下載播放清單時，會自動建立以該清單標題為名的子資料夾進行分類儲存。
- **即時進度與歌名顯示**：在下載每首歌曲前會先印出歌名，並提供包含速度、預估時間的進度列。
- **免手動安裝 FFmpeg**：採用 `static-ffmpeg` 技術，首次執行時會自動在背景下載並配置適合您作業系統的影音轉換程式。
- **防重複下載**：再次下載相同影片或清單時，若目標檔案已存在，會自動跳過已下載的檔案，節省流量與時間。

---

## 💻 使用說明

### 安裝步驟

1. **複製檔案**：將專案檔案複製到新電腦的資料夾中。
2. **建立虛擬環境**：開啟終端機（如 Git Bash 或命令提示字元）進入該資料夾，執行：
   ```bash
   python -m venv venv
   ```
3. **安裝依賴套件**：
   ```bash
   # Windows 命令提示字元 (CMD/PowerShell)
   .\venv\Scripts\python -m pip install -r requirements.txt

   # Git Bash 終端機
   ./venv/Scripts/python -m pip install -r requirements.txt
   ```

### 常用指令

- **互動模式（最推薦）**：雙擊 `yt2mp3.bat`，或是直接在終端機中執行下方指令。系統將會引導您選擇下載類型（音訊/影片）、格式、品質與下載範圍：
  ```bash
  .\yt2mp3.bat
  ```
- **單一影片下載（預設為 MP3 音訊）**：
  ```bash
  .\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼"
  ```
- **單一影片下載（影音 MP4 影片）**：
  ```bash
  .\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼" -t video
  ```
- **自訂影片下載畫質（例如 720p）**：
  ```bash
  .\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼" -t video -q 720p
  ```
- **自訂儲存檔名**：
  ```bash
  .\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼" -o "自訂名稱.mp3"
  ```
- **下載整個播放清單**：
  ```bash
  .\yt2mp3.bat -u "https://www.youtube.com/playlist?list=清單代碼"
  ```
- **下載播放清單指定範圍**（例如第 1 到 10 首）：
  ```bash
  .\yt2mp3.bat -u "https://www.youtube.com/playlist?list=清單代碼" -r "1-10"
  ```

---

## 📝 專案結構與版本控制

為了保持專案乾淨，已設定 `.gitignore` 過濾規則，請避免將以下檔案上傳至您的 GitHub 儲存庫：
- `venv/`（本機虛擬環境）
- `music/`（下載的音訊資料夾）
- `video/`（下載的影片資料夾）
- 下載產生的音訊與影片實體檔案（如 `*.mp3`, `*.mp4`, `*.mkv`, `*.wav`, `*.flac` 等）
