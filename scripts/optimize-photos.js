// scripts/optimize-photos.js
// Resize photos > 1200px wide, strip EXIF (removes GPS & camera metadata),
// and re-encode as progressive JPEG at quality 85. Skips anything already small.
//
// Run locally:  node scripts/optimize-photos.js
// Runs in CI:   .github/workflows/optimize-images.yml

const fs   = require("fs");
const path = require("path");
const sharp = require("sharp");

const DIR = "assets/images/people";
const MAX_WIDTH = 1200;
const QUALITY = 85;

async function processFile(file) {
  const full = path.join(DIR, file);
  const ext = path.extname(file).toLowerCase();
  if (![".jpg", ".jpeg", ".png", ".webp"].includes(ext)) return;

  const img = sharp(full);
  const meta = await img.metadata();

  // Skip if already optimized-size AND not a PNG (convert PNGs to JPG for size)
  if (meta.width && meta.width <= MAX_WIDTH && ext !== ".png") {
    // Still strip EXIF
    const tmp = full + ".tmp";
    await sharp(full).rotate().withMetadata({ exif: {} })
      .jpeg({ quality: QUALITY, progressive: true })
      .toFile(tmp);
    fs.renameSync(tmp, full.replace(/\.(jpeg|png|webp)$/i, ".jpg"));
    if (ext !== ".jpg") fs.existsSync(full) && fs.unlinkSync(full);
    console.log(`stripped: ${file}`);
    return;
  }

  const out = full.replace(/\.(jpeg|png|webp)$/i, ".jpg");
  const tmp = out + ".tmp";

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
