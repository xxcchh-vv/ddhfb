# Stream Sentinel

24 小时自动检测直播/录播资源并下载到本地的工具项目。

当前第一版目标：

- 定时检测多个直播间或频道
- 自动判断是否有新视频/新直播
- 调用 yt-dlp / streamlink / ffmpeg 下载到本地
- 用 SQLite 记录下载历史，避免重复下载
- 支持 Docker 长期运行

## 计划支持平台

- YouTube
- Twitch
- Bilibili
- Douyu
- Huya
- 其他 yt-dlp 支持的网站

## 项目状态

初始化中。