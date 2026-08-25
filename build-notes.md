# Bo Meubles website, build notes

**Platform target:** WordPress + Elementor Pro (Elementor v3 standard widgets, Flexbox Containers).
**Design system:** Intrio by Designesia, used as supplied. This is not a reinterpretation of the
template, it is the template with Bo Meubles content in it.
**Mockup:** `bomeubles-mockup/` (five pages plus a design kit). Open `index.html` in a browser.

---

## 1. What was and was not changed

The brief was that the design should be exactly the template. So:

**Unchanged:** every HTML class, the Bootstrap 5 grid, `css/style.css`, `css/plugins.css`,
`css/bootstrap.min.css`, `css/swiper.css`, `css/coloring.css`, `css/colors/scheme-01.css`, all
JavaScript, all section structure, all animation and carousel behaviour.

**Changed, and only this:**

| Change | Where | Why |
| --- | --- | --- |
| Copy, navigation, footer links | the five page files | Bo Meubles content |
| Photography | `images/` | client photography replaces the stock set, at the exact dimensions the template ships, so no CSS had to move |
| Logo | `images/logo.svg`, `images/logo-white.svg` | the client has no logo file, see section 7 |
| Dead Google Fonts `@import` removed | `css/style.css` line 14 | see section 6 |
| Four accessibility rules | `css/bo-meubles.css` (new, loads last) | see section 5 |
| Unused template pages deleted | blog, FAQ, testimonials, consultation, the four alternative homepages, the three style variants, the single-item pages | out of scope for a five page site |
| Blog section removed from the homepage | `index.html` | Bo Meubles has no blog. The markup is still in the pristine template if it is ever wanted |
| Team carousel removed from About | `about.html` | it needs four named people with portraits and social profiles. See section 8 |

Every one of these is reproducible: `python3 build.py` regenerates the five pages from the pristine
template in `../Intrio/Intrio HTML/`, and `./swap-template-images.sh` regenerates the imagery.
**Do not hand-edit the page files.** Edit `build.py` and re-run, or the next run overwrites you.

---

## 2. Global tokens, for Elementor Site Settings

### Global Colors

| Elementor slot | Hex | Template token | Used for |
| --- | --- | --- | --- |
| Primary | `#805231` | `--primary-color` | buttons, active states, icon accents, carousel arrows |
| Secondary | `#805231` | `--secondary-color` | scheme-01 sets it identical to primary |
| Text | `#341F16` | `--heading-font-color` | all headings |
| Accent | `#C89A6B` | added, see 5.1 | brand brown lightened for use on dark surfaces |
| Custom: Body text | `rgba(52,31,22,.75)` resolves to `#63564E` | `--body-font-color` | paragraphs on light |
| Custom: Surface | `#F0EBE5` | `--bg-default` | default page background |
| Custom: Surface light | `#F7F5F3` | `--bg-light` | alternating sections |
| Custom: Dark 1 | `#34241C` | `--bg-dark-1` | footer, dark bands, off-canvas panel |
| Custom: Dark 2 | `#433027` | `--bg-dark-2` | secondary dark surface |
| Custom: Dark 3 | `#524036` | `--bg-dark-3` | tertiary dark surface |

Section tinting uses `.bg-color-op-1` through `-op-4`, which is the primary colour at 10 to 40%
opacity. In Elementor this is a container background colour set to `rgba(128,82,49,0.1)`.

### Global Fonts

Elementor global fonts cannot express the template's values directly, so set responsive values per
breakpoint:

| Element | Desktop | Tablet | Mobile | Tracking | Line height | Transform |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | 96px | 72px | 48px | -0.02em | 0.85em | uppercase |
| H2 | 48px | 42px | 36px | -0.96px | 1em | uppercase |
| H3 | 26px | 24px | 22px | -0.4px | 1.5em | uppercase |
| H4 | 20px | 20px | 18px | -0.2px | 1.6em | uppercase |
| Body | 16px | 16px | 16px | -0.16px | 30px | none |
| Subtitle / eyebrow | 18px | 18px | 16px | 0 | 1.5em | uppercase, weight 500 |

