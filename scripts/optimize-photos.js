// scripts/optimize-photos.js
// Resize photos > 1200px wide, strip EXIF (removes GPS & camera metadata),
// and re-encode as progressive JPEG at quality 85. Skips anything already small.
// SVG files are rasterized to JPEG (requires sharp built with librsvg support).
//
// Usage:
//   node scripts/optimize-photos.js          # optimize/convert all images in DIR
//
// Called from two places:
//   - .github/workflows/build.yml            (converts SVGs to JPEGs at build time;
//                                             nothing is committed back — the SVG
//                                             source files stay in the repo)
//   - .github/workflows/optimize-images.yml  (optimizes newly-pushed JPG/PNG/WebP
//                                             photos and commits the result back)

const fs   = require("fs");
const path = require("path");
const sharp = require("sharp");

const DIR = "assets/images/people";
const MAX_WIDTH = 1200;
const QUALITY = 85;

async function processFile(file) {
  const full = path.join(DIR, file);
  const ext = path.extname(file).toLowerCase();
  if (![".jpg", ".jpeg", ".png", ".webp", ".svg"].includes(ext)) return;

  if (ext === ".svg") {
    // Rasterize SVG → JPEG. SVG files have no EXIF; flatten transparency to white.
    const out = full.replace(/\.svg$/i, ".jpg");
    const tmp = out + ".tmp";
    await sharp(full)
      .flatten({ background: "#ffffff" })
      .resize({ width: MAX_WIDTH, withoutEnlargement: true })
      .jpeg({ quality: QUALITY, progressive: true })
      .toFile(tmp);
    // Validate output has non-zero size before removing the source SVG.
    const { size } = fs.statSync(tmp);
    if (size === 0) throw new Error(`converted JPEG is empty: ${tmp}`);
    fs.renameSync(tmp, out);
    fs.unlinkSync(full);
    console.log(`converted: ${file} -> ${path.basename(out)}`);
    return;
  }

  const img = sharp(full);
  const meta = await img.metadata();
  const out = full.replace(/\.(jpeg|png|webp)$/i, ".jpg");
  const tmp = out + ".tmp";

  // Skip if already optimized-size AND not a PNG (convert PNGs to JPG for size)
  if (meta.width && meta.width <= MAX_WIDTH && ext !== ".png") {
    // Still strip EXIF
    await sharp(full).rotate().withMetadata({ exif: {} })
      .jpeg({ quality: QUALITY, progressive: true })
      .toFile(tmp);
    fs.renameSync(tmp, out);
    if (ext !== ".jpg") fs.existsSync(full) && fs.unlinkSync(full);
    console.log(`stripped: ${file}`);
    return;
  }

  await sharp(full)
    .rotate()                               // honor EXIF orientation, then drop it
    .resize({ width: MAX_WIDTH, withoutEnlargement: true })
    .withMetadata({ exif: {} })             // strip EXIF (GPS, camera)
    .jpeg({ quality: QUALITY, progressive: true })
    .toFile(tmp);

  fs.renameSync(tmp, out);
  if (full !== out && fs.existsSync(full)) fs.unlinkSync(full);
  console.log(`optimized: ${file} -> ${path.basename(out)}`);
}

(async () => {
  if (!fs.existsSync(DIR)) { console.log("no photos dir"); return; }
  for (const file of fs.readdirSync(DIR)) {
    try { await processFile(file); }
    catch (e) { console.error(`failed: ${file}`, e.message); }
  }
})();
