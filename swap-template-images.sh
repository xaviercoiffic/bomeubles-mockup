#!/bin/bash
# Bo Meubles: replace the Intrio template's stock photography with the client's
# own images, at exactly the dimensions the template ships, so the markup and
# the CSS never have to change. Run from inside the mockup folder.
set -e
SRC="images"

# fit <source> <target> <WxH>  - centre crop to fill, never distort
fit () {
  magick "$SRC/$1" -auto-orient -resize "$3^" -gravity center -extent "$3" \
         -quality 82 "$SRC/$2"
}

# Hero slider (fullscreen swiper).
# Intrio's hero overlay is a 40% dark wash, tuned for the dark stock photography
# it ships with. The Bo Meubles interiors are bright, so white hero type sat too
# close to the background. The two hero frames are darkened here rather than
# changing the template's overlay values.
hero () {
  magick "$SRC/$1" -auto-orient -resize "2000x1121^" -gravity center -extent 2000x1121 \
         -brightness-contrast -20x8 -quality 82 "$SRC/$2"
}
hero bo-meubles-water-club-4.jpg  slider/1.webp
hero bo-meubles-water-club-1.jpg  slider/2.webp
fit bo-meubles-salines-1.jpg     slider-wide/1.webp   2000x900
fit bo-meubles-necker-offices-1.jpg slider-wide/2.webp 2000x900
fit bo-meubles-tekoma-1.jpg      slider-wide/3.webp   2000x900

# Parallax bands
fit bo-meubles-atelier-2.jpg     background/1.webp    2000x1121
fit bo-meubles-atelier-1.jpg     background/2.webp    1920x800

# Craft disciplines (portrait service cards)
fit bo-meubles-salines-3.jpg      services/3.webp     1000x1350   # Kitchens
fit bo-meubles-atelier-14.jpg     services/4.webp     1000x1200   # Dressings
fit bo-meubles-atelier-5.jpg      services/5.webp     1000x1350   # Doors and shutters
fit bo-meubles-mont-choisy-5.jpg  services/6.webp     1000x1200   # Panelling
fit bo-meubles-bathroom-vanity.jpg services/1.webp    1000x1350   # Bathroom furniture
fit bo-meubles-necker-offices-1.jpg services/2.webp   1000x1200   # Commercial fit out

# Landscape variants used on the services pages
fit bo-meubles-salines-3.jpg       services-landscape/1.webp 1000x563
fit bo-meubles-atelier-14.jpg      services-landscape/2.webp 1000x563
fit bo-meubles-atelier-5.jpg       services-landscape/3.webp 1000x563
fit bo-meubles-mont-choisy-5.jpg   services-landscape/4.webp 1000x563
fit bo-meubles-bathroom-vanity.jpg services-landscape/5.webp 1000x563
fit bo-meubles-necker-offices-1.jpg services-landscape/6.webp 1000x563

# Projects
fit bo-meubles-salines-1.jpg        projects-wide/1.webp 1000x563
fit bo-meubles-necker-offices-1.jpg projects-wide/2.webp 1000x563
fit bo-meubles-tekoma-1.jpg         projects-wide/3.webp 1000x563
fit bo-meubles-water-club-1.jpg     projects-wide/4.webp 1000x563
fit bo-meubles-mont-choisy-5.jpg    projects-wide/5.webp 1000x563
fit bo-meubles-moka-4.jpg           projects-wide/6.webp 1000x563

# About: square and portrait detail shots
fit bo-meubles-atelier-10.jpg    misc/s1.webp   1000x1000
fit bo-meubles-atelier-13.jpg    misc/s2.webp   1000x1000
fit bo-meubles-atelier-7.jpg     misc/c1.webp   1190x1320
fit bo-meubles-atelier-11.jpg    misc/c2.webp   1190x1320
fit bo-meubles-atelier-9.jpg     misc/c3.webp   1190x1320
fit bo-meubles-water-club-6.jpg  misc/l1.webp   2000x1271
fit bo-meubles-salines-4.jpg     misc/l2.webp   2000x1271
fit bo-meubles-necker-offices-3.jpg misc/l3.webp 2000x1271
fit bo-meubles-atelier-6.jpg     misc/w1.webp   1000x500

# Detail / product squares
fit bo-meubles-salines-2.jpg     products/1.webp 1000x1000
fit bo-meubles-atelier-10.jpg    products/2.webp 1000x1000
fit bo-meubles-necker-offices-4.jpg products/3.webp 1000x1000
fit bo-meubles-moka-1.jpg        products/4.webp 1000x1000

echo "Template imagery replaced with Bo Meubles photography."
