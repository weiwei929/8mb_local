# 8mb.local 快速开始指南

## 🎉 太好了！您的硬件完全支持！

基于您的GTX 1660配置，您可以高效地使用8mb.local进行视频压缩。

## 🚀 快速部署（5分钟搞定）

### 1. 安装Docker Desktop
- **下载**: https://www.docker.com/products/docker-desktop/
- **安装**: 按默认设置安装Docker Desktop
- **启动**: 确保Docker Desktop在系统托盘运行

### 2. 运行8mb.local容器
在PowerShell中以管理员身份运行：

```powershell
# 创建工作目录
mkdir 8mb-local
cd 8mb-local

# 创建必要的目录
mkdir uploads
mkdir outputs

# 运行8mb.local
docker run -d --name 8mblocal `
  --gpus all `
  -e NVIDIA_DRIVER_CAPABILITIES=compute,video,utility `
  -p 8001:8001 `
  -v $PWD/uploads:/app/uploads `
  -v $PWD/outputs:/app/outputs `
  jms1717/8mblocal:latest
```

### 3. 等待启动完成
```powershell
# 检查容器状态
docker ps

# 查看启动日志（第一次可能需要等待1-2分钟）
docker logs 8mblocal
```

### 4. 访问Web界面
打开浏览器访问：**http://localhost:8001**

## 📱 使用指南

### 基本使用流程
1. **拖拽上传视频文件**
2. **设置目标大小** (如8MB、25MB、50MB)
3. **选择编码器** (推荐H.264 NVENC)
4. **点击压缩**
5. **等待完成并下载**

### 为您的GTX 1660优化的设置

#### 🎯 推荐配置
```
视频编码器: H.264 (NVIDIA)
质量预设: P6 (默认)
音频编码: AAC
音频码率: 128 kbps
容器: MP4
调整: 最佳质量 (HQ)
```

#### ⚡ 速度优化设置（如果需要更快速度）
```
视频编码器: H.264 (NVIDIA)  
质量预设: P4 或 P5
音频编码: AAC
音频码率: 96 kbps 或更低
```

#### 🎨 质量优先设置（如果需要更好质量）
```
视频编码器: H.264 (NVIDIA)
质量预设: P7
音频编码: Opus (如果用MKV容器)
音频码率: 160 kbps
```

### 常用场景设置

#### 📱 社交媒体 (Instagram, Twitter)
- **目标大小**: 8MB
- **编码器**: H.264
- **预设**: P5
- **分辨率**: 1080p或720p

#### 🎬 视频存档
- **目标大小**: 25MB
- **编码器**: H.264
- **预设**: P6
- **音频**: 128 kbps AAC

#### 💼 工作会议记录
- **目标大小**: 50MB
- **编码器**: H.264
- **预设**: P5
- **音频**: 128 kbps AAC

## 🔧 进阶设置

### 任务队列管理
- **并发任务**: 建议2-3个同时进行
- **访问队列页面**: http://localhost:8001/queue

### 历史记录
- **查看历史**: http://localhost:8001/history
- **重新下载**: 点击历史记录中的下载链接

### 系统设置
- **访问设置**: http://localhost:8001/settings
- **调整预设**: 可以创建自定义压缩预设
- **性能调优**: 调整并发任务数量

## 🚨 常见问题解决

### 容器启动问题
```powershell
# 查看详细错误信息
docker logs 8mblocal

# 重启容器
docker restart 8mblocal

# 停止并重新创建
docker stop 8mblocal
docker rm 8mblocal
```

### GPU识别问题
1. 确保Docker Desktop已启用GPU支持
2. 检查Windows WSL2 GPU访问是否启用
3. 重启Docker Desktop

### 压缩速度慢
1. 检查是否使用了H.264编码器
2. 降低质量预设（如使用P5而不是P7）
3. 减少并发任务数量

### 内存不足
1. 关闭其他大型应用程序
2. 减少并发任务数量
3. 选择较低分辨率

## 📊 性能预期

### 您的GTX 1660预期性能
- **1080p H.264压缩**: 3-6x实时速度
- **720p H.264压缩**: 5-10x实时速度
- **4K H.264压缩**: 1-3x实时速度
- **内存使用**: 每个任务约300-500MB

### 文件大小参考
- **1分钟1080p视频**: 8-25MB (取决于内容复杂度)
- **5分钟1080p视频**: 25-100MB
- **10分钟720p视频**: 25-50MB

## 🎯 成功小贴士

1. **选择合适的编码器**: 优先使用H.264 (NVIDIA)
2. **合理设置目标大小**: 不要太小以免损失过多质量
3. **监控压缩进度**: 通过实时日志查看编码状态
4. **批量处理**: 可以同时添加多个视频到队列
5. **定期清理**: 删除不需要的压缩历史记录

## 🔄 常用命令

```powershell
# 查看运行状态
docker ps | findstr 8mblocal

# 查看实时日志
docker logs -f 8mblocal

# 重启服务
docker restart 8mblocal

# 停止服务
docker stop 8mblocal

# 删除所有数据重新开始
docker stop 8mblocal
docker rm 8mblocal
docker volume prune
```

## 🎉 开始使用吧！

您现在可以开始使用8mb.local来高效压缩您的视频文件了。您的GTX 1660将提供很好的H.264硬件加速性能！

有任何问题随时询问哦！ 🚀