Headings and body share one family. See section 6 before setting it.

### Layout

- Site Settings, Layout, Content Width **1200px**. The template also widens to 1304px above 1400px;
  match it with a container max width if you want exact parity, otherwise 1200px is fine.
- Section padding **100px top and bottom** desktop, **40px** below 768px.
- Spacer widget presets: **30 / 60 / 90px** (`.spacer-single`, `-double`, `-triple`).
- Border radius **0** everywhere (`--rounded-1: 0px`).
- Row gutter **24px** (`row g-4`).
- Breakpoints: desktop above 1024, tablet 768 to 1024, mobile below 768. These are Elementor's
  defaults and they match the template's media queries.

### Buttons

Padding `4px 30px` (`.btn-main` adds its own line height), font size 15px, weight bold, uppercase,
radius 0, white label on `#805231`, hover background `#805231`. Set Button width to **100%** on the
mobile breakpoint.

---

## 3. Page by page, section to Elementor mapping

Every section in the mockup carries the template's own comment markers. Widget choice is Elementor
Pro core first; addons only where the pattern genuinely needs one.

### 3.1 Header (Theme Builder, one template for all pages)

| Template markup | Elementor build |
| --- | --- |
| `header.transparent` absolute over the hero | Header template, Theme Builder. Container position **Absolute**, width 100%, background transparent, z-index 1001 |
| `#logo` with `.logo-main`, `.logo-scroll`, `.logo-mobile` | Image widget (Site Logo). Three variants are only needed if you want a different mark when the header sticks; otherwise one white logo |
| `ul#mainmenu` with one dropdown under Services | **Nav Menu** widget, WordPress menu `Primary`. Services has five children |
| `.btn-main.fx-slide` "Book a Showroom Visit" | Button widget. The slide-in label effect is template CSS; if you want it, keep the class, otherwise a normal hover is acceptable |
| Sticky behaviour | Motion Effects, Sticky Top, "Effects Offset" 0. The template's own `headerAutoshow` hides then re-shows on scroll up; reproduce with Sticky plus Elementor's scrolling effects, or accept a plain sticky header |
| `#menu-btn`, `#btn-extra`, `#extra-wrap` off-canvas panel | The off-canvas panel is **not** required. If wanted: JetPopup (Crocoblock) or Elementor Pro Off-Canvas, with the same content blocks (logo, selected work, service list, contact, about, socials) |

### 3.2 Footer (Theme Builder, one template for all pages)

Container, background `#34241C`, padding `100px 0 0`.
Row: two columns at 50%.

- Left: Image (white logo), Spacer 30, nested row with two Icon List widgets (Bespoke Work, Bo
  Meubles), then a Social Icons widget.
- Right: Heading "Get in Touch" plus an Image (arrow), then repeated Text Editor label + Heading
  pairs for Email, Phone, Office Location.
- Sub-footer: full width container, `border-top` 1px `rgba(241,235,224,.18)`, centred Text Editor
  with the copyright, the Namakoa credit and the site credit link.

**The site credit link is required on every page** and must survive the rebuild exactly:
`Website by <a href="https://xavïer.co/?ref=bo-meubles">xavïer.co</a>`. The domain contains **ï**;
do not normalise it, and do not drop the `?ref=bo-meubles` parameter.

### 3.3 Homepage, `index.html`

