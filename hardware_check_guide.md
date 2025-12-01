# 8mb.local 硬件兼容性检查指南

## 1. 基本系统要求

### 操作系统支持
- **Windows 11 + WSL2** (推荐) - 支持NVIDIA GPU
- **Linux** (Ubuntu 18.04+, Debian 10+, CentOS 8+) - 支持NVIDIA、Intel、AMD GPU
- **macOS** - 仅支持CPU模式，无GPU加速

### 系统资源要求
- **内存**: 最少4GB，推荐8GB以上
- **存储**: 至少10GB可用空间（用于临时文件和输出文件）
- **Docker**: 支持Docker Desktop或Docker Engine

## 2. GPU硬件检查

### 2.1 检查NVIDIA GPU

#### Windows系统 (Windows 11 + WSL2)
```powershell
# 在Windows PowerShell中运行
nvidia-smi
```

#### Linux系统
```bash
# 检查NVIDIA GPU
nvidia-smi

# 检查CUDA支持
nvcc --version

# 检查GPU设备文件
ls -la /dev/nvidia*
```

**支持的NVIDIA GPU：**
- **RTX 40系列/50系列** (RTX 4090, RTX 4080, RTX 4070等): 支持AV1、HEVC、H.264
- **RTX 30系列** (RTX 3090, RTX 3080, RTX 3070等): 支持HEVC、H.264，AV1需更新驱动
- **RTX 20系列** (RTX 2080, RTX 2070等): 支持HEVC、H.264
- **GTX 16系列** (GTX 1660, GTX 1650等): 支持H.264，部分支持HEVC
- **GTX 10系列** (GTX 1080, GTX 1070等): 支持H.264，部分支持HEVC

### 2.2 检查Intel GPU

#### Linux系统
```bash
# 检查Intel GPU设备
ls -la /dev/dri/

# 检查Intel媒体驱动
vainfo

# 检查QSV支持
ffmpeg -hide_banner -hwaccels
```

**支持的Intel GPU：**
- **Intel Arc GPU** (A770, A750, A580等): 支持AV1、HEVC、H.264
- **Intel Quick Sync** (第6代Core处理器及以上): 支持HEVC、H.264
- **注意**: WSL2和Docker Desktop可能无法访问Intel GPU

### 2.3 检查AMD GPU

#### Linux系统
```bash
# 检查AMD GPU
lspci | grep VGA

# 检查VAAPI支持
ffmpeg -hide_banner -hwaccels

# 检查Mesa驱动
glxinfo | grep -i mesa
```

**支持的AMD GPU：**
- **RDNA 3系列** (RX 7900系列): 支持AV1、HEVC、H.264
- **RDNA 2系列** (RX 6600及以上): 支持HEVC、H.264
- **RDNA 1系列** (RX 5700系列): 支持HEVC、H.264

## 3. 驱动程序检查

### 3.1 NVIDIA驱动程序
```bash
# 检查驱动版本 (要求550+)
nvidia-smi

# 检查NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu20.04 nvidia-smi
```

**驱动版本要求：**
- **RTX 50系列**: 550.54+ (最新推荐)
- **RTX 40/30系列**: 535.x+ 
- **RTX 20/16/10系列**: 470.x+

### 3.2 Intel媒体驱动 (Linux)
```bash
# 安装Intel媒体驱动
sudo apt install intel-media-va-driver libmfx1

# 检查驱动状态
vainfo --display drm
```

### 3.3 AMD Mesa驱动 (Linux)
```bash
# 安装Mesa驱动
sudo apt install mesa-va-drivers mesa-vdpau-drivers

# 检查VAAPI支持
vainfo
```

## 4. FFmpeg硬件加速检查

### 4.1 检查可用的硬件加速
```bash
# 检查FFmpeg支持的硬件加速
ffmpeg -hide_banner -hwaccels

# 检查可用的编码器
ffmpeg -hide_banner -encoders | grep -E "(nvenc|nvenc|qsv|vaapi|amf)"

# 检查解码器
ffmpeg -hide_banner -decoders | grep -E "(nvenc|nvenc|qsv|vaapi|amf)"
```

### 4.2 GPU编码器测试
```bash
# NVIDIA NVENC测试
ffmpeg -f lavfi -i nullsrc -c:v h264_nvenc -f null -

# Intel QSV测试  
ffmpeg -f lavfi -i nullsrc -c:v h264_qsv -f null -

# VAAPI测试
ffmpeg -f lavfi -i nullsrc -c:v h264_vaapi -f null -
```

## 5. Docker支持检查

### 5.1 Docker安装检查
```bash
# 检查Docker版本
docker --version

# 检查Docker运行状态
docker ps

# 检查Docker Compose版本
docker-compose --version
```

### 5.2 GPU支持检查 (NVIDIA)
```bash
# 检查NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu20.04 nvidia-smi

# 检查Docker GPU支持
docker run --rm --gpus all ubuntu nvidia-smi
```

### 5.3 GPU支持检查 (Intel/AMD Linux)
```bash
# 检查GPU设备访问
docker run --rm -it --device=/dev/dri:/dev/dri ubuntu ls -la /dev/dri
```

## 6. 快速诊断脚本

