#!/bin/bash
# Bo Meubles - client photo conversion for web.
#
# Nothing in the supplied Photos/ folder is web ready:
#   - L_atelier is HEIC, which no browser renders, and the frames are portrait
#     with an EXIF orientation tag that sips silently discards, so they come out
#     rotated. ImageMagick -auto-orient is used instead.
#   - Mont-Choisy and Residence-Moka were supplied as GIF (256 colours).
#   - Most project frames are only 800px wide, so they are never upscaled.
#
# Run from the project root (the folder containing Photos/ and bomeubles-mockup/). Requires ImageMagick (brew install imagemagick).

set -e
SRC="Photos"
OUT="bomeubles-mockup/images"
mkdir -p "$OUT"

# $1 = shell glob pattern (unquoted at call site), $2 = slug, $3 = max edge
# Images smaller than the max edge are left at native size, never upscaled.
convert_series () {
  local slug=$1; local max=$2; shift 2
  local n=1
  for f in "$@"; do
    [ -e "$f" ] || continue
    magick "$f" -auto-orient -strip -resize "${max}x${max}>" \
           -quality 78 -interlace Plane "$OUT/bo-meubles-$slug-$n.jpg"
    n=$((n+1))
  done
}

# Workshop, the only imagery Bo Meubles unambiguously owns
convert_series atelier 1600 "$SRC"/L_atelier/*.HEIC

# Namakoa project series. Credit: Namakoa Interior Design.
convert_series water-club 1600 "$SRC"/Namakoa/"Copie de Water-Club"-*
convert_series salines 1600 "$SRC"/Namakoa/"Copie de Residence-Salines"-*
convert_series necker-offices 1600 "$SRC"/Namakoa/"Copie de Uniciti-Office"-*
convert_series tekoma 1600 "$SRC"/Namakoa/"Copie de Tekoma-boutik"-*
convert_series mont-choisy 1600 "$SRC"/Namakoa/"Copie de Mont-Choisy"-*
convert_series moka 1600 "$SRC"/Namakoa/"Copie de Residence-Moka"-*

echo "Done. $(ls -1 "$OUT"/*.jpg | wc -l | tr -d ' ') files written to $OUT"

# Several Namakoa frames are diptychs, two photographs butted together in one
# file. Cards need a single image, so the useful half is cropped out.
magick "$OUT/bo-meubles-moka-1.jpg"       -crop 48%x100%+0+0   +repage -quality 82 "$OUT/bo-meubles-bathroom-vanity.jpg"
magick "$OUT/bo-meubles-water-club-5.jpg" -crop 48%x100%+52%+0 +repage -quality 82 "$OUT/bo-meubles-water-club-bedroom.jpg"
echo "Crops written."