| # | Section | Elementor build |
| --- | --- | --- |
| 1 | Fullscreen hero, Swiper crossfade over two photos, headline split across two lines, three feature labels along the bottom | Full width container, min height 800px. **Slides widget** (Elementor Pro) with the two hero images, Ken Burns off, transition fade, 4s autoplay. Overlay: background overlay `#34241C` at 40%. Headline: two Heading widgets, first `h1`, second styled identically but `div`, right aligned. Feature labels: a three column container, `justify-content: space-between` |
| 2 | About strip: square image, heading, paragraph, sign-off | Container, row, three columns 33/33/33. Image widget, Heading widget, Text Editor plus Heading |
| 3 | Counter band, four figures | Container, row, four **Counter** widgets. Values 27, 60, 14, 5. Note two of them have no `+` suffix |
| 4 | Craft disciplines, six card carousel, centred, four visible | **Premium Carousel** (Premium Addons) or Elementor Pro **Loop Carousel** with a loop item template. Each card: image, gradient overlay bottom, Heading overlaid bottom left, arrow icon top right, image scales 1.2 on hover |
| 5 | Testimonials over a parallax photo, six slides, dots | Container with background image, **Background Effects, Scrolling Effect** for the parallax, plus `#34241C` overlay at 60%. **Testimonial Carousel** widget, one visible slide, dots on |
| 6 | Selected work, six project cards, two column carousel | Same carousel approach as 4. Each card adds a row of `.bg-blur` tag chips bottom left: a container with three Text Editor pills, background `rgba(255,255,255,.15)`, backdrop blur |
| 7 | Process, four steps with connector arrows | Container, row, four columns. **Icon Box** widget each. The connector arrow between steps is a `::after` in template CSS; in Elementor use an Icon widget between columns or accept no connector |
| 8 | Video call to action, full bleed image with a play button, opens a lightbox | Image widget with **Lightbox** enabled and a video URL, or Elementor Pro **Video** widget with a custom poster. **A video does not exist yet, see section 8** |
| 9 | FAQ accordion, five items | **Accordion** widget. First item closed by default, matching the template |

### 3.4 About, `about.html`

| Section | Elementor build |
| --- | --- |
| Page hero, dark band with a parallax workshop photo, breadcrumb, intro paragraph | Container, background image with Scrolling Effect, overlay `#34241C` 50%, gradient edge bottom. Heading `h1`, **Breadcrumbs** widget, Text Editor |
| About strip and sign-off | As homepage section 2 |
| Counter band | As homepage section 3 |
| Testimonials | As homepage section 5 |

### 3.5 Services, `services.html`

| Section | Elementor build |
| --- | --- |
| Page hero | As About |
| Six discipline cards, static three column grid, anchors `#kitchens` `#dressings` `#doors` `#bathroom` `#panelling` `#commercial` | Container, row, `col-lg-4 col-sm-6`. Each card as homepage section 4, but static rather than a carousel. Set the CSS ID on each card container so the header dropdown anchors work |

The header dropdown links to these anchors, so **the CSS IDs are load bearing**.

### 3.6 Projects, `projects.html`

| Section | Elementor build |
| --- | --- |
| Page hero | As About |
| Six project cards, two column grid, each with title overlay and three tag chips | Container, row, two columns. Same card pattern as homepage section 6. If the client wants to add projects themselves, build this as a **JetEngine** Projects CPT with a Listing Grid instead, fields: title, sector, location, detail, designer credit, gallery |

### 3.7 Contact, `contact.html`

| Section | Elementor build |
| --- | --- |
| Page hero | As About |
| Six info blocks in a two by three grid, then the enquiry form | Container, row, left column 50% holding a nested six cell grid of Heading + Text Editor; right column 50% holding the **Form** widget (Elementor Pro) |
| Form fields: Name, Email, Phone, Message | Form widget. Actions after submit: Email plus Redirect. Set the recipient to the confirmed Bo Meubles address. The template's `contact.php` and `js/validation-contact.js` are **not** used in a WordPress build |

Add a **Google Maps** widget once the showroom address is confirmed.

---

## 4. Contrast results, WCAG AA

Semi-transparent template colours are resolved against the surface they sit on before measuring.

