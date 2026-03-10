#!/bin/bash

# Download sample fabric swatches for testing
# Uses Unsplash for free, high-quality texture images

echo "🎨 Downloading sample fabric swatches..."
echo ""

# Create directories
mkdir -p swatches/curtains
mkdir -p swatches/blinds
mkdir -p swatches/shades

# Counter
count=0

# Curtains - Various fabric textures
echo "📥 Downloading curtain fabrics..."

# Linen beige
curl -L -o swatches/curtains/linen_beige.jpg \
  "https://images.unsplash.com/photo-1541643600914-78b084683601?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ linen_beige.jpg"; fi

# Cotton white
curl -L -o swatches/curtains/cotton_white.jpg \
  "https://images.unsplash.com/photo-1615486991829-3f5b6f33e6cf?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ cotton_white.jpg"; fi

# Linen gray
curl -L -o swatches/curtains/linen_gray.jpg \
  "https://images.unsplash.com/photo-1604075311531-4e433c01e0be?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ linen_gray.jpg"; fi

# Velvet navy
curl -L -o swatches/curtains/velvet_navy.jpg \
  "https://images.unsplash.com/photo-1592170889910-56e8f491c9e2?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ velvet_navy.jpg"; fi

# Silk cream
curl -L -o swatches/curtains/silk_cream.jpg \
  "https://images.unsplash.com/photo-1594116511668-8b4b5d2163be?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ silk_cream.jpg"; fi

# Blinds - Wood and metal textures
echo ""
echo "📥 Downloading blind materials..."

# Wood oak
curl -L -o swatches/blinds/wood_oak.jpg \
  "https://images.unsplash.com/photo-1547389027-e2dfc6f17e3e?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ wood_oak.jpg"; fi

# Faux wood white
curl -L -o swatches/blinds/faux_wood_white.jpg \
  "https://images.unsplash.com/photo-1563089145-599997674d42?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ faux_wood_white.jpg"; fi

# Wood dark walnut
curl -L -o swatches/blinds/wood_walnut.jpg \
  "https://images.unsplash.com/photo-1614964107039-8d90e80dceba?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ wood_walnut.jpg"; fi

# Aluminum silver
curl -L -o swatches/blinds/aluminum_silver.jpg \
  "https://images.unsplash.com/photo-1588419189877-f397680b6465?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ aluminum_silver.jpg"; fi

# Shades - Soft fabrics
echo ""
echo "📥 Downloading shade fabrics..."

# Roller white
curl -L -o swatches/shades/roller_white.jpg \
  "https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ roller_white.jpg"; fi

# Cellular beige
curl -L -o swatches/shades/cellular_beige.jpg \
  "https://images.unsplash.com/photo-1541643600914-78b084683601?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ cellular_beige.jpg"; fi

# Roman tan
curl -L -o swatches/shades/roman_tan.jpg \
  "https://images.unsplash.com/photo-1604719312552-c89e8aa35a40?w=1024&q=80" 2>/dev/null
if [ $? -eq 0 ]; then ((count++)); echo "  ✓ roman_tan.jpg"; fi

echo ""
echo "✅ Downloaded $count sample swatches"
echo ""
echo "📁 Swatches saved to:"
echo "   swatches/curtains/ ($(ls swatches/curtains/*.jpg 2>/dev/null | wc -l) files)"
echo "   swatches/blinds/ ($(ls swatches/blinds/*.jpg 2>/dev/null | wc -l) files)"
echo "   swatches/shades/ ($(ls swatches/shades/*.jpg 2>/dev/null | wc -l) files)"
echo ""
echo "💡 To add vendor swatches, see: swatches/README.md"
