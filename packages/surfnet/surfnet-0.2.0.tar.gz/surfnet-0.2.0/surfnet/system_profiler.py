"""
System profiler for automatically detecting hardware capabilities
and optimizing parallel processing settings.
"""

import os
import platform
import multiprocessing
import logging
from typing import Dict, Optional, Tuple

# Initialize logging
logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    import psutil
    HAVE_PSUTIL = True
except ImportError:
    HAVE_PSUTIL = False
    logger.warning("psutil not found - limited system info available")

try:
    import GPUtil
    HAVE_GPUTIL = True
except ImportError:
    HAVE_GPUTIL = False
    logger.warning("GPUtil not found - GPU detection disabled")

try:
    import ray
    HAVE_RAY = True
except ImportError:
    HAVE_RAY = False
    logger.warning("Ray not found - advanced parallel processing disabled")


class SystemProfiler:
    """Detects system capabilities and recommends optimal settings for parallel processing."""
    
    def __init__(self, min_workers: int = 2, max_workers: int = 32):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.system_info = self._get_system_info()
        self.optimal_settings = self._calculate_optimal_settings()
        
    def _get_system_info(self) -> Dict:
        """Get comprehensive system information."""
        info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'cpu_count': multiprocessing.cpu_count(),
            'logical_cpus': os.cpu_count() or multiprocessing.cpu_count(),
            'memory_gb': None,
            'gpus': None,
            'gpu_memory_gb': None,
            'has_cuda': False,
            'has_tensor_cores': False,
            'io_capability': 'unknown'
        }
        
        # Get detailed memory info if psutil is available
        if HAVE_PSUTIL:
            mem = psutil.virtual_memory()
            info['memory_gb'] = round(mem.total / (1024 ** 3), 2)
            
            # Estimate IO capability based on disk
            try:
                disk_io = psutil.disk_io_counters(perdisk=False)
                if disk_io:
                    info['io_capability'] = 'ssd' if disk_io.read_bytes > 100000000 else 'hdd'
            except Exception:
                pass
            
        # Get GPU info if available
        if HAVE_GPUTIL:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    info['gpus'] = len(gpus)
                    info['gpu_memory_gb'] = sum(gpu.memoryTotal for gpu in gpus) / 1024  # Convert MB to GB
                    info['has_cuda'] = any('CUDA' in gpu.name for gpu in gpus)
                    info['has_tensor_cores'] = any(('RTX' in gpu.name or 'TITAN RTX' in gpu.name or 'A100' in gpu.name or 'V100' in gpu.name) for gpu in gpus)
            except Exception as e:
                logger.warning(f"Error detecting GPUs: {str(e)}")
        
        logger.info(f"System info: {info}")
        return info
    
    def _calculate_optimal_settings(self) -> Dict:
        """Calculate optimal settings based on system capabilities."""
        si = self.system_info
        
        # Default conservative settings
        settings = {
            'recommended_workers': min(max(si['logical_cpus'] - 1, self.min_workers), self.max_workers),
            'max_parallel_requests': 10,
            'max_memory_gb': 1.0,
            'use_gpu': False,
            'use_ray': False,
            'batch_size': 1,
            'estimated_throughput': 0
        }
        
        # Adjust for available memory
        if si['memory_gb']:
            # Reserve 2GB for the system or 25% of memory, whichever is larger
            reserved_memory = max(2, si['memory_gb'] * 0.25)
            available_memory = si['memory_gb'] - reserved_memory
            settings['max_memory_gb'] = max(1.0, available_memory)
            
            # More memory = larger batches possible
            if available_memory > 8:
                settings['batch_size'] = 16
            elif available_memory > 4:
                settings['batch_size'] = 8
            elif available_memory > 2:
                settings['batch_size'] = 4
            else:
                settings['batch_size'] = 2
        
        # Adjust for GPU if available
        if si['gpus'] and si['gpu_memory_gb']:
            settings['use_gpu'] = True
            # Increase parallel requests if GPU is available
            settings['max_parallel_requests'] = 20 if si['has_tensor_cores'] else 15
            
        # Adjust for Ray if available
        if HAVE_RAY:
            settings['use_ray'] = True
            # Can handle more workers with Ray's efficient scheduling
            settings['recommended_workers'] = min(si['logical_cpus'] * 2, self.max_workers)
        
        # Calculate estimated throughput (rows per hour)
        # Base throughput: 100 rows per minute per worker
        base_throughput = 100 * 60 * settings['recommended_workers']
        
        # Multipliers
        memory_multiplier = min(2.0, max(1.0, settings['max_memory_gb'] / 4))
        gpu_multiplier = 2.5 if settings['use_gpu'] and si['has_tensor_cores'] else 1.5 if settings['use_gpu'] else 1.0
        ray_multiplier = 1.2 if settings['use_ray'] else 1.0
        batch_multiplier = 0.8 + (settings['batch_size'] * 0.05)  # Larger batches are more efficient
        
        # Final estimate
        settings['estimated_throughput'] = int(base_throughput * memory_multiplier * gpu_multiplier * ray_multiplier * batch_multiplier)
        
        logger.info(f"Optimal settings: {settings}")
        return settings
    
    def get_recommended_workers(self) -> int:
        """Get the recommended number of parallel workers."""
        return self.optimal_settings['recommended_workers']
    
    def get_max_parallel_requests(self) -> int:
        """Get the recommended maximum number of parallel requests."""
        return self.optimal_settings['max_parallel_requests']
    
    def should_use_gpu(self) -> bool:
        """Determine if GPU acceleration should be used."""
        return self.optimal_settings['use_gpu']
    
    def should_use_ray(self) -> bool:
        """Determine if Ray should be used for distributed processing."""
        return self.optimal_settings['use_ray']
    
    def get_estimated_throughput(self) -> int:
        """Get the estimated throughput in rows per hour."""
        return self.optimal_settings['estimated_throughput']
    
    def print_system_report(self) -> None:
        """Print a human-readable system report with optimization recommendations."""
        si = self.system_info
        settings = self.optimal_settings
        
        report = [
            "=== Surfnet System Capability Report ===",
            f"Platform: {si['platform']} {si['platform_release']} ({si['architecture']})",
            f"Processor: {si['processor']}",
            f"CPU Cores: {si['cpu_count']} physical, {si['logical_cpus']} logical",
            f"Memory: {si['memory_gb'] or 'Unknown'} GB",
            f"GPU: {'Yes, ' + str(si['gpus']) + ' detected' if si['gpus'] else 'None detected'}"
        ]
        
        if si['gpus']:
            report.append(f"GPU Memory: {si['gpu_memory_gb']:.2f} GB")
            report.append(f"CUDA Support: {'Yes' if si['has_cuda'] else 'No'}")
            report.append(f"Tensor Cores: {'Yes' if si['has_tensor_cores'] else 'No'}")
        
        report.extend([
            "",
            "=== Recommended Settings ===",
            f"Parallel Workers: {settings['recommended_workers']}",
            f"Max Parallel Requests: {settings['max_parallel_requests']}",
            f"Memory Allocation: {settings['max_memory_gb']:.2f} GB",
            f"Use GPU Acceleration: {'Yes' if settings['use_gpu'] else 'No'}",
            f"Use Ray Distributed Computing: {'Yes' if settings['use_ray'] else 'No'}",
            f"Optimal Batch Size: {settings['batch_size']}",
            "",
            f"Estimated Throughput: {settings['estimated_throughput']:,} rows per hour"
        ])
        
        if settings['estimated_throughput'] >= 500000:
            report.append("✓ System meets high-throughput requirement (500K+ rows/hour)")
        else:
            report.append(f"⚠ System may not meet throughput target (Current: {settings['estimated_throughput']:,}/hr, Target: 500,000/hr)")
            
            # Provide suggestions for improvement
            suggestions = []
            if si['logical_cpus'] < 8:
                suggestions.append("- More CPU cores would improve processing speed")
            if not si['gpus']:
                suggestions.append("- Adding a GPU would significantly improve throughput")
            elif not si['has_tensor_cores']:
                suggestions.append("- A GPU with Tensor Cores would improve processing")
            if si['memory_gb'] and si['memory_gb'] < 8:
                suggestions.append("- Additional memory would allow larger batch sizes")
            
            if suggestions:
                report.append("\nSuggestions to improve performance:")
                report.extend(suggestions)
        
        print("\n".join(report))


def initialize_ray_if_available(num_workers: Optional[int] = None) -> bool:
    """Initialize Ray for distributed processing if available."""
    if not HAVE_RAY:
        return False
        
    try:
        if not ray.is_initialized():
            ray.init(num_cpus=num_workers, ignore_reinit_error=True)
        return True
    except Exception as e:
        logger.warning(f"Failed to initialize Ray: {str(e)}")
        return False


def get_optimal_settings() -> Tuple[int, bool]:
    """Get optimal worker count and GPU usage settings."""
    profiler = SystemProfiler()
    return profiler.get_recommended_workers(), profiler.should_use_gpu() 