| Pair | Resolved | Ratio | AA body (4.5) | AA large (3.0) |
| --- | --- | --- | --- | --- |
| Body text on cream | `#63564E` on `#F0EBE5` | 5.96:1 | Pass | Pass |
| Body text on light grey | `#63564E` on `#F7F5F3` | 6.50:1 | Pass | Pass |
| Headings on cream | `#341F16` on `#F0EBE5` | 13.09:1 | Pass | Pass |
| Brand brown on cream | `#805231` on `#F0EBE5` | 5.59:1 | Pass | Pass |
| Button label on brand brown | `#FFFFFF` on `#805231` | 6.63:1 | Pass | Pass |
| Body text on dark | `#D6D3D2` on `#34241C` | 9.97:1 | Pass | Pass |
| Headings on dark | `#FFFFFF` on `#34241C` | 14.84:1 | Pass | Pass |
| 50% muted text on dark | `#9A928E` on `#34241C` | 4.86:1 | Pass | Pass |
| Lightened brand on dark (our override) | `#C89A6B` on `#34241C` | 5.86:1 | Pass | Pass |
| **Stock brand brown on dark (replaced)** | `#805231` on `#34241C` | **2.24:1** | **Fail** | **Fail** |

The template's own palette passes AA everywhere except the last row, which is fixed in
`css/bo-meubles.css`. See 5.1.

White hero type sits over photography, so its contrast varies with the image. The two hero frames
are darkened during image preparation (see `swap-template-images.sh`) rather than by changing the
template's overlay, which keeps the design identical and the type legible.

---

## 5. Accessibility fixes carried in `css/bo-meubles.css`

This file loads last and is the only stylesheet that is not stock Intrio. Four rules, all of which
must be reproduced in the Elementor build.

**5.1 Brand brown on dark surfaces.** Intrio paints `.id-color` icons in `#805231`. On `#34241C`
that is 2.24:1. Lightened to `#C89A6B` (5.86:1) on dark surfaces only. In Elementor: set the icon
colour to `#C89A6B` in any widget placed on a dark container.

**5.2 Visible keyboard focus.** Stock Intrio has no focus styling at all, so keyboard users cannot
see where they are. A 3px `#C89A6B` outline with 3px offset is applied to links, buttons and form
fields. In Elementor: add this to Site Settings, Custom CSS, or to the child theme.

**5.3 Skip link.** A "Skip to content" link is added as the first element in the body, targeting
`#main-content` on the `<main>` element. **Do not use the id `content`**: the template already
styles `#content` with 90px padding and a background colour, and reusing it breaks the hero layout.

**5.4 Single `h1`.** The template splits the hero headline across two `h1` elements. The second is
changed to a `div` carrying the `.h1` class, so styling is identical and each page has exactly one
`h1`. In Elementor: set the second Heading widget's HTML tag to `div`.

The fifth rule in the file, `.mock-note`, is the mockup banner. **Delete the rule and its markup at
build time.**

---

## 6. Typography, decision required before build

The template's stylesheet requests a font that does not exist:

```
@import url('https://fonts.googleapis.com/css2?family=Google Sans:ital,wght@0,200;...');
```

"Google Sans" is not a public Google Fonts family, and the unescaped space makes the URL invalid, so
the request has always failed. Intrio has therefore always rendered in its fallback,
`Helvetica, Arial, sans-serif`. The mockup preserves that appearance exactly and the dead request is
removed so the browser does not chase a 404.

**This needs a decision.** Options:

1. **Keep the system stack** (Helvetica on Mac, Arial on Windows). Zero cost, zero load time, and
   identical to what the client has already seen. Renders noticeably differently across platforms.
2. **Licence a close geometric-humanist sans.** Google Sans Text is available commercially; the free
   families closest in feel are DM Sans, Figtree and Onest, all on Google Fonts.
3. **Choose a face deliberately for the brand**, which is a design conversation rather than a
   template one.

Whichever is chosen, load only the weights actually used: 400, 500 and 700.

---

## 7. Logo

Bo Meubles has no logo file. The mockup uses `images/logo.svg` and `images/logo-white.svg`, a
wordmark reconstructed from the client's own direction sketch: a circular gradient "BM" mark beside
"Bo Meubles" with "Meubles" in the brand brown, set in Georgia.

