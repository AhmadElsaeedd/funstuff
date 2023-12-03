const sharp = require('sharp');

sharp('IMG_9218.png')
  .ensureAlpha() // This will add an alpha channel if it doesn't exist
  .toColourspace('rgba') // Convert to RGBA color space
  .toFile('Mawadda_RGBA.png', (err, info) => {
    if (err) throw err;
    console.log('Image converted to RGBA and saved as', info);
  });