### 6.1 Windows WSL2检查脚本
```powershell
# 创建检查脚本：check_requirements.ps1
Write-Host "=== 8mb.local 硬件检查 ===" -ForegroundColor Green

Write-Host "`n1. 检查NVIDIA GPU..."
try {
    $gpu = nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
    Write-Host "✓ 发现NVIDIA GPU: $gpu" -ForegroundColor Green
} catch {
    Write-Host "✗ 未检测到NVIDIA GPU" -ForegroundColor Red
}

Write-Host "`n2. 检查驱动程序..."
try {
    $driver = nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits
    Write-Host "✓ NVIDIA驱动版本: $driver" -ForegroundColor Green
    if ([version]$driver -ge [version]"550") {
        Write-Host "✓ 驱动版本满足要求 (≥550)" -ForegroundColor Green
    } else {
        Write-Host "⚠ 建议升级驱动到550+" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ 无法获取驱动信息" -ForegroundColor Red
}

Write-Host "`n3. 检查Docker..."
try {
    $docker = docker --version
    Write-Host "✓ $docker" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker未安装或未运行" -ForegroundColor Red
}

Write-Host "`n4. 检查FFmpeg..."
try {
    $ffmpeg = ffmpeg -version | Select-String "ffmpeg version" | ForEach-Object { $_.Line }
    Write-Host "✓ $ffmpeg" -ForegroundColor Green
} catch {
    Write-Host "✗ FFmpeg未安装" -ForegroundColor Red
}

Write-Host "`n=== 检查完成 ===" -ForegroundColor Green
```

### 6.2 Linux检查脚本
```bash
#!/bin/bash
# 创建检查脚本：check_requirements.sh

echo "=== 8mb.local 硬件检查 ==="
echo

echo "1. 检查GPU设备..."
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
    DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits)
    echo "✓ NVIDIA驱动版本: $DRIVER"
    if [[ $(echo "$DRIVER" | cut -d. -f1) -ge 550 ]]; then
        echo "✓ 驱动版本满足要求 (≥550)"
    else
        echo "⚠ 建议升级驱动到550+"
    fi
else
    echo "✗ 未检测到NVIDIA GPU"
fi

echo
echo "2. 检查Intel/AMD GPU..."
if [[ -d /dev/dri ]]; then
    echo "✓ 发现GPU设备:"
    ls -la /dev/dri/
    if command -v vainfo &> /dev/null; then
        echo "✓ VAAPI支持检查:"
        vainfo 2>/dev/null || echo "⚠ vainfo测试失败"
    fi
else
    echo "✗ 未检测到GPU设备文件 (/dev/dri不存在)"
fi

echo
echo "3. 检查FFmpeg硬件加速..."
echo "可用的硬件加速:"
ffmpeg -hide_banner -hwaccels 2>/dev/null || echo "✗ FFmpeg未安装"

echo
echo "可用的编码器 (硬件相关):"
ffmpeg -hide_banner -encoders 2>/dev/null | grep -E "(nvenc|nvenc|qsv|vaapi|amf)" || echo "✗ 未发现硬件编码器"

echo
echo "4. 检查Docker..."
if command -v docker &> /dev/null; then
    echo "✓ Docker已安装:"
    docker --version
    if [[ -S /var/run/docker.sock ]]; then
        echo "✓ Docker守护进程运行中"
    else
        echo "⚠ Docker守护进程未运行"
    fi
else
    echo "✗ Docker未安装"
fi

echo
echo "=== 检查完成 ==="
```

## 7. 运行检查

### 7.1 保存并运行脚本

#### Windows (PowerShell)
```powershell
# 1. 创建脚本文件
New-Item -ItemType File -Path "check_requirements.ps1"

# 2. 复制上面的PowerShell脚本内容到文件

# 3. 运行脚本 (可能需要管理员权限)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
./check_requirements.ps1
```

#### Linux/macOS (Bash)
```bash
# 1. 创建脚本文件
cat > check_requirements.sh << 'EOF'
# 复制上面的Bash脚本内容
EOF

# 2. 添加执行权限
chmod +x check_requirements.sh

# 3. 运行脚本
./check_requirements.sh
```

## 8. 常见问题解决

### 8.1 驱动程序问题
- **RTX 50系列驱动过旧**: 升级到550.54+
- **Debian 12驱动**: 使用NVIDIA官方仓库而非backports
- **Ubuntu驱动**: 添加graphics-drivers PPA

### 8.2 Docker GPU访问问题
- **NVIDIA Container Toolkit**: 安装NVIDIA容器工具包
- **WSL2 GPU支持**: 在Docker Desktop中启用GPU支持
- **权限问题**: 将用户添加到docker组

### 8.3 FFmpeg编译问题
- **硬件编码器缺失**: 使用预编译的FFmpeg或重新编译包含硬件支持
- **库依赖**: 安装相应的硬件加速库

## 9. 兼容性总结

### ✅ 完全支持 (推荐配置)
- **Windows 11 + WSL2 + NVIDIA RTX 40/50系列**
- **Ubuntu 20.04+ + NVIDIA RTX 30/40系列**
- **Ubuntu 20.04+ + Intel Arc GPU**
- **Ubuntu 20.04+ + AMD RDNA 3 GPU**

### ⚠️ 部分支持
- **macOS**: 仅CPU模式，无GPU加速
- **旧款GPU**: 可能只支持H.264编码

### ❌ 不推荐
- **GTX 10系列以下**: 硬件加速有限
- **纯CPU系统**: 压缩速度较慢

通过以上检查，您就能确定自己的硬件是否支持8mb.local项目了！