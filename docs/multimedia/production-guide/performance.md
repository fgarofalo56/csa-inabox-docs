# Performance Optimization for Multimedia Content

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **📎 [Production Guide](README.md)** | **⚡ Performance**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Type: Guide](https://img.shields.io/badge/Type-Guide-blue)
![Impact: High](https://img.shields.io/badge/Impact-High-red)

## Overview

Comprehensive guide for optimizing multimedia content performance in Cloud Scale Analytics documentation. This guide covers video compression, image optimization, streaming efficiency, and delivery optimization techniques to ensure fast, reliable content delivery across all platforms and devices.

## Performance Goals

### Target Metrics

```yaml
performance_targets:
  video:
    initial_load: "< 2 seconds"
    time_to_first_frame: "< 1 second"
    buffering_ratio: "< 1%"
    startup_failures: "< 0.1%"
    rebuffering_rate: "< 5%"

  interactive:
    page_load: "< 3 seconds"
    time_to_interactive: "< 5 seconds"
    first_contentful_paint: "< 1.5 seconds"
    largest_contentful_paint: "< 2.5 seconds"
    cumulative_layout_shift: "< 0.1"

  images:
    load_time: "< 1 second"
    format: "WebP with JPEG fallback"
    compression: "80-85% quality"
    lazy_loading: "enabled"
    responsive: "multiple sizes"

  animations:
    file_size: "< 500KB"
    frame_rate: "60 fps"
    load_time: "< 500ms"
    cpu_usage: "< 30%"
```

## Video Optimization

### Encoding Best Practices

**FFmpeg Optimal Settings:**

```bash
#!/bin/bash
# Optimized video encoding script for web delivery

INPUT_VIDEO="$1"
OUTPUT_DIR="$2"
FILENAME=$(basename "$INPUT_VIDEO" .mp4)

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to encode video with optimal settings
encode_video() {
  local resolution=$1
  local bitrate=$2
  local output_file="$OUTPUT_DIR/${FILENAME}_${resolution}.mp4"

  ffmpeg -i "$INPUT_VIDEO" \
    -c:v libx264 \
    -preset slow \
    -crf 23 \
    -profile:v high \
    -level 4.1 \
    -pix_fmt yuv420p \
    -movflags +faststart \
    -b:v $bitrate \
    -maxrate $(echo "$bitrate * 1.5" | bc) \
    -bufsize $(echo "$bitrate * 2" | bc) \
    -vf "scale=${resolution}:flags=lanczos" \
    -c:a aac \
    -b:a 128k \
    -ac 2 \
    -ar 48000 \
    -threads 0 \
    -y \
    "$output_file"

  echo "Encoded: $output_file"
}

# Encode multiple resolutions
echo "Starting multi-resolution encoding..."

# 1080p - High quality
encode_video "1920:-2" "5000k"

# 720p - Medium quality
encode_video "1280:-2" "3000k"

# 480p - Low quality
encode_video "854:-2" "1500k"

# 360p - Mobile quality
encode_video "640:-2" "800k"

echo "Encoding complete!"

# Generate WebM versions for better compression
generate_webm() {
  local resolution=$1
  local bitrate=$2
  local input_file="$OUTPUT_DIR/${FILENAME}_${resolution}.mp4"
  local output_file="$OUTPUT_DIR/${FILENAME}_${resolution}.webm"

  ffmpeg -i "$input_file" \
    -c:v libvpx-vp9 \
    -crf 30 \
    -b:v $bitrate \
    -row-mt 1 \
    -tile-columns 2 \
    -threads 8 \
    -c:a libopus \
    -b:a 128k \
    -y \
    "$output_file"

  echo "WebM created: $output_file"
}

echo "Generating WebM versions..."
generate_webm "1920:-2" "4000k"
generate_webm "1280:-2" "2500k"
generate_webm "854:-2" "1200k"

# Create thumbnail
ffmpeg -i "$INPUT_VIDEO" \
  -vf "thumbnail,scale=1280:720" \
  -frames:v 1 \
  "$OUTPUT_DIR/${FILENAME}_thumbnail.jpg"

echo "Thumbnail created"

# Generate statistics
echo ""
echo "=== Encoding Statistics ==="
for file in "$OUTPUT_DIR"/*; do
  if [[ -f "$file" ]]; then
    size=$(du -h "$file" | cut -f1)
    echo "$(basename "$file"): $size"
  fi
done
```

### Video Compression Settings

**Advanced Compression Configuration:**

```python
# Python script for optimal video compression
import subprocess
import json
from pathlib import Path

class VideoCompressor:
    def __init__(self, input_file, output_dir):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def analyze_video(self):
        """Analyze input video to determine optimal settings"""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            str(self.input_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        metadata = json.loads(result.stdout)

        video_stream = next(
            s for s in metadata['streams'] if s['codec_type'] == 'video'
        )

        return {
            'width': int(video_stream['width']),
            'height': int(video_stream['height']),
            'duration': float(metadata['format']['duration']),
            'bitrate': int(metadata['format']['bit_rate']),
            'fps': eval(video_stream['r_frame_rate'])
        }

    def calculate_optimal_bitrate(self, resolution, fps):
        """Calculate optimal bitrate based on resolution and fps"""
        # Base bitrates (kbps) for 30fps
        bitrate_map = {
            (3840, 2160): 15000,  # 4K
            (2560, 1440): 10000,  # 1440p
            (1920, 1080): 5000,   # 1080p
            (1280, 720): 3000,    # 720p
            (854, 480): 1500,     # 480p
            (640, 360): 800       # 360p
        }

        # Find closest resolution
        width, height = resolution
        closest = min(
            bitrate_map.keys(),
            key=lambda x: abs(x[0] - width) + abs(x[1] - height)
        )

        base_bitrate = bitrate_map[closest]

        # Adjust for frame rate
        if fps > 30:
            base_bitrate = int(base_bitrate * (fps / 30))

        return base_bitrate

    def encode_h264(self, output_resolution, bitrate):
        """Encode video with H.264 codec"""
        output_file = self.output_dir / f"{self.input_file.stem}_{output_resolution[1]}p.mp4"

        cmd = [
            'ffmpeg',
            '-i', str(self.input_file),

            # Video codec settings
            '-c:v', 'libx264',
            '-preset', 'slow',           # Better compression
            '-crf', '23',                # Constant quality
            '-profile:v', 'high',
            '-level', '4.1',
            '-pix_fmt', 'yuv420p',       # Maximum compatibility

            # Optimization flags
            '-movflags', '+faststart',   # Enable progressive download
            '-tune', 'film',             # Optimize for film content

            # Bitrate control
            '-b:v', f'{bitrate}k',
            '-maxrate', f'{int(bitrate * 1.5)}k',
            '-bufsize', f'{int(bitrate * 2)}k',

            # Scaling
            '-vf', f'scale={output_resolution[0]}:{output_resolution[1]}:flags=lanczos',

            # Audio settings
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ac', '2',
            '-ar', '48000',

            # Performance
            '-threads', '0',

            '-y',
            str(output_file)
        ]

        subprocess.run(cmd, check=True)
        return output_file

    def encode_av1(self, output_resolution, bitrate):
        """Encode video with AV1 codec for maximum compression"""
        output_file = self.output_dir / f"{self.input_file.stem}_{output_resolution[1]}p_av1.mp4"

        cmd = [
            'ffmpeg',
            '-i', str(self.input_file),

            # AV1 codec settings
            '-c:v', 'libaom-av1',
            '-cpu-used', '4',            # Balance speed/quality
            '-crf', '30',                # Quality level
            '-b:v', '0',                 # Use CRF mode

            # Optimization
            '-row-mt', '1',              # Multi-threading
            '-tiles', '2x2',

            # Scaling
            '-vf', f'scale={output_resolution[0]}:{output_resolution[1]}:flags=lanczos',

            # Audio
            '-c:a', 'libopus',
            '-b:a', '128k',

            '-y',
            str(output_file)
        ]

        subprocess.run(cmd, check=True)
        return output_file

    def create_hls_playlist(self, resolutions):
        """Create HLS adaptive streaming playlist"""
        # Generate variant playlists for each resolution
        variant_playlists = []

        for resolution, bitrate in resolutions.items():
            width, height = resolution
            variant_name = f"{height}p"

            # Create variant playlist
            variant_playlist = self.output_dir / f"stream_{variant_name}.m3u8"
            variant_playlists.append({
                'playlist': variant_playlist,
                'bandwidth': bitrate * 1000,
                'resolution': f"{width}x{height}"
            })

            # Segment video for streaming
            self._create_hls_segments(resolution, bitrate, variant_name)

        # Create master playlist
        self._create_master_playlist(variant_playlists)

    def _create_hls_segments(self, resolution, bitrate, variant_name):
        """Create HLS segments for streaming"""
        cmd = [
            'ffmpeg',
            '-i', str(self.input_file),

            # Video settings
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-b:v', f'{bitrate}k',
            '-maxrate', f'{int(bitrate * 1.5)}k',
            '-bufsize', f'{int(bitrate * 2)}k',
            '-vf', f'scale={resolution[0]}:{resolution[1]}',

            # Audio settings
            '-c:a', 'aac',
            '-b:a', '128k',

            # HLS settings
            '-f', 'hls',
            '-hls_time', '6',            # 6-second segments
            '-hls_list_size', '0',
            '-hls_segment_filename', str(self.output_dir / f'segment_{variant_name}_%03d.ts'),

            str(self.output_dir / f'stream_{variant_name}.m3u8')
        ]

        subprocess.run(cmd, check=True)

    def _create_master_playlist(self, variants):
        """Create HLS master playlist"""
        master_playlist = self.output_dir / 'master.m3u8'

        with open(master_playlist, 'w') as f:
            f.write('#EXTM3U\n')
            f.write('#EXT-X-VERSION:3\n\n')

            for variant in variants:
                f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={variant['bandwidth']},"
                       f"RESOLUTION={variant['resolution']}\n")
                f.write(f"{variant['playlist'].name}\n")

        return master_playlist

    def optimize(self):
        """Run complete optimization pipeline"""
        # Analyze input
        info = self.analyze_video()
        print(f"Input: {info['width']}x{info['height']} @ {info['fps']}fps")

        # Define target resolutions
        resolutions = {
            (1920, 1080): self.calculate_optimal_bitrate((1920, 1080), info['fps']),
            (1280, 720): self.calculate_optimal_bitrate((1280, 720), info['fps']),
            (854, 480): self.calculate_optimal_bitrate((854, 480), info['fps'])
        }

        # Encode each resolution
        results = {}
        for resolution, bitrate in resolutions.items():
            print(f"Encoding {resolution[1]}p at {bitrate}kbps...")

            # H.264 encoding
            h264_file = self.encode_h264(resolution, bitrate)
            results[f"{resolution[1]}p_h264"] = h264_file

        # Create HLS playlist for adaptive streaming
        print("Creating HLS adaptive streaming...")
        self.create_hls_playlist(resolutions)

        # Generate report
        return self._generate_report(results)

    def _generate_report(self, results):
        """Generate optimization report"""
        report = {
            'input_file': str(self.input_file),
            'input_size': self.input_file.stat().st_size,
            'outputs': {}
        }

        total_reduction = 0

        for name, output_file in results.items():
            output_size = output_file.stat().st_size
            reduction = ((report['input_size'] - output_size) / report['input_size']) * 100

            report['outputs'][name] = {
                'file': str(output_file),
                'size': output_size,
                'size_mb': round(output_size / (1024 * 1024), 2),
                'reduction': round(reduction, 2)
            }

            total_reduction += reduction

        report['avg_reduction'] = round(total_reduction / len(results), 2)

        return report
```

## Image Optimization

### Automated Image Processing

**Image Optimization Pipeline:**

```python
# Image optimization for web delivery
from PIL import Image
import pillow_avif
from pathlib import Path
import subprocess

class ImageOptimizer:
    def __init__(self, quality=85):
        self.quality = quality
        self.formats = ['webp', 'avif', 'jpeg']

    def optimize_image(self, input_path, output_dir):
        """Optimize single image to multiple formats"""
        input_path = Path(input_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        img = Image.open(input_path)

        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background

        results = {}

        # Generate responsive sizes
        sizes = {
            'thumbnail': 320,
            'small': 640,
            'medium': 1280,
            'large': 1920,
            'original': max(img.size)
        }

        for size_name, width in sizes.items():
            if width >= max(img.size):
                resized = img
            else:
                # Calculate proportional height
                aspect_ratio = img.size[1] / img.size[0]
                height = int(width * aspect_ratio)
                resized = img.resize((width, height), Image.Resampling.LANCZOS)

            # Save in multiple formats
            for fmt in self.formats:
                output_file = output_dir / f"{input_path.stem}_{size_name}.{fmt}"

                if fmt == 'webp':
                    resized.save(
                        output_file,
                        'WebP',
                        quality=self.quality,
                        method=6  # Highest quality encoding
                    )
                elif fmt == 'avif':
                    resized.save(
                        output_file,
                        'AVIF',
                        quality=self.quality
                    )
                elif fmt == 'jpeg':
                    resized.save(
                        output_file,
                        'JPEG',
                        quality=self.quality,
                        optimize=True,
                        progressive=True
                    )

                results[f"{size_name}_{fmt}"] = {
                    'file': str(output_file),
                    'size': output_file.stat().st_size,
                    'dimensions': resized.size
                }

        return results

    def create_responsive_html(self, image_name, alt_text):
        """Generate responsive HTML picture element"""
        html = f'''<picture>
  <!-- AVIF format (best compression, newest) -->
  <source
    srcset="
      /images/{image_name}_thumbnail.avif 320w,
      /images/{image_name}_small.avif 640w,
      /images/{image_name}_medium.avif 1280w,
      /images/{image_name}_large.avif 1920w
    "
    sizes="
      (max-width: 640px) 100vw,
      (max-width: 1280px) 80vw,
      1280px
    "
    type="image/avif">

  <!-- WebP format (good compression, wide support) -->
  <source
    srcset="
      /images/{image_name}_thumbnail.webp 320w,
      /images/{image_name}_small.webp 640w,
      /images/{image_name}_medium.webp 1280w,
      /images/{image_name}_large.webp 1920w
    "
    sizes="
      (max-width: 640px) 100vw,
      (max-width: 1280px) 80vw,
      1280px
    "
    type="image/webp">

  <!-- JPEG fallback (universal support) -->
  <img
    src="/images/{image_name}_medium.jpeg"
    srcset="
      /images/{image_name}_thumbnail.jpeg 320w,
      /images/{image_name}_small.jpeg 640w,
      /images/{image_name}_medium.jpeg 1280w,
      /images/{image_name}_large.jpeg 1920w
    "
    sizes="
      (max-width: 640px) 100vw,
      (max-width: 1280px) 80vw,
      1280px
    "
    alt="{alt_text}"
    loading="lazy"
    decoding="async">
</picture>'''

        return html

    def compress_png(self, input_file, output_file):
        """Lossless PNG compression using pngquant and optipng"""
        # First pass: color reduction with pngquant
        subprocess.run([
            'pngquant',
            '--quality=80-95',
            '--speed=1',
            '--force',
            '--output', str(output_file),
            str(input_file)
        ], check=True)

        # Second pass: optimization with optipng
        subprocess.run([
            'optipng',
            '-o7',  # Maximum optimization
            '-strip', 'all',
            str(output_file)
        ], check=True)

        return output_file
```

### Image Lazy Loading

**Intersection Observer Implementation:**

```javascript
// Efficient lazy loading for images and videos
class LazyLoader {
  constructor(options = {}) {
    this.options = {
      rootMargin: options.rootMargin || '50px',
      threshold: options.threshold || 0.01,
      loadingClass: options.loadingClass || 'lazy-loading',
      loadedClass: options.loadedClass || 'lazy-loaded',
      errorClass: options.errorClass || 'lazy-error'
    };

    this.observer = null;
    this.init();
  }

  init() {
    // Check for browser support
    if (!('IntersectionObserver' in window)) {
      this.fallbackLoad();
      return;
    }

    // Create observer
    this.observer = new IntersectionObserver(
      this.handleIntersection.bind(this),
      {
        rootMargin: this.options.rootMargin,
        threshold: this.options.threshold
      }
    );

    // Observe all lazy elements
    this.observe();
  }

  observe() {
    // Images
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => this.observer.observe(img));

    // Picture sources
    const sources = document.querySelectorAll('source[data-srcset]');
    sources.forEach(source => this.observer.observe(source));

    // Videos
    const videos = document.querySelectorAll('video[data-src]');
    videos.forEach(video => this.observer.observe(video));

    // Background images
    const backgrounds = document.querySelectorAll('[data-bg]');
    backgrounds.forEach(el => this.observer.observe(el));
  }

  handleIntersection(entries, observer) {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;

      const element = entry.target;
      element.classList.add(this.options.loadingClass);

      this.loadElement(element)
        .then(() => {
          element.classList.remove(this.options.loadingClass);
          element.classList.add(this.options.loadedClass);
          observer.unobserve(element);
        })
        .catch(err => {
          element.classList.remove(this.options.loadingClass);
          element.classList.add(this.options.errorClass);
          console.error('Lazy loading failed:', err);
        });
    });
  }

  loadElement(element) {
    return new Promise((resolve, reject) => {
      if (element.tagName === 'IMG') {
        this.loadImage(element).then(resolve).catch(reject);
      } else if (element.tagName === 'SOURCE') {
        this.loadSource(element).then(resolve).catch(reject);
      } else if (element.tagName === 'VIDEO') {
        this.loadVideo(element).then(resolve).catch(reject);
      } else if (element.dataset.bg) {
        this.loadBackground(element).then(resolve).catch(reject);
      } else {
        resolve();
      }
    });
  }

  loadImage(img) {
    return new Promise((resolve, reject) => {
      const src = img.dataset.src;
      const srcset = img.dataset.srcset;

      const tempImg = new Image();

      tempImg.onload = () => {
        if (srcset) img.srcset = srcset;
        img.src = src;
        delete img.dataset.src;
        delete img.dataset.srcset;
        resolve();
      };

      tempImg.onerror = reject;
      tempImg.src = src;
    });
  }

  loadSource(source) {
    const srcset = source.dataset.srcset;
    source.srcset = srcset;
    delete source.dataset.srcset;
    return Promise.resolve();
  }

  loadVideo(video) {
    const src = video.dataset.src;
    video.src = src;
    delete video.dataset.src;
    video.load();
    return Promise.resolve();
  }

  loadBackground(element) {
    return new Promise((resolve, reject) => {
      const bgUrl = element.dataset.bg;

      const img = new Image();
      img.onload = () => {
        element.style.backgroundImage = `url('${bgUrl}')`;
        delete element.dataset.bg;
        resolve();
      };
      img.onerror = reject;
      img.src = bgUrl;
    });
  }

  fallbackLoad() {
    // Load all images immediately if IntersectionObserver not supported
    const elements = document.querySelectorAll('[data-src], [data-srcset], [data-bg]');
    elements.forEach(element => this.loadElement(element));
  }
}

// Initialize lazy loader
document.addEventListener('DOMContentLoaded', () => {
  const lazyLoader = new LazyLoader({
    rootMargin: '100px',
    threshold: 0.01
  });
});
```

## Animation Performance

### Lottie Optimization

**Animation File Optimization:**

```javascript
// Lottie animation optimization utilities
class LottieOptimizer {
  constructor() {
    this.compressionThreshold = 500 * 1024; // 500KB
  }

  async optimizeAnimation(animationData) {
    const optimized = JSON.parse(JSON.stringify(animationData));

    // Remove unnecessary data
    this.removeUnusedLayers(optimized);
    this.simplifyPaths(optimized);
    this.mergeShapes(optimized);
    this.roundNumbers(optimized);
    this.removeEmptyKeyframes(optimized);

    // Compression check
    const originalSize = JSON.stringify(animationData).length;
    const optimizedSize = JSON.stringify(optimized).length;
    const reduction = ((originalSize - optimizedSize) / originalSize * 100).toFixed(2);

    console.log(`Lottie optimization: ${reduction}% reduction`);

    return optimized;
  }

  removeUnusedLayers(data) {
    if (!data.layers) return;

    data.layers = data.layers.filter(layer => {
      // Remove hidden layers
      if (layer.hd === true) return false;

      // Remove layers with zero opacity
      if (layer.ks?.o?.k === 0) return false;

      // Remove empty shape layers
      if (layer.ty === 4 && (!layer.shapes || layer.shapes.length === 0)) {
        return false;
      }

      return true;
    });
  }

  simplifyPaths(data) {
    // Simplify Bezier paths to reduce complexity
    const tolerance = 0.5;

    if (data.layers) {
      data.layers.forEach(layer => {
        if (layer.shapes) {
          layer.shapes.forEach(shape => {
            if (shape.it) {
              shape.it.forEach(item => {
                if (item.ty === 'sh' && item.ks?.k) {
                  // Simplify path vertices
                  this.simplifyVertices(item.ks.k, tolerance);
                }
              });
            }
          });
        }
      });
    }
  }

  simplifyVertices(vertices, tolerance) {
    // Douglas-Peucker algorithm for path simplification
    // Implementation details omitted for brevity
  }

  mergeShapes(data) {
    // Merge adjacent shapes with same properties
    if (!data.layers) return;

    data.layers.forEach(layer => {
      if (!layer.shapes) return;

      const merged = [];
      let currentGroup = null;

      layer.shapes.forEach(shape => {
        if (this.canMerge(currentGroup, shape)) {
          this.mergeIntoGroup(currentGroup, shape);
        } else {
          if (currentGroup) merged.push(currentGroup);
          currentGroup = shape;
        }
      });

      if (currentGroup) merged.push(currentGroup);
      layer.shapes = merged;
    });
  }

  roundNumbers(obj, precision = 2) {
    // Round all numeric values to reduce file size
    Object.keys(obj).forEach(key => {
      if (typeof obj[key] === 'number') {
        obj[key] = Math.round(obj[key] * Math.pow(10, precision)) / Math.pow(10, precision);
      } else if (typeof obj[key] === 'object' && obj[key] !== null) {
        this.roundNumbers(obj[key], precision);
      }
    });
  }

  removeEmptyKeyframes(data) {
    // Remove redundant keyframes
    if (!data.layers) return;

    data.layers.forEach(layer => {
      if (layer.ks) {
        Object.keys(layer.ks).forEach(prop => {
          if (layer.ks[prop].k && Array.isArray(layer.ks[prop].k)) {
            layer.ks[prop].k = this.compressKeyframes(layer.ks[prop].k);
          }
        });
      }
    });
  }

  compressKeyframes(keyframes) {
    if (keyframes.length <= 2) return keyframes;

    const compressed = [keyframes[0]];

    for (let i = 1; i < keyframes.length - 1; i++) {
      const prev = keyframes[i - 1];
      const current = keyframes[i];
      const next = keyframes[i + 1];

      // Keep keyframe if it represents significant change
      if (!this.isLinearInterpolation(prev, current, next)) {
        compressed.push(current);
      }
    }

    compressed.push(keyframes[keyframes.length - 1]);
    return compressed;
  }

  isLinearInterpolation(prev, current, next) {
    // Check if current keyframe is redundant (linear interpolation)
    const threshold = 0.01;

    const t = (current.t - prev.t) / (next.t - prev.t);
    const interpolated = prev.s.map((val, idx) =>
      val + (next.s[idx] - val) * t
    );

    return current.s.every((val, idx) =>
      Math.abs(val - interpolated[idx]) < threshold
    );
  }
}

// Lottie player with performance optimization
class OptimizedLottiePlayer {
  constructor(container, animationData, options = {}) {
    this.container = container;
    this.animationData = animationData;
    this.options = {
      renderer: options.renderer || 'svg',
      loop: options.loop !== false,
      autoplay: options.autoplay !== false,
      rendererSettings: {
        preserveAspectRatio: 'xMidYMid meet',
        progressiveLoad: true,
        hideOnTransparent: true,
        ...options.rendererSettings
      }
    };

    this.init();
  }

  async init() {
    // Optimize animation data
    const optimizer = new LottieOptimizer();
    this.optimizedData = await optimizer.optimizeAnimation(this.animationData);

    // Load Lottie player
    this.player = lottie.loadAnimation({
      container: this.container,
      animationData: this.optimizedData,
      ...this.options
    });

    // Performance monitoring
    this.setupPerformanceMonitoring();
  }

  setupPerformanceMonitoring() {
    let frameCount = 0;
    let lastTime = performance.now();

    this.player.addEventListener('enterFrame', () => {
      frameCount++;

      const currentTime = performance.now();
      if (currentTime - lastTime >= 1000) {
        const fps = frameCount;
        console.log(`Lottie FPS: ${fps}`);

        if (fps < 30) {
          console.warn('Low FPS detected, consider optimizing animation');
        }

        frameCount = 0;
        lastTime = currentTime;
      }
    });
  }

  play() {
    this.player.play();
  }

  pause() {
    this.player.pause();
  }

  destroy() {
    this.player.destroy();
  }
}
```

## CDN Performance

### Cache Optimization

**Advanced Caching Strategy:**

```typescript
// CDN cache control configuration
interface CacheConfig {
  contentType: string;
  maxAge: number;
  sMaxAge: number;
  staleWhileRevalidate: number;
  staleIfError: number;
  immutable: boolean;
}

class CDNCacheManager {
  private cacheConfigs: Map<string, CacheConfig>;

  constructor() {
    this.cacheConfigs = new Map([
      // Videos - Long cache, immutable
      ['video/mp4', {
        contentType: 'video/mp4',
        maxAge: 2592000,           // 30 days
        sMaxAge: 31536000,          // 1 year on CDN
        staleWhileRevalidate: 86400, // 1 day
        staleIfError: 604800,        // 7 days
        immutable: true
      }],

      // Interactive content - Medium cache
      ['text/html', {
        contentType: 'text/html',
        maxAge: 3600,               // 1 hour
        sMaxAge: 86400,             // 1 day on CDN
        staleWhileRevalidate: 3600,
        staleIfError: 86400,
        immutable: false
      }],

      // Images - Long cache
      ['image/webp', {
        contentType: 'image/webp',
        maxAge: 2592000,
        sMaxAge: 31536000,
        staleWhileRevalidate: 86400,
        staleIfError: 604800,
        immutable: true
      }],

      // Animations - Long cache
      ['application/json', {
        contentType: 'application/json',
        maxAge: 2592000,
        sMaxAge: 31536000,
        staleWhileRevalidate: 86400,
        staleIfError: 604800,
        immutable: true
      }]
    ]);
  }

  getCacheHeaders(contentType: string): Record<string, string> {
    const config = this.cacheConfigs.get(contentType) || this.getDefaultConfig();

    const directives = [
      `max-age=${config.maxAge}`,
      `s-maxage=${config.sMaxAge}`,
      `stale-while-revalidate=${config.staleWhileRevalidate}`,
      `stale-if-error=${config.staleIfError}`
    ];

    if (config.immutable) {
      directives.push('immutable');
    }

    return {
      'Cache-Control': directives.join(', '),
      'CDN-Cache-Control': `max-age=${config.sMaxAge}`,
      'Surrogate-Control': `max-age=${config.sMaxAge}`,
      'Vary': 'Accept-Encoding'
    };
  }

  private getDefaultConfig(): CacheConfig {
    return {
      contentType: 'application/octet-stream',
      maxAge: 3600,
      sMaxAge: 86400,
      staleWhileRevalidate: 3600,
      staleIfError: 86400,
      immutable: false
    };
  }
}
```

## Performance Monitoring

### Real User Monitoring (RUM)

**Performance Tracking Implementation:**

```javascript
// Comprehensive performance monitoring for multimedia content
class MultimediaPerformanceMonitor {
  constructor() {
    this.metrics = {
      videos: [],
      images: [],
      animations: [],
      interactive: []
    };

    this.init();
  }

  init() {
    // Monitor page load performance
    this.trackPageLoad();

    // Monitor resource loading
    this.trackResources();

    // Monitor video performance
    this.trackVideoPerformance();

    // Monitor user interactions
    this.trackInteractions();

    // Send metrics periodically
    setInterval(() => this.sendMetrics(), 30000); // Every 30 seconds
  }

  trackPageLoad() {
    window.addEventListener('load', () => {
      const perfData = performance.getEntriesByType('navigation')[0];

      const metrics = {
        type: 'page_load',
        timestamp: Date.now(),
        dns: perfData.domainLookupEnd - perfData.domainLookupStart,
        tcp: perfData.connectEnd - perfData.connectStart,
        ttfb: perfData.responseStart - perfData.requestStart,
        download: perfData.responseEnd - perfData.responseStart,
        domInteractive: perfData.domInteractive - perfData.fetchStart,
        domComplete: perfData.domComplete - perfData.fetchStart,
        loadComplete: perfData.loadEventEnd - perfData.fetchStart
      };

      this.sendToAnalytics('page_performance', metrics);
    });

    // Core Web Vitals
    this.trackWebVitals();
  }

  trackWebVitals() {
    // Largest Contentful Paint (LCP)
    new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      const lastEntry = entries[entries.length - 1];

      this.sendToAnalytics('web_vitals_lcp', {
        value: lastEntry.renderTime || lastEntry.loadTime,
        element: lastEntry.element?.tagName
      });
    }).observe({ type: 'largest-contentful-paint', buffered: true });

    // First Input Delay (FID)
    new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      entries.forEach(entry => {
        this.sendToAnalytics('web_vitals_fid', {
          value: entry.processingStart - entry.startTime,
          eventType: entry.name
        });
      });
    }).observe({ type: 'first-input', buffered: true });

    // Cumulative Layout Shift (CLS)
    let clsValue = 0;
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      }

      this.sendToAnalytics('web_vitals_cls', {
        value: clsValue
      });
    }).observe({ type: 'layout-shift', buffered: true });
  }

  trackResources() {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.initiatorType === 'img' || entry.initiatorType === 'video') {
          this.metrics.images.push({
            url: entry.name,
            duration: entry.duration,
            size: entry.transferSize,
            cached: entry.transferSize === 0
          });
        }
      }
    });

    observer.observe({ entryTypes: ['resource'] });
  }

  trackVideoPerformance() {
    document.querySelectorAll('video').forEach(video => {
      const metrics = {
        url: video.currentSrc,
        buffering: [],
        quality: [],
        startTime: null,
        errors: []
      };

      video.addEventListener('loadstart', () => {
        metrics.startTime = performance.now();
      });

      video.addEventListener('canplay', () => {
        const loadTime = performance.now() - metrics.startTime;
        this.sendToAnalytics('video_load', {
          url: metrics.url,
          loadTime: loadTime
        });
      });

      video.addEventListener('waiting', () => {
        metrics.buffering.push(performance.now());
      });

      video.addEventListener('playing', () => {
        if (metrics.buffering.length > 0) {
          const bufferDuration = performance.now() - metrics.buffering[metrics.buffering.length - 1];
          this.sendToAnalytics('video_buffering', {
            url: metrics.url,
            duration: bufferDuration
          });
        }
      });

      video.addEventListener('error', (e) => {
        this.sendToAnalytics('video_error', {
          url: metrics.url,
          error: e.message
        });
      });

      this.metrics.videos.push(metrics);
    });
  }

  trackInteractions() {
    // Track clicks on interactive elements
    document.addEventListener('click', (e) => {
      const target = e.target.closest('[data-interactive]');
      if (target) {
        this.sendToAnalytics('interaction_click', {
          element: target.dataset.interactive,
          timestamp: Date.now()
        });
      }
    });
  }

  sendToAnalytics(eventName, data) {
    // Send to Azure Application Insights
    if (window.appInsights) {
      window.appInsights.trackEvent({
        name: eventName,
        properties: data
      });
    }

    // Also send to custom endpoint
    this.sendMetricsToServer(eventName, data);
  }

  async sendMetricsToServer(eventName, data) {
    try {
      await fetch('/api/analytics/multimedia', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          event: eventName,
          data: data,
          timestamp: Date.now(),
          userAgent: navigator.userAgent,
          url: window.location.href
        })
      });
    } catch (error) {
      console.error('Failed to send metrics:', error);
    }
  }

  sendMetrics() {
    // Aggregate and send metrics
    const summary = {
      videos: this.metrics.videos.length,
      images: this.metrics.images.length,
      avgImageLoad: this.calculateAverageImageLoad(),
      avgVideoLoad: this.calculateAverageVideoLoad()
    };

    this.sendToAnalytics('metrics_summary', summary);
  }

  calculateAverageImageLoad() {
    if (this.metrics.images.length === 0) return 0;

    const total = this.metrics.images.reduce((sum, img) => sum + img.duration, 0);
    return total / this.metrics.images.length;
  }

  calculateAverageVideoLoad() {
    // Implementation omitted for brevity
    return 0;
  }
}

// Initialize monitoring
new MultimediaPerformanceMonitor();
```

## Best Practices

### Performance Checklist

- [ ] **Video Optimization**
  - [ ] Multiple resolutions encoded (1080p, 720p, 480p, 360p)
  - [ ] H.264 codec with faststart flag enabled
  - [ ] Adaptive streaming (HLS/DASH) implemented
  - [ ] Thumbnail images generated
  - [ ] Captions embedded and separate files provided

- [ ] **Image Optimization**
  - [ ] Modern formats (WebP, AVIF) with JPEG fallback
  - [ ] Responsive images with srcset
  - [ ] Lazy loading implemented
  - [ ] Compression applied (80-85% quality)
  - [ ] Dimensions optimized for display size

- [ ] **Animation Optimization**
  - [ ] File size under 500KB
  - [ ] Lottie animations optimized
  - [ ] CPU usage monitored
  - [ ] Fallback static images provided
  - [ ] Reduced motion respected

- [ ] **CDN Configuration**
  - [ ] Long cache durations for immutable content
  - [ ] Compression enabled
  - [ ] Edge locations configured
  - [ ] Purge strategy defined
  - [ ] Analytics enabled

- [ ] **Monitoring**
  - [ ] Core Web Vitals tracked
  - [ ] Resource timing monitored
  - [ ] Error tracking configured
  - [ ] User engagement measured
  - [ ] Performance budgets set

## Additional Resources

- [Video Encoding Guide](video-production-workflow.md)
- [Image Optimization Tools](../tools/image-optimization.md)
- [CDN Configuration](distribution.md)
- [Analytics Setup](../../monitoring/monitoring-setup.md)
- [Azure CDN Best Practices](https://docs.microsoft.com/azure/cdn/cdn-best-practices)

---

*Last Updated: January 2025 | Version: 1.0.0*
