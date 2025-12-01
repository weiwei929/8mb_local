# 8mb.local 轻量级部署方案

## 🎯 理解您的担忧

您的担心很合理！我来提供几个更轻量级的方案，让您在不占用太多C盘空间的情况下使用8mb.local。

## 📊 Docker Desktop占用分析

### 实际占用情况
- **Docker Desktop应用**: ~500MB
- **Docker镜像**: ~2-3GB (8mb.local镜像)
- **容器存储**: ~1-2GB (运行时)
- **总计**: 约4-6GB

### C盘空间管理技巧
如果您想使用Docker，我提供几个空间管理方法：

#### 方法1: 迁移Docker数据目录
```powershell
# 1. 停止Docker Desktop
# 2. 在PowerShell中运行：
wsl --shutdown
docker system prune -a

# 3. 迁移Docker数据到其他盘符
# 在Docker Desktop设置中 -> Resources -> Disk image location
# 改为 D:\ 或 E:\ 等盘符
```

#### 方法2: 限制Docker资源使用
- **内存限制**: 2-4GB (Docker Desktop设置中)
- **磁盘空间**: 设置合理的限制
- **CPU核心**: 限制1-2个核心

## 🚀 轻量级替代方案

### 方案1: 便携版8mb.local (推荐)

我会为您创建一个免安装的便携版本：

#### 文件结构
```
8mb_local_portable/
├── app/
│   ├── backend/          # 后端Python代码
│   ├── frontend/         # 前端Web界面
│   ├── ffmpeg/           # FFmpeg可执行文件
│   └── requirements.txt  # Python依赖
├── uploads/             # 上传目录
├── outputs/             # 输出目录
├── start.bat            # Windows启动脚本
└── stop.bat             # Windows停止脚本
```

#### 优势
- ✅ 零安装，解压即用
- ✅ 可以放到任何盘符
- ✅ 关闭后完全清理
- ✅ 不在系统中留下痕迹
- ✅ 约200MB总大小

#### 缺点
- ⚠️ 需要手动启动/停止
- ⚠️ 需要手动管理Python环境

### 方案2: Python原生部署

使用Python直接运行，无需Docker：

```bash
# 1. 安装Python 3.8+ (如果还没有)
# 2. 创建项目目录
mkdir 8mb-local-python
cd 8mb-local-python

# 3. 下载并解压8mb.local源码
# 从GitHub: https://github.com/JMS1717/8mb.local/releases

# 4. 安装Python依赖
pip install -r requirements.txt

# 5. 启动应用
python -m backend.app.main
```

#### 优势
- ✅ 完全控制
- ✅ 可以修改代码
- ✅ 轻量级 (约100MB)
- ✅ 性能更好 (无容器开销)

#### 缺点
- ⚠️ 需要Python环境
- ⚠️ 需要手动管理依赖

### 方案3: WSL2 独立部署

在WSL2中运行，完全隔离：

```bash
# 1. 在WSL2中运行
wsl

# 2. 安装在WSL2home目录 (不在C盘)
mkdir ~/8mb-local
cd ~/8mb-local

# 3. 部署Docker版本或Python版本
# 所有文件都在WSL2的虚拟文件系统
```

#### 优势
- ✅ 完全隔离C盘
- ✅ 可以完整使用Docker
- ✅ WSL2内部性能很好
- ✅ 可以随时删除整个环境

### 方案4: 直接使用FFmpeg

如果您只需要简单的视频压缩：

```powershell
# 创建压缩脚本: compress_video.ps1

param(
    [string]$InputFile,
    [string]$OutputFile,
    [int]$TargetMB = 25
)

# 计算目标码率 (假设音频128kbps)
$duration = ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$InputFile"
$audioKbps = 128
$videoKbps = [math]::Round(($TargetMB * 8192 / $duration) - $audioKbps)

# 压缩命令
ffmpeg -i "$InputFile" -c:v libx264 -b:v ${videoKbps}k -c:a aac -b:a ${audioKbps}k "$OutputFile"

Write-Host "压缩完成: $OutputFile"
```

#### 优势
- ✅ 极致轻量级
- ✅ 快速执行
- ✅ 完全可控
- ✅ 无任何额外开销

#### 缺点
- ⚠️ 无Web界面
- ⚠️ 需要命令行操作
- ⚠️ 无进度显示

## 🎯 推荐方案

基于您的需求，我推荐：

### 第一选择: 便携版8mb.local
- 最接近原版体验
- 零安装，轻量级
- 可以放到D盘或E盘

### 第二选择: Python原生版
- 如果您不介意安装Python
- 更好的性能和控制

### 第三选择: 直接FFmpeg脚本
- 如果您只需要批量压缩
- 最轻量级选择

## 🔧 便携版8mb.local制作

如果您选择便携版，我可以为您：
1. **创建完整的便携版包**
2. **提供启动/停止脚本**
3. **优化C盘使用**
4. **提供升级方法**

## 📝 您的选择

请告诉我您更倾向于哪种方案：
1. **便携版8mb.local** (推荐，200MB)
2. **Python原生版** (150MB，需要Python)
3. **FFmpeg脚本版** (50MB，命令行)
4. **还是想试试Docker但解决空间问题**

我会根据您的选择提供详细的制作和部署指南！