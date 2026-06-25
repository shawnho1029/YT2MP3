# 🎧 yt2mp3 - YouTube 音樂下載與轉檔工具

本專案是一個輕量級的 YouTube 音樂下載與轉檔工具，使用 `yt-dlp` 下載音訊，並自動透過內建的 `static-ffmpeg` 將其轉檔為高品質的音訊格式（如 MP3、FLAC、WAV 等）。

專案同時提供**命令列/批次檔工具**以及**網頁版圖形介面**，方便您在不同環境下使用。

## ✨ 特色功能

- **預設整組清單下載**：只要輸入播放清單網址，預設會自動下載整組播放清單。
- **清單範圍下載**：支援指定下載範圍（例如下載第 `1-10` 首，或特定歌曲如 `1,3,5`）。
- **自動分類與壓縮下載**：
  - **批次檔版**：下載播放清單時，會自動建立以清單標題為名的子資料夾進行分類儲存。
  - **網頁版**：下載整個清單時，會自動將所有歌曲打包為以清單名稱命名的 ZIP 壓縮檔，並提供一鍵下載按鈕。
- **即時進度與歌名顯示**：在下載每首歌曲前會先印出歌名，並提供包含速度、預估時間的進度列。
- **免手動安裝 FFmpeg**：採用 `static-ffmpeg` 技術，首次執行時會自動在背景下載並配置適合您作業系統的影音轉換程式，省去繁瑣的環境變數設定。
- **防重複下載**：內建 `downloaded.txt` 紀錄檔，再次下載相同影片或清單時會自動跳過已下載的檔案，節省流量。

---

## 💻 批次檔/命令列版使用說明

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

- **互動模式（最推薦）**：雙擊 `yt2mp3.bat`，或是直接在終端機中執行：
  ```bash
  .\yt2mp3.bat
  ```
- **單一影片下載**：
  ```bash
  .\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼"
  ```
- **自訂儲存檔名**：
  ```bash
  .\yt2mp3.bat -u "https://www.youtube.com/watch?v=影片代碼" -o "自訂歌名.mp3"
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

## 🌐 網頁版應用程式 (Streamlit Web App)

網頁版提供了一個直覺美觀的瀏覽器操作介面，支援單檔下載與整組清單打包成 ZIP 壓縮檔下載。

### 1. 本機執行網頁版
1. 確保已安裝 `streamlit` 套件（已包含在 `requirements.txt` 中）：
   ```bash
   .\venv\Scripts\python -m pip install -r requirements.txt
   ```
2. 啟動網頁服務：
   ```bash
   .\venv\Scripts\streamlit run app.py
   ```
3. 程式會自動開啟瀏覽器網頁（預設網址為 `http://localhost:8501`）。

### 2. 免費部署至 Streamlit Community Cloud
您可以將此專案免費部署至 Streamlit 雲端平台，讓您或朋友在手機、平板或任何裝置上都可以透過瀏覽器直接下載音樂：

1. 前往 [Streamlit Community Cloud](https://share.streamlit.io) 並使用您的 **GitHub 帳號** 登入。
2. 點選 **"Create app"**（新建應用程式）。
3. 在部署設定中填入：
   - **Repository**: `shawnho1029/YT2MP3`
   - **Branch**: `master`
   - **Main file path**: `app.py`
4. 點選 **"Deploy!"**（部署）。
5. 稍等數分鐘，平台會自動讀取 `requirements.txt` 安裝所有套件。由於程式內建了 `static-ffmpeg`，它會自動在雲端 Linux 伺服器上配置好轉檔環境，您完全不需要做任何額外設定。
6. 部署完成後，您將獲得一個專屬的網頁連結（網址類似 `https://yt2mp3-xxxx.streamlit.app`），即可開始分享與使用！

---

## 📝 專案結構與版本控制

為了保持專案乾淨，已設定 `.gitignore` 過濾規則，請避免將以下檔案上傳至您的 GitHub 儲存庫：
- `venv/`（本機虛擬環境）
- `music/`（下載的音樂資料夾）
- `downloaded.txt`（下載歷史紀錄檔）
- 所有 `.mp3` 等實體音訊檔案