This is a stand-in, not an identity. It is built with a system serif so it renders everywhere, but a
real logo should be commissioned or supplied before launch. The template renders the logo at 130px
wide in the header and 150px in the footer, so any replacement should read clearly at that size.

---

## 8. Replace before launch

Everything here is either invented for the mockup or unconfirmed. Nothing in this table should go
live as it stands.

| Item | Current value | Status |
| --- | --- | --- |
| Phone | `+230 664 0178` | **Probably real.** Read off the team's branded workshop shirts in `Photos/L_atelier/IMG_9862.HEIC`. Confirm with the client |
| Trading name | `Bo Meubles & Cie Ltee` | **Probably real.** Same source. The client's own preview says "Bo Meubles Ltée", so confirm which is correct |
| Email | `hello@bomeubles.mu` | Invented. Domain not verified |
| Showroom address | `Royal Road, Pailles, Port Louis District` | **Invented.** The client's preview had a bracketed placeholder |
| Opening hours | Mon to Fri 08.00 to 16.30, Sat 08.00 to 12.00 | Invented |
| WhatsApp | `wa.me/2306640178` | Assumes the same number as the phone line |
| Six testimonials | homepage and About | **All invented**, each labelled `(placeholder)` in the copy. Collect real quotes with permission to publish |
| Counters | 27 years, 60 projects, 14 staff, 5 disciplines | Invented, except that "since 1998" and the five disciplines follow the client's own preview. The staff count is inferred from the workshop photographs |
| Social links | all `#` | No accounts supplied |
| Homepage video block | uses the template's YouTube lightbox | **No video exists.** Either commission a workshop film, or replace the block with a still image |
| Team section | removed from About | Needs four portraits, names, roles and consent before it can be rebuilt |
| Logo | reconstructed wordmark | See section 7 |
| Font | Helvetica fallback | See section 6 |

---

## 9. Photography

### 9.1 What was supplied and what condition it was in

Nothing in the supplied `Photos/` folder was web ready.

| Source | Count | Problem | Handling |
| --- | --- | --- | --- |
| `Photos/L_atelier/*.HEIC` | 15 | HEIC renders in no browser. Frames are portrait with an EXIF orientation tag that `sips` silently discards, so a naive conversion produces sideways images | Converted with ImageMagick `-auto-orient`, longest edge 1600px |
| `Photos/Namakoa/Water-Club-*` | 6 | usable, 1202 to 1428px wide | Converted, never upscaled |
| `Photos/Namakoa/Residence-Salines`, `Uniciti-Office`, `Tekoma-boutik` | 11 | only 800px wide | Converted. **Do not use full bleed at 2x**; they are fine at card size |
| `Photos/Namakoa/Mont-Choisy`, `Residence-Moka` | 9 | supplied as **GIF**, a 256 colour format that bands badly on photographs | Converted to JPEG. Ask Namakoa for the original JPEGs |
| `Photos/Projet CRE/CRE-Lobby1.png` | 1 | 1536x1024 PNG. The size and format both point to a render or an AI generated visual, not a photograph | **Excluded.** Confirm what it is before using it |
| `Necker-Finance-*.jpg` (project root) | 4 | same subject as the Uniciti office set but downloaded separately, so the licence may differ | **Excluded.** The Namakoa Uniciti frames are used instead |

Several Namakoa frames are diptychs, two photographs butted together in one file. The useful half is
cropped out in `convert-images.sh` for the bathroom vanity and one Water Club bedroom.

### 9.2 Rebuild the imagery

```bash
# from the project root
./bomeubles-mockup/convert-images.sh     # Photos/ -> bomeubles-mockup/images/bo-meubles-*.jpg
cd bomeubles-mockup && ./swap-template-images.sh   # -> the template's own image slots
```

`swap-template-images.sh` writes into the template's existing filenames at the exact dimensions it
ships, which is why no CSS or markup had to change. It is also the register of which client photo
sits in which slot.

