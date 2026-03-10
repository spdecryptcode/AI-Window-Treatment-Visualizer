# User Guide - Sales Rep Workflow

Complete guide for using the Window Treatment Visualizer in customer consultations.

---

## Quick Start

1. **Start the application** (if not already running)
2. **Open browser** to `http://localhost:3000`
3. **Upload room photo** from customer
4. **Select window** (auto-detected or manual)
5. **Choose treatment** and swatch
6. **Generate preview** (wait 5-15 seconds)
7. **Show customer** before/after comparison
8. **Export PDF** for consultation record

---

## Detailed Workflow

### Step 1: Prepare Room Photo

**Best practices for photos:**

✅ **DO:**
- Use well-lit room (natural or artificial light)
- Capture entire window clearly
- Take photo straight-on (perpendicular to window)
- Use landscape orientation
- Ensure window is unobstructed
- Take 1920x1080 or higher resolution

❌ **DON'T:**
- Extreme angles or distorted perspective
- Very dark or backlit scenes
- Blurry or out-of-focus images
- Heavy Instagram filters
- Photos with existing treatments (if possible)

**Getting photos from customers:**

- **Option A:** Take photo during in-home consultation
- **Option B:** Ask customer to email photo before meeting
- **Option C:** Use photo from virtual consultation

**File format:** JPG or PNG, max 10MB

---

### Step 2: Upload Image

1. Click **"Upload Room Photo"** or drag-and-drop
2. System will auto-resize if needed (maintains aspect ratio)
3. Preview appears showing uploaded image
4. Processing begins automatically

**Upload time:** <5 seconds on typical connection

**Troubleshooting:**
- File too large? Resize on phone/camera before upload
- Upload fails? Check internet connection (if using cloud version)
- Wrong orientation? System auto-rotates based on EXIF data

---

### Step 3: Window Detection

**Automatic detection:**

System automatically analyzes image and draws **bounding boxes** around detected windows:

- **Green box** = High confidence (>70%)
- **Yellow box** = Medium confidence (50-70%)
- **Red box** = Low confidence (<50%)

**If detection works:**
1. Click on the detected window box to select it
2. Multiple windows? Select the one customer wants to treat
3. Proceed to Step 4

**If detection fails or is inaccurate:**

Use **Manual Selection Tool**:

1. Click **"Draw Window Manually"** button
2. Click and drag to draw rectangle around window
3. Adjust corners by dragging handles
4. Click **"Confirm"** when satisfied

**Tips:**
- Include window frame in selection
- Don't include too much wall
- For bay windows, you can draw multiple regions or one large region

---

### Step 4: Review Segmentation (Optional)

After window selection, system creates precise mask of glass and frame.

**Mask overlay shows:**
- Blue = Glass area
- Orange = Frame
- Transparent = Wall/other

**If mask looks wrong:**

1. Click **"Refine Mask"**
2. Use brush tool to add/remove areas
3. Brush size adjustable with slider
4. Click **"Apply"** when done

**Note:** Clean mask = better rendering quality. Take 30 seconds to refine if needed.

---

### Step 5: Select Treatment Type

Choose from available treatment types:

**Curtains/Drapes**
- Full-length fabric panels
- Best for: Living rooms, bedrooms, formal spaces
- Options: Single panel, pair, layered

**Roller Shades**
- Flat fabric that rolls up
- Best for: Modern spaces, offices, small windows
- Options: Blackout, light filtering, sheer

**Roman Shades**
- Fabric with horizontal folds
- Best for: Kitchen, bathroom, traditional style
- Options: Flat fold, hobbled, relaxed

**Horizontal Blinds**
- Adjustable slats (wood, faux wood, aluminum)
- Best for: Offices, casual spaces, budget-friendly
- Options: 2", 2.5", or 3" slat width

**Vertical Blinds**
- Vertical slats
- Best for: Sliding glass doors, large windows
- Options: Fabric, PVC, aluminum

**Cellular Shades**
- Honeycomb structure for insulation
- Best for: Energy efficiency, bedrooms
- Options: Single cell, double cell

