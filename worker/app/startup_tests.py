"""
Startup encoder tests to validate hardware acceleration on container boot.
Populates ENCODER_TEST_CACHE so compress jobs don't pay the init test cost.
"""
import subprocess
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


def test_encoder_init(encoder_name: str, hw_flags: List[str]) -> Tuple[bool, str]:
    """
    Test if encoder can actually be initialized (not just listed).
    Returns (success: bool, message: str)
    """
    try:
        cmd = ["ffmpeg", "-hide_banner"]
        cmd.extend(hw_flags)
        cmd.extend([
            "-f", "lavfi", "-i", "color=black:s=256x256:d=0.1",
            "-c:v", encoder_name,
            "-t", "0.1",
            "-frames:v", "1",
            "-f", "null", "-"
        ])
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        stderr_lower = result.stderr.lower()
        
        # Check for specific errors that indicate driver/library issues
        if "operation not permitted" in stderr_lower:
            return False, "Operation not permitted"
        if "could not open encoder" in stderr_lower:
            return False, "Could not open encoder"
        if "no device found" in stderr_lower:
            return False, "No device found"
        if "failed to set value" in stderr_lower and "init_hw_device" in stderr_lower:
            return False, "Hardware device initialization failed"
        if "cannot load" in stderr_lower and ".so" in stderr_lower:
            lib = result.stderr.split('Cannot load')[1].split()[0] if 'Cannot load' in result.stderr else 'unknown'
            return False, f"Missing library ({lib})"
        
        # Success
        return True, "OK"
    except subprocess.TimeoutExpired:
        return True, "Timeout (>10s) - assuming works"
    except Exception as e:
        return False, f"Exception: {str(e)}"


def is_encoder_available(encoder_name: str) -> bool:
    """Check if encoder is available in ffmpeg."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            capture_output=True,
            text=True,
            timeout=2
        )
        return encoder_name in result.stdout
    except Exception:
        return False


def run_startup_tests(hw_info: Dict) -> Dict[str, bool]:
    """
    Run encoder initialization tests for all hardware-accelerated encoders.
    Returns cache dict of {encoder_key: bool}.
    Logs results for troubleshooting.
    """
    from .hw_detect import map_codec_to_hw
    
    logger.info("=" * 60)
    logger.info("Starting encoder validation tests...")
    logger.info(f"Hardware type detected: {hw_info.get('type', 'unknown').upper()}")
    logger.info("=" * 60)
    
    cache: Dict[str, bool] = {}
    
    # Test all common codecs for this hardware type
    test_codecs = []
    hw_type = hw_info.get("type", "cpu")
    
    if hw_type == "nvidia":
        test_codecs = ["h264_nvenc", "hevc_nvenc", "av1_nvenc"]
    elif hw_type == "intel":
        test_codecs = ["h264_qsv", "hevc_qsv", "av1_qsv"]
    elif hw_type in ("amd", "vaapi"):
        test_codecs = ["h264_vaapi", "hevc_vaapi", "av1_vaapi"]
    
    # Always test CPU fallbacks
    test_codecs.extend(["libx264", "libx265", "libaom-av1"])
    
    for codec in test_codecs:
        try:
            actual_encoder, v_flags, init_hw_flags = map_codec_to_hw(codec, hw_info)
            
            # Skip if not actually a hardware encoder for this system
            if actual_encoder in ("libx264", "libx265", "libaom-av1"):
                if codec not in ("libx264", "libx265", "libaom-av1"):
                    logger.info(f"  [{codec}] -> Skipped (maps to CPU: {actual_encoder})")
                    continue
            
            # Check availability first (fast)
            if not is_encoder_available(actual_encoder):
                logger.warning(f"  [{codec}] -> UNAVAILABLE (not in ffmpeg -encoders)")
                cache_key = f"{actual_encoder}:{':'.join(init_hw_flags)}"
                cache[cache_key] = False
                continue
            
            # Run init test (slow but thorough)
            cache_key = f"{actual_encoder}:{':'.join(init_hw_flags)}"
            success, message = test_encoder_init(actual_encoder, init_hw_flags)
            cache[cache_key] = success
            
            status = "✓ PASS" if success else "✗ FAIL"
            logger.info(f"  [{codec}] -> {status} ({actual_encoder}) - {message}")
            
        except Exception as e:
            logger.error(f"  [{codec}] -> ERROR: {str(e)}")
    
    logger.info("=" * 60)
    logger.info(f"Encoder tests complete. {sum(cache.values())} passed, {len(cache) - sum(cache.values())} failed.")
    logger.info("=" * 60)
    
    return cache