### 9.3 Image register

| Template slot | Dimensions | Client source | Appears on |
| --- | --- | --- | --- |
| `images/slider/1.webp` | 2000x1121 | Water Club 4, darkened | homepage hero |
| `images/slider/2.webp` | 2000x1121 | Water Club 1, darkened | homepage hero |
| `images/background/1.webp` | 2000x1121 | workshop, timber stacks | testimonial parallax |
| `images/background/2.webp` | 1920x800 | workshop, main bay | inner page heroes, video block |
| `images/services/3.webp` | 1000x1350 | Salines kitchen | Kitchens |
| `images/services/4.webp` | 1000x1200 | workshop, oak shelving | Dressings and Wardrobes |
| `images/services/5.webp` | 1000x1350 | workshop, louvred shutters | Doors, Shutters and Screens |
| `images/services/6.webp` | 1000x1200 | Mont Choisy slatted wall | Panelling and Mouldings |
| `images/services/1.webp` | 1000x1350 | Moka vanity (diptych, left half) | Bathroom Furniture |
| `images/services/2.webp` | 1000x1200 | Necker reception | Commercial Fit-Outs |
| `images/projects-wide/1.webp` | 1000x563 | Salines wall library | Projects |
| `images/projects-wide/2.webp` | 1000x563 | Necker reception | Projects |
| `images/projects-wide/3.webp` | 1000x563 | Tekoma bar | Projects |
| `images/projects-wide/4.webp` | 1000x563 | Water Club living space | Projects |
| `images/projects-wide/5.webp` | 1000x563 | Mont Choisy bedroom | Projects |
| `images/projects-wide/6.webp` | 1000x563 | Moka room divider | Projects |
| `images/misc/s1.webp` | 1000x1000 | workshop, cane panel in an oak frame | About strip |
| `images/misc/c1-c3, l1-l3, s2, w1` | various | further workshop and project frames | available for the build |

The 15 converted workshop frames and 26 converted project frames are all in
`bomeubles-mockup/images/` as `bo-meubles-*.jpg`, so there is a larger library than the mockup uses.

### 9.4 Rights, which need settling

Every interior photograph belongs to a third party. The client's own preview granted rights only
"accordés par Namakoa".

- **Namakoa Interior Design** is credited in the footer and in the project copy on every page.
- EXIF names **Amaury Bouchet** on the Water Club frames and **Virginie Tennant** on Tekoma. Their
  photographer credit may be contractual and is currently **not** in the markup.
- The workshop photographs are the only images Bo Meubles unambiguously owns.

Confirm in writing what may be published and with what credit before launch.

---

## 10. SEO transfer

Enter these in SEOPress, per page.

| Page | Title (under 60) | Meta description (under 155) |
| --- | --- | --- |
| Home | Bo Meubles \| Bespoke joinery and furniture, Mauritius (55) | Mauritian cabinetmakers building bespoke kitchens, dressings, doors and furniture for homes, offices and hotels. Designed, made and fitted in house. (148) |
| About | The workshop \| Bo Meubles, Mauritius (37) | Inside the Bo Meubles workshop: cabinetmakers, finishers and fitters building bespoke joinery in Mauritius since 1998. (117) |
| Services | Bespoke joinery services \| Bo Meubles, Mauritius (49) | Bespoke kitchens, dressings, doors, panelling and bathroom furniture, designed and built in our Mauritius workshop and fitted by our own team. (140) |
| Projects | Projects \| Bo Meubles bespoke joinery, Mauritius (48) | Bespoke joinery projects by Bo Meubles: private residences, offices and hotels across Mauritius and Rodrigues. (110) |
| Contact | Contact and showroom \| Bo Meubles, Mauritius (44) | Visit the Bo Meubles showroom and workshop, or send us your project. Bespoke furniture and joinery made in Mauritius. (117) |

### Heading map