**Select the treatment type that matches customer interest.**

---

### Step 6: Choose Swatch

**Swatch gallery displays:**
- Fabric/material samples
- Organized by treatment type (auto-filtered)
- Vendor name
- Material type (e.g., "Linen", "Faux Wood")
- Color name

**Filter options:**
- Vendor: Select specific vendor catalog
- Color family: White, beige, gray, blue, etc.
- Material: Linen, cotton, polyester, wood, etc.
- Price tier: Budget, mid-range, premium (if configured)

**Swatch preview:**
- Click swatch for full-size preview
- Shows texture detail
- Use zoom to see fabric weave

**Try multiple swatches:**
- Select 4-6 swatches for comparison
- System can render all in batch mode (faster than one-by-one)
- Great for showing customer options

---

### Step 7: Adjust Settings (Optional)

**Treatment Settings:**

**Length:**
- Floor length (curtains touch floor)
- Sill length (ends at window sill)
- Below sill (4-6" below sill)
- Custom (specify inches)

**Fullness:** (Curtains only)
- Standard (2x width)
- Extra full (2.5x width)
- Minimal (1.5x width)

**Hardware:**
- Show mounting rod/track
- Hide mounting hardware
- Color: White, black, nickel, bronze, wood

**Lighting adjustment:**
- Auto-match room lighting (recommended)
- Brighten (+10% to +50%)
- Darken (-10% to -50%)

**Most users skip this step and use defaults.**

---

### Step 8: Generate Preview

1. Click **"Generate Preview"** button
2. Progress indicator shows:
   - "Detecting window..." (2s)
   - "Creating treatment..." (2-3s)
   - "Rendering photorealistic view..." (3-10s)
3. Total time: **5-15 seconds** depending on mode

**Rendering modes:**

**Classical (Fast):**
- Processing time: 5-7 seconds
- Quality: Very good, slight "CG" look
- Best for: Quick previews, multiple options

**AI Enhanced (Slow):**
- Processing time: 10-15 seconds
- Quality: Photorealistic, AI-generated
- Best for: Final presentation, high-end sales

**Default mode set by administrator.**

**While waiting:**
- Progress bar shows status
- Can't cancel once started
- System is working - don't refresh page

---

### Step 9: Review & Compare

**Before/After View:**

**Slider mode:**
- Drag slider left/right to reveal before vs after
- Great for dramatic reveal to customer
- Default view

**Side-by-side mode:**
- Click "Side by Side" button
- Shows both images at once
- Good for detailed comparison

**Zooming:**
- Click "Zoom" to see detail
- Pan around image
- Check shadow quality, edge blending, texture

**Customer presentation tips:**
- Start with "before" fully visible
- Slowly drag slider to reveal "after"
- Point out how fabric complements room
- Zoom on treatment to show texture detail

**If result looks wrong:**
- Check window selection (did it capture full window?)
- Try refining mask
- Try different swatch (some textures render better)
- Adjust lighting settings

---

### Step 10: Try Additional Swatches (Optional)

**Compare multiple options:**

1. Click **"Try Another Swatch"**
2. System keeps window detection/mask (saves time!)
3. Select different swatch
4. Generates new preview in ~5 seconds (faster - uses cache)
5. Repeat for 3-4 options

**Batch comparison mode:**

1. Check boxes next to 4-6 swatches
2. Click **"Compare All"**
3. Generates grid of all options (~30 seconds total)
4. Customer can see all side-by-side
5. Click any to see full before/after

**Very effective sales technique!**

---

### Step 11: Export Results

**Export Options:**

**High-Resolution PNG:**
- Full-quality image (original resolution)
- Perfect for emailing customer
- Can print 8x10 or larger
- No company branding (clean image)

**Consultation PDF:**
- Professional layout with company logo
- Before/after images side-by-side
- Treatment details:
  - Type (e.g., "Roman Shades")
  - Vendor and product line
  - Material and color name
  - Estimated price (if configured)
- Consultation date
- Sales rep name and contact
- Customer name (fill in form)
- Notes section

**Export workflow:**

1. Click **"Export"** button
2. Choose format: PNG or PDF
3. For PDF, fill in:
   - Customer name
   - Address (optional)
   - Phone/email (optional)
   - Notes (e.g., "Measurement scheduled for...")
4. Click **"Generate PDF"**
5. PDF opens in new tab
6. Save or print from browser

**File naming:**
- PNG: `WindowTreatment_[CustomerName]_[Date].png`
- PDF: `Consultation_[CustomerName]_[Date].pdf`

**Sending to customer:**

- **Email:** Attach PDF/PNG to email
- **Text:** Share via messaging app
- **Print:** Print PDF for in-person handoff
- **Cloud:** Upload to Dropbox/OneDrive and share link

---

### Step 12: Save to CRM (Optional)

If integrated with CRM:

1. Click **"Save to CRM"**
2. Select customer from dropdown or create new
3. Associate with opportunity/quote
4. Images and details auto-saved
5. Accessible in CRM record

---

## Advanced Features

### Multi-Window Rooms

**For rooms with multiple windows:**

1. System detects all windows automatically
2. Click **"Select All Windows"** to treat identically
3. Or select windows individually for different treatments
4. Click **"Apply to Selected"** to use same swatch on multiple
5. Generate preview shows all windows treated

**Different treatments per window:**
- Select first window → choose treatment A → generate
- Select second window → choose treatment B → generate
- System composites both onto same room image

### Layered Treatments

**Combine multiple treatment types:**

1. Apply first treatment (e.g., roller shade)
2. Click **"Add Layer"**
3. Select second treatment (e.g., curtain panels)
4. System renders both/showing layered effect
5. Great for upselling!

### Virtual Staging

**For empty rooms or poor photos:**

1. Upload room photo
2. Click **"Enhance Room"** (if available)
3. AI adjusts:
   - Lighting/brightness
   - Color correction
   - Remove clutter (experimental)
4. Then proceed with window treatment

### Saved Templates

**Create reusable combinations:**

1. After creating great combo, click **"Save as Template"**
2. Name it (e.g., "Modern Minimalist", "Farmhouse Chic")
3. Includes: treatment type + swatch + settings
4. Re-apply to future rooms with one click
5. Great for brand consistency

---

## Tips for Best Results

### Photography Tips

**Lighting:**
- Morning or afternoon light (not harsh noon sun)
- Turn on room lights for even illumination
- Avoid extreme backlighting from window

**Angle:**
- Stand directly in front of window (not at angle)
- Camera height at window mid-point
- Use portrait mode for very tall windows

**Framing:**
- Include 12-18" of wall around window
- Capture floor line (helps with depth)
- Include ceiling if possible
- Don't crop window edges

### Treatment Selection Tips

**Match room style:**
- Modern spaces → roller shades, minimal curtains
- Traditional → drapes, Roman shades
- Transitional → cellular shades, simple panels

**Match function:**
- Bedrooms → blackout liners
- Living rooms → light filtering
- Bathrooms → privacy (top-down bottom-up)
- Sliding doors → vertical blinds or panel track

**Color selection:**
- Neutral = appeals to most customers
- Bold colors = show 2-3 options (include neutral)
- Match existing room colors for coherence

### Quality Optimization

**If preview looks fake:**
- Refine window mask (most common issue)
- Adjust lighting match setting
- Try different swatch (some textures work better)
- Check source photo quality

**If shadows look wrong:**
- Verify window depth detected correctly
- Adjust mounting depth setting
- Classical mode = more predictable shadows

**If colors don't match:**
- Use auto-adjust lighting (usually fixes it)
- Check room photo white balance
- Manually adjust brightness up/down

---

## Troubleshooting

### Common Issues

**"No windows detected"**
- Photo too dark → use manual selection
- Window obstructed → crop/retake photo
- Glass very reflective → try different angle
- Use manual draw tool

**"Processing failed"**
- Image too large → system should auto-resize, but try resizing manually
- Corrupted file → re-export from phone/camera
- Server overload → wait 30 seconds and retry

**"Preview looks blurry"**
- Source image low resolution → retake at higher quality
- Mesh not aligned → refine window mask
- SDXL rendering sometimes blurry → switch to Classical mode

**"Wrong perspective"**
- Extreme photo angle → retake straight-on
- Bay window confusing detector → use manual selection + adjust geometry
- Depth estimation failed → check mask quality

**"Color is wrong"**
- Auto-match failed → manually adjust lighting slider
- Swatch itself is off → verify swatch image is color-accurate
- Monitor calibration → customer's screen may show differently

**"Takes too long"**
- First render slower (models loading) → subsequent renders faster
- SDXL mode slower than Classical → switch modes
- Large image → reduce upload size
- Check system isn't running other GPU tasks

### Getting Help

1. Click **"Help"** in top-right corner
2. Search knowledge base
3. Contact support: support@yourcompany.com
4. Include screenshot if possible

---

## Keyboard Shortcuts

- `Ctrl/Cmd + U` - Upload image
- `Ctrl/Cmd + D` - Manual draw window
- `Ctrl/Cmd + G` - Generate preview
- `Ctrl/Cmd + S` - Save/export
- `Ctrl/Cmd + Z` - Undo
- `Space` - Toggle before/after
- `Arrow keys` - Move slider
- `+/-` - Zoom in/out

---

## Sales Best Practices

### First Meeting

1. **Take multiple room photos** during walkthrough
2. **Ask customer preferences:** style, color, budget
3. **Show 2-3 options** using system
4. **Email PDF** before leaving
5. **Schedule follow-up** for measurement

### Virtual Consultation

1. **Ask customer to send photos** (include photo guide)
2. **Screen share during call** to show live rendering
3. **Try 4-5 options together** on call
4. **Send all PDFs** after call
5. **Customer can review and decide**

### Overcoming Objections

**"I can't visualize it"**
→ Perfect use case! Show live preview in 10 seconds.

**"That color might not match"**
→ Try 3-4 colors side-by-side, they can see which matches.

**"Too expensive"**
→ Show budget option first, then upgrade rendering to show value.

**"I need to think about it"**
→ Send PDF for review, schedule follow-up with measurement appointment.

### Upselling Techniques

1. **Show basic option first** (single shade)
2. **Then show layered** (shade + curtain panels)
3. **Visual difference** obvious and compelling
4. **Higher close rate** on upgraded options

---

## FAQ

**Q: Can I use photos from online listings?**
A: Yes, but quality varies. Best results with original photos.

**Q: Do I need internet connection?**
A: After initial setup, system works 100% offline.

**Q: How accurate is the preview?**
A: Very accurate for perspective/scale. Color may vary slightly based on monitor calibration and lighting.

**Q: Can customers use this themselves?**
A: System is designed for sales rep use. Customer-facing version available separately.

**Q: What if customer wants a swatch not in system?**
A: Contact admin to add vendor swatches. Can usually add within 24-48 hours.

**Q: Does this work on tablets/phones?**
A: Desktop/laptop only. Requires GPU hardware.

**Q: Can I show multiple rooms?**
A: Yes, upload multiple images and treat separately or create combined presentation.

**Q: Is there a limit to renderings?**
A: No limit. Generate as many as needed.

**Q: Can I edit the preview?**
A: Limited adjustments (lighting, treatment settings). For major edits, adjust source photo and re-render.

**Q: How do I add my logo to PDFs?**
A: Admin setting. Contact support to configure branding.

---

## Support & Training

**New user orientation:** 30-minute walkthrough (schedule with manager)

**Video tutorials:** Available at `http://localhost:3000/help`

**Practice images:** Use sample room photos in `test_data/` folder

**Support email:** support@yourcompany.com

**Support hours:** Monday-Friday 9am-5pm

---

**User Guide Version:** 1.0  
**Last Updated:** February 16, 2026  
**For:** Production System v1.0
