# 🖼️ Image Optimization Tool

> **🏠 [Home](../../../README.md)** | **📖 [Documentation](../../README.md)** | **🎬 [Multimedia](../README.md)** | **🛠️ [Tools](README.md)** | **🖼️ Image Optimization**

![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Type: Optimization](https://img.shields.io/badge/Type-Optimization-blue)
![Performance: High](https://img.shields.io/badge/Performance-High-green)

## 📋 Overview

Automated image compression, format conversion, and optimization tool for web delivery. Integrates with Azure Blob Storage and CDN for seamless cloud deployment. Reduces image file sizes by 50-80% while maintaining visual quality.

## 🚀 Quick Start

### Installation

```bash
# NPM
npm install -g @csa/image-optimizer

# Yarn
yarn global add @csa/image-optimizer

# Verify installation
csa-image-optimize --version
```

### Basic Usage

```bash
# Optimize single image
csa-image-optimize input.png --output optimized.png

# Optimize directory
csa-image-optimize ./images --output ./optimized

# Convert to WebP
csa-image-optimize ./images --format webp --quality 85

# Generate responsive images
csa-image-optimize ./images --responsive --sizes 320,640,1024,1920
```

## 🎯 Optimization Features

### Compression

Lossy and lossless compression options:

```bash
# Lossless compression (no quality loss)
csa-image-optimize input.png --lossless

# Lossy compression with quality control
csa-image-optimize input.jpg --quality 85

# Aggressive compression
csa-image-optimize input.jpg --quality 70 --aggressive

# Auto-optimize (choose best settings)
csa-image-optimize ./images --auto
```

**Compression Results:**

| Format | Original | Optimized | Savings | Quality Loss |
|--------|----------|-----------|---------|--------------|
| PNG | 2.5 MB | 450 KB | 82% | None (lossless) |
| JPEG (Q85) | 1.8 MB | 320 KB | 82% | Imperceptible |
| WebP (Q85) | 1.8 MB | 180 KB | 90% | Imperceptible |
| AVIF (Q80) | 1.8 MB | 140 KB | 92% | Slight |

### Format Conversion

Convert between image formats:

```bash
# Convert to WebP
csa-image-optimize input.png --format webp --quality 85

# Convert to AVIF
csa-image-optimize input.jpg --format avif --quality 80

# Multiple format output
csa-image-optimize input.png --formats webp,avif,jpg --keep-original

# Auto-detect best format
csa-image-optimize input.png --auto-format
```

**Format Comparison:**

| Format | File Size | Quality | Browser Support | Use Case |
|--------|-----------|---------|-----------------|----------|
| PNG | Large | Lossless | Universal | Graphics, logos, transparency |
| JPEG | Medium | Lossy | Universal | Photos, complex images |
| WebP | Small | Lossy/Lossless | Modern browsers | General web use |
| AVIF | Smallest | Lossy/Lossless | Cutting-edge | Next-gen optimization |
| SVG | Tiny | Vector | Universal | Icons, simple graphics |

### Responsive Images

Generate multiple sizes for responsive web design:

```bash
# Generate standard sizes
csa-image-optimize input.jpg --responsive

# Custom sizes
csa-image-optimize input.jpg --sizes 320,640,1024,1920,2560

# With srcset generation
csa-image-optimize input.jpg --responsive --srcset --output-html

# Maintain aspect ratio
csa-image-optimize input.jpg --width 1920 --maintain-aspect
```

**Generated Output:**

```
input.jpg (original)
input-320w.jpg
input-640w.jpg
input-1024w.jpg
input-1920w.jpg
input-srcset.html
```

**Example srcset HTML:**

```html
<img
  src="input-1024w.jpg"
  srcset="
    input-320w.jpg 320w,
    input-640w.jpg 640w,
    input-1024w.jpg 1024w,
    input-1920w.jpg 1920w
  "
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  alt="Descriptive alt text"
  loading="lazy"
/>
```

### Batch Processing

Process multiple images efficiently:

```bash
# Process directory
csa-image-optimize ./images --output ./optimized --recursive

# Filter by pattern
csa-image-optimize ./images --pattern "*.{jpg,png}" --output ./optimized

# Parallel processing
csa-image-optimize ./images --parallel --workers 8

# Progress tracking
csa-image-optimize ./images --output ./optimized --progress --verbose
```

**Example Output:**

```text
Processing images...
[████████████████████] 100% | 45/45 images

Results:
  ✅ Successfully optimized: 43 images
  ⚠️  Warnings: 2 images
  ❌ Failed: 0 images

  Original total size: 125.6 MB
  Optimized total size: 28.4 MB
  Total savings: 97.2 MB (77.4%)

  Average processing time: 2.3s per image
  Total processing time: 1m 43s

Details saved to: optimization-report.json
```

## 🔧 Advanced Options

### Quality Presets

Pre-configured quality settings:

```bash
# Maximum quality (minimal compression)
csa-image-optimize input.jpg --preset max-quality

# Balanced (good quality, reasonable file size)
csa-image-optimize input.jpg --preset balanced

# High compression (smaller files, slight quality loss)
csa-image-optimize input.jpg --preset high-compression

# Web optimized (best for web delivery)
csa-image-optimize input.jpg --preset web
```

**Preset Details:**

```yaml
presets:
  max-quality:
    jpeg_quality: 95
    webp_quality: 95
    png_compression: 6
    strip_metadata: false

  balanced:
    jpeg_quality: 85
    webp_quality: 85
    png_compression: 7
    strip_metadata: false

  high-compression:
    jpeg_quality: 75
    webp_quality: 75
    png_compression: 9
    strip_metadata: true

  web:
    jpeg_quality: 85
    webp_quality: 85
    png_compression: 8
    strip_metadata: true
    progressive: true
    optimize: true
```

### Metadata Handling

Control image metadata:

```bash
# Strip all metadata
csa-image-optimize input.jpg --strip-metadata

# Keep copyright info
csa-image-optimize input.jpg --keep-metadata copyright,creator

# Add custom metadata
csa-image-optimize input.jpg --add-metadata "Author=CSA Team" "License=MIT"

# Preserve EXIF orientation
csa-image-optimize input.jpg --preserve-orientation
```

### Color Management

Optimize color profiles and color space:

```bash
# Convert to sRGB
csa-image-optimize input.jpg --colorspace srgb

# Optimize color profile
csa-image-optimize input.jpg --optimize-colors

# Reduce color palette (PNG)
csa-image-optimize input.png --colors 256
```

## ☁️ Azure Integration

### Azure Blob Storage

Upload optimized images directly to Azure:

```bash
# Upload to Azure Blob Storage
csa-image-optimize ./images \
  --azure \
  --storage-account csamediastorage \
  --container multimedia-images \
  --public-access blob

# Use connection string
csa-image-optimize ./images \
  --azure \
  --connection-string "${AZURE_STORAGE_CONNECTION_STRING}" \
  --container images

# Set blob metadata
csa-image-optimize ./images \
  --azure \
  --storage-account csamediastorage \
  --container images \
  --blob-metadata "optimized=true" "tool=csa-optimizer"
```

### Azure CDN Integration

Deploy optimized images to Azure CDN:

```bash
# Upload and purge CDN
csa-image-optimize ./images \
  --azure \
  --storage-account csamediastorage \
  --container images \
  --cdn-profile csa-cdn \
  --cdn-endpoint csa-images \
  --purge-cdn

# Custom domain
csa-image-optimize ./images \
  --azure \
  --storage-account csamediastorage \
  --container images \
  --cdn-domain images.csa.azure.com
```

### Azure Computer Vision

Auto-generate alt text using Azure AI:

```bash
# Generate alt text
csa-image-optimize ./images \
  --azure-vision \
  --generate-alt-text \
  --output-metadata alt-text.json

# Configure Computer Vision
csa-image-optimize ./images \
  --azure-vision \
  --vision-endpoint "${AZURE_VISION_ENDPOINT}" \
  --vision-key "${AZURE_VISION_KEY}" \
  --generate-alt-text \
  --detect-objects
```

**Generated alt-text.json:**

```json
{
  "images": [
    {
      "filename": "architecture-diagram.png",
      "alt_text": "Architecture diagram showing Azure Synapse Analytics connected to Data Lake Storage with data flow arrows indicating ingestion, processing, and analytics stages",
      "objects_detected": ["diagram", "arrows", "cloud services"],
      "confidence": 0.94
    },
    {
      "filename": "dashboard-screenshot.png",
      "alt_text": "Power BI dashboard displaying sales metrics with bar charts and KPI tiles",
      "objects_detected": ["chart", "graph", "dashboard"],
      "confidence": 0.91
    }
  ]
}
```

## 📊 Validation & Quality Control

### Quality Validation

Ensure optimized images meet quality standards:

```bash
# Validate quality
csa-image-optimize input.jpg --validate-quality --min-quality 80

# Compare with original
csa-image-optimize input.jpg --output optimized.jpg --compare

# Generate quality report
csa-image-optimize ./images --output ./optimized --quality-report report.html
```

**Quality Metrics:**

- **SSIM** (Structural Similarity Index): 0.95-1.0 (excellent)
- **PSNR** (Peak Signal-to-Noise Ratio): >40 dB (excellent)
- **VMAF** (Video Multi-Method Assessment Fusion): >90 (excellent)
- **Butteraugli** (Perceptual difference): <1.0 (imperceptible)

### File Size Validation

Enforce file size limits:

```bash
# Maximum file size
csa-image-optimize ./images --max-size 500KB --output ./optimized

# Warn on large files
csa-image-optimize ./images --warn-size 300KB

# Auto-adjust quality to meet size target
csa-image-optimize input.jpg --target-size 200KB --output optimized.jpg
```

## 🔄 Automation & CI/CD

### GitHub Actions

```yaml
# .github/workflows/optimize-images.yml
name: Optimize Images

on:
  push:
    paths:
      - 'docs/multimedia/images/**'

jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Image Optimizer
        run: npm install -g @csa/image-optimizer

      - name: Optimize Images
        run: |
          csa-image-optimize docs/multimedia/images \
            --output site/assets/images \
            --format webp \
            --quality 85 \
            --responsive \
            --sizes 320,640,1024,1920

      - name: Upload to Azure
        run: |
          csa-image-optimize site/assets/images \
            --azure \
            --storage-account ${{ secrets.AZURE_STORAGE_ACCOUNT }} \
            --container multimedia-images \
            --connection-string "${{ secrets.AZURE_STORAGE_CONNECTION_STRING }}" \
            --cdn-profile csa-cdn \
            --purge-cdn

      - name: Generate Report
        run: |
          csa-image-optimize site/assets/images \
            --generate-report \
            --output optimization-report.html

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: optimization-report
          path: optimization-report.html
```

### Azure DevOps Pipeline

```yaml
# azure-pipelines.yml
trigger:
  paths:
    include:
      - docs/multimedia/images/*

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: NodeTool@0
  inputs:
    versionSpec: '18.x'

- script: |
    npm install -g @csa/image-optimizer
  displayName: 'Install Image Optimizer'

- script: |
    csa-image-optimize docs/multimedia/images \
      --output $(Build.ArtifactStagingDirectory)/images \
      --format webp \
      --quality 85 \
      --azure \
      --storage-account $(AZURE_STORAGE_ACCOUNT) \
      --connection-string "$(AZURE_STORAGE_CONNECTION_STRING)" \
      --container multimedia-images
  displayName: 'Optimize and Upload Images'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'optimized-images'
```

## 📝 Configuration File

Create `image-optimizer.config.js`:

```javascript
module.exports = {
  // Input/Output
  input: './docs/multimedia/images',
  output: './site/assets/images',

  // Formats
  formats: ['webp', 'jpg'],
  quality: {
    jpeg: 85,
    webp: 85,
    png: 85,
    avif: 80
  },

  // Responsive images
  responsive: {
    enabled: true,
    sizes: [320, 640, 1024, 1920],
    generateSrcset: true
  },

  // Azure integration
  azure: {
    enabled: true,
    storageAccount: process.env.AZURE_STORAGE_ACCOUNT,
    container: 'multimedia-images',
    connectionString: process.env.AZURE_STORAGE_CONNECTION_STRING,
    cdn: {
      profile: 'csa-cdn',
      endpoint: 'csa-images',
      purgeOnUpload: true
    },
    computerVision: {
      enabled: true,
      endpoint: process.env.AZURE_VISION_ENDPOINT,
      key: process.env.AZURE_VISION_KEY,
      generateAltText: true
    }
  },

  // Optimization
  optimization: {
    progressive: true,
    stripMetadata: true,
    optimizeColors: true
  },

  // Validation
  validation: {
    maxFileSize: '500KB',
    minQuality: 80,
    enforceAltText: true
  },

  // Performance
  parallel: true,
  workers: 4
};
```

Use config file:

```bash
csa-image-optimize --config image-optimizer.config.js
```

## 📚 API Reference

### JavaScript/Node.js

```javascript
const { ImageOptimizer } = require('@csa/image-optimizer');

const optimizer = new ImageOptimizer({
  quality: 85,
  format: 'webp',
  responsive: {
    sizes: [320, 640, 1024, 1920]
  }
});

// Optimize single image
await optimizer.optimize('input.jpg', 'output.webp');

// Optimize directory
await optimizer.optimizeDirectory('./images', './optimized');

// Get optimization stats
const stats = optimizer.getStats();
console.log(`Saved ${stats.totalSavings} bytes (${stats.percentSaved}%)`);
```

### Python

```python
from csa_image_optimizer import ImageOptimizer

optimizer = ImageOptimizer(
    quality=85,
    format='webp',
    responsive={'sizes': [320, 640, 1024, 1920]}
)

# Optimize single image
optimizer.optimize('input.jpg', 'output.webp')

# Optimize directory
optimizer.optimize_directory('./images', './optimized')

# Get stats
stats = optimizer.get_stats()
print(f"Saved {stats['total_savings']} bytes ({stats['percent_saved']}%)")
```

## 📚 Related Resources

- [Tools Overview](README.md)
- [Configuration Generator](config-generator.md)
- [Production Guide](../production-guide/README.md)
- [Asset Management](../production-guide/asset-management.md)

---

*Last Updated: January 2025 | Version: 1.0.0*