| Page | h1 | h2 | h3 / h4 |
| --- | --- | --- | --- |
| Home | "Bespoke Joinery" (the second hero line is a `div.h1`) | section titles, discipline card titles, project card titles, process step titles, FAQ questions | counter figures |
| About | "The Workshop" | about heading, testimonials | counter figures |
| Services | "What We Make" | overview heading | six discipline card titles are `h2`, keep them as `h2` |
| Projects | "Selected Work" | six project card titles | none |
| Contact | "Contact" | none in the body | six info block titles are `h4` |

### Transfer checklist

- [ ] One `h1` per page. The second hero line must be a `div`, not an `h1`
- [ ] Alt text on every content image. The template ships `alt=""` on all of them; the mockup fills
      in the 23 content images and correctly leaves the decorative arrows empty
- [ ] Descriptive anchor text, no "read more"
- [ ] Canonical per page, Open Graph title, description and image
- [ ] LocalBusiness schema: name, telephone, email, address, `areaServed` Mauritius. Add opening
      hours once confirmed
- [ ] XML sitemap, five URLs
- [ ] Redirects: the deleted template URLs (`blog`, `faq`, `testimonials`, `consultation`,
      `services-style-2` and so on) never go live, so no redirects are needed
- [ ] `lang="en-GB"` on `<html>`. The template ships `lang="en"`

---

## 11. Known template defects, inherited

These are Intrio's, not introduced by this build. Fix or accept, but know about them.

1. **Invalid Google Fonts URL.** Section 6. Removed in the mockup.
2. **`contact.js` 404.** The five homepage variants reference a root level `contact.js` that the
   template does not ship. Removed in the mockup.
3. **No focus styling.** Section 5.2. Fixed in the mockup.
4. **`#content` id collision.** Section 5.3. Worth knowing before you add any element with that id.
5. **Two `h1` elements in the hero.** Section 5.4. Fixed in the mockup.
6. **`#extra-wrap` is `position: fixed; right: -500px; width: 500px`.** It relies on
   `body { overflow: hidden }` to stay hidden. That works, but it is fragile: anything that changes
   the body overflow will expose a 500px horizontal scroll. In an Elementor build the off-canvas
   panel would be a popup instead, which avoids the problem entirely.

---

## 12. QA performed on the mockup

- Contrast: every pair in section 4 measured, all pass AA except the one that is overridden
- No em dashes in any file
- Site credit link present on all five pages with the `ref` parameter intact
- Exactly one `h1` per page, no skipped heading levels
- Every `src` and internal `href` resolves; no missing images, no dead links
- Alt text on all content images, empty alt on decorative arrows only
- Rendered at 500px, 768px, 1200px and 1440px. Note: headless Chrome clamps its viewport to a 500px
  minimum, so the narrowest capture is 500px rather than 375px. Check a real phone before sign-off
- Header confirmed transparent over the hero, as in the template
- JavaScript verified by DOM probe, not by eye: jQuery 3.7.1 loads, 2 Swiper hero slides, 3 Owl
  carousels initialise with 38 items, 4 counters, 58 WOW reveal elements, 1 jarallax band. The
  accordion click handler binds, sets `.active` and expands its panel to 140px. The mobile menu
  button binds and opens `#mainmenu`
- Not verified: counter animation on scroll, sticky header behaviour on scroll, and hover states.
  These need a real browser and a real scroll

---

## 13. Files

```
bomeubles-mockup/
  index.html  about.html  services.html  projects.html  contact.html
  bo-meubles-design-kit.html     tokens, type, components, live contrast table
  build.py                       regenerates the five pages from the pristine template
  convert-images.sh              Photos/ -> web ready client images
  swap-template-images.sh        client images -> the template's image slots
  css/bo-meubles.css             the only non-stock stylesheet, four accessibility rules
  css/ js/ fonts/ images/        Intrio, as supplied
```

`alt-clean-build/` at the project root holds an earlier, different direction: a from-scratch
five page mockup with its own tokens and typography, built before the decision to use the Intrio
design exactly. It is kept only for reference and is not part of this deliverable.
