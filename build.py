#!/usr/bin/env python3
"""Bo Meubles site build on the Intrio template.

Reads the pristine template pages from ../Intrio/Intrio HTML/, applies the
Bo Meubles content, and writes the result here. Nothing about the template's
markup, classes, grid or CSS is changed: only copy, links, image files and a
handful of genuine template defects (a 404 script, an invalid font URL).

Run:  python3 build.py
"""
import re, pathlib, sys

HERE = pathlib.Path(__file__).parent
TPL = HERE.parent / "Intrio" / "Intrio HTML"

PHONE = "+230 664 0178"
PHONE_HREF = "+2306640178"
WA = "https://wa.me/2306640178"
EMAIL = "hello@bomeubles.mu"
ADDRESS = "Royal Road, Pailles, Port Louis District"
HOURS = "Monday to Friday 08.00 - 16.30, Saturday 08.00 - 12.00"

TITLES = {
    "index.html":    ("Bo Meubles | Bespoke joinery and furniture, Mauritius",
                      "Mauritian cabinetmakers building bespoke kitchens, dressings, doors and furniture for homes, offices and hotels. Designed, made and fitted in house."),
    "about.html":    ("The workshop | Bo Meubles, Mauritius",
                      "Inside the Bo Meubles workshop: cabinetmakers, finishers and fitters building bespoke joinery in Mauritius since 1998."),
    "services.html": ("Bespoke joinery services | Bo Meubles, Mauritius",
                      "Bespoke kitchens, dressings, doors, panelling and bathroom furniture, designed and built in our Mauritius workshop and fitted by our own team."),
    "projects.html": ("Projects | Bo Meubles bespoke joinery, Mauritius",
                      "Bespoke joinery projects by Bo Meubles: private residences, offices and hotels across Mauritius and Rodrigues."),
    "contact.html":  ("Contact and showroom | Bo Meubles, Mauritius",
                      "Visit the Bo Meubles showroom and workshop, or send us your project. Bespoke furniture and joinery made in Mauritius."),
}

MAINMENU = '''<ul id="mainmenu">
                                    <li><a class="menu-item" href="index.html">Home</a></li>
                                    <li><a class="menu-item" href="about.html">About</a></li>
                                    <li><a class="menu-item" href="services.html">Services</a>
                                        <ul>
                                            <li><a href="services.html#kitchens">Kitchens</a></li>
                                            <li><a href="services.html#dressings">Dressings &amp; Wardrobes</a></li>
                                            <li><a href="services.html#doors">Doors, Shutters &amp; Screens</a></li>
                                            <li><a href="services.html#panelling">Panelling &amp; Mouldings</a></li>
                                            <li><a href="services.html#bathroom">Bathroom Furniture</a></li>
                                        </ul>
                                    </li>
                                    <li><a class="menu-item" href="projects.html">Projects</a></li>
                                    <li><a class="menu-item" href="contact.html">Contact</a></li>
                                </ul>'''

FOOTER_1 = '''<h2 class="hs-5">Bespoke Work</h2>
                                    <ul>
                                        <li><a href="services.html#kitchens">Kitchens</a></li>
                                        <li><a href="services.html#dressings">Dressings &amp; Wardrobes</a></li>
                                        <li><a href="services.html#doors">Doors &amp; Shutters</a></li>
                                        <li><a href="services.html#panelling">Panelling &amp; Mouldings</a></li>
                                        <li><a href="services.html#bathroom">Bathroom Furniture</a></li>
                                    </ul>'''

FOOTER_2 = '''<h2 class="hs-5">Bo Meubles</h2>
                                    <ul>
                                        <li><a href="index.html">Home</a></li>
                                        <li><a href="about.html">The Workshop</a></li>
                                        <li><a href="projects.html">Projects</a></li>
                                        <li><a href="about.html#partners">For Architects</a></li>
                                        <li><a href="contact.html">Showroom &amp; Contact</a></li>
                                    </ul>'''

SIDE_SERVICES = '''<ul class="ul-check">
                    <li><a href="services.html#kitchens">Kitchens</a></li>
                    <li><a href="services.html#dressings">Dressings &amp; Wardrobes</a></li>
                    <li><a href="services.html#doors">Doors, Shutters &amp; Screens</a></li>
                    <li><a href="services.html#panelling">Panelling &amp; Mouldings</a></li>
                    <li><a href="services.html#bathroom">Bathroom Furniture</a></li>
                    <li><a href="services.html#commercial">Commercial Fit-Outs</a></li>
                </ul>'''

# --------------------------------------------------------------------------
# Copy shared by every page: header, off-canvas panel, footer.
# --------------------------------------------------------------------------
SHARED = [
    # Header call to action
    ('<a href="consultation.html" class="btn-main fx-slide"><span>Free Consultation</span></a>',
     '<a href="contact.html" class="btn-main fx-slide"><span>Book a Showroom Visit</span></a>'),
    # Off-canvas panel
    ('<h4 class="mb-3">Our Services</h4>', '<h4 class="mb-3">What We Make</h4>'),
    ('<div><i class="icofont-clock-time me-2 id-color"></i>Monday - Saturday 08.00 - 18.00</div>',
     f'<div><i class="icofont-clock-time me-2 id-color"></i>{HOURS}</div>'),
    ('<div><i class="icofont-location-pin me-2 id-color"></i>100 S Main St, New York, </div>',
     f'<div><i class="icofont-location-pin me-2 id-color"></i>{ADDRESS}</div>'),
    ('<div><i class="icofont-envelope me-2 id-color"></i>contact@intrio.com</div>',
     f'<div><i class="icofont-envelope me-2 id-color"></i><a href="mailto:{EMAIL}">{EMAIL}</a></div>'),
    ('<h4>About Us</h4>\n                <p>Transform your home, office, or commercial space with professional interior design services tailored to your vision and lifestyle. Our experienced designers create customized interiors, from concept development to final styling, ensuring every space reflects beauty, functionality, and attention to detail.</p>',
     '<h4>About Bo Meubles</h4>\n                <p>Bo Meubles is a Mauritian cabinetmaker. We draw, build and fit bespoke kitchens, dressings, doors, panelling and furniture for private houses, offices and hotels. Everything is measured on site, made in our own workshop and installed by the people who built it.</p>'),
    ('<h4 class="mb-3">Latest Projects</h4>', '<h4 class="mb-3">Selected Work</h4>'),
    # Footer contact block
    ('<h3>contact@intrio.com</h3>', f'<h3><a href="mailto:{EMAIL}">{EMAIL}</a></h3>'),
    ('<h3>+929 333 9296</h3>', f'<h3><a href="tel:{PHONE_HREF}">{PHONE}</a></h3>'),
    ('<h3>100 S Main St, New York, NY</h3>', f'<h3>{ADDRESS}</h3>'),
    ('Copyright 2026 Intrio by Designesia',
     'Copyright 2026 Bo Meubles &amp; Cie Ltee, Mauritius. '
     'Interior design credits: Namakoa Interior Design. '
     'Website by <a href="https://xavïer.co/?ref=bo-meubles">xavïer.co</a>'),
    ('<a href="#"><i class="fa-brands fa-whatsapp"></i></a>',
     f'<a href="{WA}" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>'),
    # Logo assets. The client has no logo file, so a wordmark built from their
    # own direction sketch stands in. See build-notes.md.
    ('src="images/logo-white.webp"', 'src="images/logo-white.svg"'),
    ('<link rel="icon" href="images/icon.webp" type="image/gif" sizes="16x16">',
     '<link rel="icon" href="images/logo.svg" type="image/svg+xml">'),
    # Template defect: the template ships a broken <html lang> value fix here.
    ('<html lang="en">', '<html lang="en-GB">'),
    # Accessibility and mockup banner, injected at the top of <body>.
    ('<body>\n\n        <!-- header begin -->',
     '<body>\n\n        <a class="skip-link" href="#content">Skip to content</a>\n\n'
     '        <!-- Mockup banner. Remove this div and the .mock-note rule at build. -->\n'
     '        <div class="mock-note"><strong>Design mockup.</strong> Some copy, photography and contact details are placeholders. See build-notes.md.</div>\n\n        <!-- header begin -->'),
]


# --------------------------------------------------------------------------
# Homepage copy
# --------------------------------------------------------------------------
INDEX = [
    # Hero
    ('<h1 class="fs-sm-10vw mb-0 wow fadeInLeft">Inspired Spaces</h1>',
     '<h1 class="fs-sm-10vw mb-0 wow fadeInLeft">Bespoke Joinery</h1>'),
    # The template splits the hero headline across two h1 elements. Only the
    # first stays an h1; the second keeps the identical styling via .h1.
    ('<h1 class="fs-sm-10vw mb-4 wow fadeInRight" data-wow-delay=".2s">Elevated Living</h1>',
     '<div class="h1 fs-sm-10vw mb-4 wow fadeInRight" data-wow-delay=".2s">Made In Mauritius</div>'),
    ('We design refined interiors that blend comfort and style, creating spaces that feel inviting and functional while reflecting your personality with thoughtful details and timeless elegance.',
     'Kitchens, dressings, doors and furniture, drawn and built to measure by our cabinetmakers. One workshop, from the first survey to the day we fit it.'),
    ('Functional Space Planning', 'Measured On Site'),
    ('Stylish Material Selection', 'Built In Our Workshop'),
    ('Tailored Design Concepts', 'Fitted By Our Own Team'),

    # About strip
    ('<div class="subtitle">About Us</div>', '<div class="subtitle">Our Conviction</div>'),
    ('We’re committed to turning your vision into reality',
     'We do not sell furniture, we build the way a room works'),
    ('We create spaces that are not only visually stunning but also functional and uniquely yours. Whether it’s a private residence or a commercial space, our interior design services are tailored to bring your vision to life with style and precision.',
     'Every piece starts on site, with a tape measure and a conversation. Nothing is ordered from a catalogue, so nothing has to be forced into a space it was not made for. Drawing, machining, assembly, finishing and fitting all happen under one roof.'),
    ('<img src="images/misc/signature.webp" class="w-150px" alt="">\n                                <h3 class="hs-5">John Smith</h3>',
     '<h3 class="hs-5">Bo Meubles &amp; Cie Ltee</h3>\n                                <div class="fs-15 op-7">Cabinetmakers since 1998</div>'),

    # Counters
    ('<span class="timer" data-to="65250" data-speed="3000">0</span>+</h3>\n                                Design Hours Completed',
     '<span class="timer" data-to="27" data-speed="3000">0</span></h3>\n                                Years In The Workshop'),
    ('<span class="timer" data-to="23160" data-speed="3000">0</span>+</h3>\n                                Satisfied Clients',
     '<span class="timer" data-to="60" data-speed="3000">0</span>+</h3>\n                                Projects Delivered'),
    ('<span class="timer" data-to="150" data-speed="3000">0</span>+</h3>\n                                Awards Winning',
     '<span class="timer" data-to="14" data-speed="3000">0</span></h3>\n                                Cabinetmakers &amp; Finishers'),
    ('<span class="timer" data-to="20" data-speed="3000">0</span>+</h3>\n                                Years of Design Experience',
     '<span class="timer" data-to="5" data-speed="3000">0</span></h3>\n                                Bespoke Disciplines'),

    # Services carousel
    ('<div class="subtitle">Our Services</div>', '<div class="subtitle">What We Make</div>'),
    ('Design Solutions Made for Living', 'One Craft, Five Disciplines'),
    ('We craft refined interior spaces with thoughtful planning and detail, combining style and comfort to create functional environments that reflect your personality and elevate everyday living with timeless appeal.',
     'Each discipline is its own trade, held to the same standard of fit and finish. Most projects use two or three of them together.'),
    ('<h2 class="fs-40">Furniture & Decor Selection</h2>', '<h2 class="fs-40">Kitchens</h2>'),
    ('<h2 class="fs-40">Concept Development</h2>', '<h2 class="fs-40">Dressings &amp; Wardrobes</h2>'),
    ('<h2 class="fs-40">Renovation & Space Planning</h2>', '<h2 class="fs-40">Doors, Shutters &amp; Screens</h2>'),
    ('<h2 class="fs-40">Visual Design Rendering</h2>', '<h2 class="fs-40">Panelling &amp; Mouldings</h2>'),
    ('<h2 class="fs-40">Residential Interior Design</h2>', '<h2 class="fs-40">Bathroom Furniture</h2>'),
    ('<h2 class="fs-40">Commercial Interior Design</h2>', '<h2 class="fs-40">Commercial Fit-Outs</h2>'),

    # Testimonials. All six are placeholders, see build-notes.md.
    ('They transformed our home into a warm, elegant space. Every detail felt intentional and refined.',
     'They read our drawings properly, asked the right questions early, and delivered on the date they gave us. That is rarer than it should be.'),
    ('Anna L., Paris', 'Interior designer, Namakoa Interior Design (placeholder)'),
    ('The layout and design exceeded expectations. Our space now feels larger, brighter, and more inviting.',
     'Our kitchen has an awkward angle in one corner. Nobody else wanted to touch it. Bo Meubles made it look deliberate.'),
    ('Michael H., Toronto', 'Private client, Black River (placeholder)'),
    ('They truly understood our vision. The result reflects our lifestyle with style and comfort.',
     'They built the bar in Mauritius, shipped it to Rodrigues and fitted it themselves. The whole job was one phone number.'),
    ('Nadia R., Dubai', 'Operations manager, Tekoma Boutik Hotel (placeholder)'),
    ('The entire process was smooth and inspiring. A truly professional and creative design team.',
     'The shop drawings came back dimensioned and on time, so the site programme never slipped because of joinery.'),
    ('Tom S., Los Angeles', 'Project architect, Moka (placeholder)'),
    ('From concept to finish, everything was flawless. Our home now feels both functional and beautiful.',
     'Two years on, every drawer still closes the way it did on the first day. That is what we paid for.'),
    ('Elise K., Amsterdam', 'Private client, Mont Choisy (placeholder)'),
    ('Creative ideas and excellent execution. They turned our space into something truly special.',
     'We asked them to match a cornice profile from an old colonial house. They machined it and you cannot tell the new from the old.'),
    ('David M., Singapore', 'Private client, Port Louis (placeholder)'),

    # Projects carousel
    ('<div class="subtitle">Latest Projects</div>', '<div class="subtitle">Selected Work</div>'),
    ('Thoughtfully Designed Spaces That Inspire', 'Projects That Asked The Most Of Us'),
    ('Explore a curated selection of our recent interior projects, where each space is thoughtfully designed to balance aesthetics and function while showcasing our attention to detail and timeless design approach.',
     'Private houses, offices and hotels across Mauritius and Rodrigues, built alongside the architects and interior designers who drew them.'),
    ('<h2 class="fs-36">Modern Minimalist Living Room</h2>', '<h2 class="fs-36">Wall Library, Salines</h2>'),
    ('<h2 class="fs-36">Luxury Contemporary Bedroom Suite</h2>', '<h2 class="fs-36">Necker Offices, Uniciti</h2>'),
    ('<h2 class="fs-36">Scandinavian Inspired Kitchen Design</h2>', '<h2 class="fs-36">Tekoma Boutik Hotel</h2>'),
    ('<h2 class="fs-36">Elegant Home Office Workspace</h2>', '<h2 class="fs-36">The Water Club, La Balise</h2>'),
    ('<h2 class="fs-36">Warm Rustic Dining Room Concept</h2>', '<h2 class="fs-36">Panelling, Mont Choisy</h2>'),
    ('<h2 class="fs-36">Luxury Bathroom With Marble Finish</h2>', '<h2 class="fs-36">Room Divider, Moka</h2>'),
    # Project tag chips, replaced as whole rows so short words stay unambiguous
    ('<div class="bg-blur p-2 me-2">Private Residence</div>\n                                                    <div class="bg-blur p-2 me-2">Open Space</div>\n                                                    <div class="bg-blur p-2 me-2">Contemporary</div>',
     '<div class="bg-blur p-2 me-2">Private Residence</div>\n                                                    <div class="bg-blur p-2 me-2">Black River</div>\n                                                    <div class="bg-blur p-2 me-2">Built-In Joinery</div>'),
    ('<div class="bg-blur p-2 me-2">Master Suite</div>\n                                                    <div class="bg-blur p-2 me-2">Luxury</div>\n                                                    <div class="bg-blur p-2 me-2">Soft Lighting</div>',
     '<div class="bg-blur p-2 me-2">Workplace</div>\n                                                    <div class="bg-blur p-2 me-2">Uniciti, Moka</div>\n                                                    <div class="bg-blur p-2 me-2">Solid Timber</div>'),
    ('<div class="bg-blur p-2 me-2">Kitchen</div>\n                                                    <div class="bg-blur p-2 me-2">Nordic Style</div>\n                                                    <div class="bg-blur p-2 me-2">Minimalist</div>',
     '<div class="bg-blur p-2 me-2">Hospitality</div>\n                                                    <div class="bg-blur p-2 me-2">Rodrigues</div>\n                                                    <div class="bg-blur p-2 me-2">Shipped &amp; Fitted</div>'),
    ('<div class="bg-blur p-2 me-2">Home Office</div>\n                                                    <div class="bg-blur p-2 me-2">Productivity</div>\n                                                    <div class="bg-blur p-2 me-2">Modern</div>',
     '<div class="bg-blur p-2 me-2">Hospitality</div>\n                                                    <div class="bg-blur p-2 me-2">La Balise Marina</div>\n                                                    <div class="bg-blur p-2 me-2">Fitted Kitchens</div>'),
    ('<div class="bg-blur p-2 me-2">Dining Area</div>\n                                                    <div class="bg-blur p-2 me-2">Rustic</div>\n                                                    <div class="bg-blur p-2 me-2">Natural Wood</div>',
     '<div class="bg-blur p-2 me-2">Private Residence</div>\n                                                    <div class="bg-blur p-2 me-2">Mont Choisy</div>\n                                                    <div class="bg-blur p-2 me-2">Panelling</div>'),
    ('<div class="bg-blur p-2 me-2">Bathroom</div>\n                                                    <div class="bg-blur p-2 me-2">Marble</div>\n                                                    <div class="bg-blur p-2 me-2">Premium Finish</div>',
     '<div class="bg-blur p-2 me-2">Private Residence</div>\n                                                    <div class="bg-blur p-2 me-2">Moka</div>\n                                                    <div class="bg-blur p-2 me-2">Screens &amp; Dressing</div>'),

    # Process
    ('<h2 class="hs-4">Consultation</h2>', '<h2 class="hs-4">Get In Touch</h2>'),
    ('We discuss your needs, style, and goals to understand your vision and space requirements clearly.',
     'Showroom, phone or WhatsApp. Tell us the room and the problem you want solved.'),
    ('<h2 class="hs-4">Concept Design</h2>', '<h2 class="hs-4">Survey &amp; Design</h2>'),
    ('Our team creates detailed concepts, layouts, and mood boards tailored to your lifestyle and taste.',
     'We measure on site, check the services, then return drawings, timber and finish options and a detailed quote.'),
    ('<h2 class="hs-4">Execution</h2>', '<h2 class="hs-4">Build</h2>'),
    ('We bring the design to life with quality materials, skilled work, and precise project management.',
     'Made in our own workshop, with progress photographs as the pieces come together.'),
    ('<h2 class="hs-4">Final Reveal</h2>', '<h2 class="hs-4">Fit &amp; Aftercare</h2>'),
    ('Your completed space is delivered beautifully finished, ready to enjoy with comfort and style.',
     'Delivery, installation, sign off and a guarantee you can actually call on. Same team throughout.'),

    # FAQ
    ('What services do you offer?', 'What exactly do you make?'),
    ('We offer commercial and residential interior design, 3D visualizations, renovation planning, concept development, and furniture/decor curation.',
     'Bespoke kitchens, dressings and wardrobes, interior doors, shutters and screens, wall panelling, skirtings and mouldings, and bathroom furniture. We also take on full commercial fit-outs for offices and hotels.'),
    ('How do I get started to get service?', 'How long does a bespoke project take?'),
    ("Simply contact us to schedule an initial consultation. We'll discuss your needs, style, budget, and timeline.",
     'A single fitted wardrobe is usually four to six weeks from approved drawings. A full kitchen is eight to twelve. Commercial fit-outs are programmed around the site. You get a date at quotation stage and we work to it.'),
    ('Do you handle renovations?', 'Do you work from an interior designer&#8217;s drawings?'),
    ('Yes, we offer renovation and space planning services, including layout optimization, material selection, and contractor coordination.',
     'Yes, and most of our commercial work arrives that way. We produce shop drawings from the design intent, return them for approval, and build only once they are signed off.'),
    ('What is included in the design process?', 'Can you match joinery in an older house?'),
    ('Our process includes concept development, mood boards, space planning, 3D visualizations, and final styling with furniture and decor.',
     'Usually. Bring us a photograph and, if you can, an offcut of a skirting or a moulding. We machine to profile, so matching a run of cornice or an old door style is routine work.'),
    ('How long does a project usually take?', 'Do you deliver outside the main island?'),
    ('Timelines vary by project size and scope. Small projects may take 2–4 weeks, while full renovations can take several months.',
     'Yes. We have built, packed, shipped and installed a complete bar and storage fit-out on Rodrigues. Freight and installation are quoted as part of the job.'),
]


# --------------------------------------------------------------------------
# Inner page copy
# --------------------------------------------------------------------------
INNER_LEAD = ('We create inspiring interiors that combine comfort, functionality, and timeless design. '
              'Every space is thoughtfully tailored to reflect your lifestyle and needs.')

SERVICE_TITLES = [
    ('Furniture & Decor Selection', 'Kitchens'),
    ('Concept Development',         'Dressings &amp; Wardrobes'),
    ('Renovation & Space Planning', 'Doors, Shutters &amp; Screens'),
    ('Visual Design Rendering',     'Panelling &amp; Mouldings'),
    ('Residential Interior Design', 'Bathroom Furniture'),
    ('Commercial Interior Design',  'Commercial Fit-Outs'),
]

PROJECT_TITLES = [
    ('Modern Minimalist Living Room',        'Wall Library, Salines'),
    ('Luxury Contemporary Bedroom Suite',    'Necker Offices, Uniciti'),
    ('Scandinavian Inspired Kitchen Design', 'Tekoma Boutik Hotel'),
    ('Elegant Home Office Workspace',        'The Water Club, La Balise'),
    ('Warm Rustic Dining Room Concept',      'Panelling, Mont Choisy'),
    ('Luxury Bathroom With Marble Finish',   'Room Divider, Moka'),
]

PROJECT_TAGS = [
    (('Private Residence', 'Open Space', 'Contemporary'),
     ('Private Residence', 'Black River', 'Built-In Joinery')),
    (('Master Suite', 'Luxury', 'Soft Lighting'),
     ('Workplace', 'Uniciti, Moka', 'Solid Timber')),
    (('Kitchen', 'Nordic Style', 'Minimalist'),
     ('Hospitality', 'Rodrigues', 'Shipped &amp; Fitted')),
    (('Home Office', 'Productivity', 'Modern'),
     ('Hospitality', 'La Balise Marina', 'Fitted Kitchens')),
    (('Dining Area', 'Rustic', 'Natural Wood'),
     ('Private Residence', 'Mont Choisy', 'Panelling')),
    (('Bathroom', 'Marble', 'Premium Finish'),
     ('Private Residence', 'Moka', 'Screens &amp; Dressing')),
]

TESTIMONIALS = [
    ('They read our drawings properly, asked the right questions early, and delivered on the date they gave us. That is rarer than it should be.',
     'Interior designer, Namakoa Interior Design (placeholder)'),
    ('Our kitchen has an awkward angle in one corner. Nobody else wanted to touch it. Bo Meubles made it look deliberate.',
     'Private client, Black River (placeholder)'),
    ('They built the bar in Mauritius, shipped it to Rodrigues and fitted it themselves. The whole job was one phone number.',
     'Operations manager, Tekoma Boutik Hotel (placeholder)'),
    ('The shop drawings came back dimensioned and on time, so the site programme never slipped because of joinery.',
     'Project architect, Moka (placeholder)'),
    ('Two years on, every drawer still closes the way it did on the first day. That is what we paid for.',
     'Private client, Mont Choisy (placeholder)'),
    ('We asked them to match a cornice profile from an old colonial house. They machined it and you cannot tell the new from the old.',
     'Private client, Port Louis (placeholder)'),
]

ABOUT_TESTIMONIAL_SOURCE = [
    'Their campaign made our brand shine online. Outstanding creativity and flawless execution.',
    'Our traffic grew beyond expectations. A truly data-driven and impactful partnership.',
    'The attention to our goals was amazing. Every ad reflected our brand perfectly.',
    'Working with them was effortless and inspiring. The best digital agency experience.',
    'From SEO to ads, everything delivered results. A partner we truly trust.',
    'Professional, creative, and results-driven. Our leads doubled in just two months.',
]
NAMES = ['Anna L., Paris', 'Michael H., Toronto', 'Nadia R., Dubai',
         'Tom S., Los Angeles', 'Elise K., Amsterdam', 'David M., Singapore']

COUNTERS = [
    ('data-to="65250" data-speed="3000">0</span>+</h3>\n                                Design Hours Completed',
     'data-to="27" data-speed="3000">0</span></h3>\n                                Years In The Workshop'),
    ('data-to="23160" data-speed="3000">0</span>+</h3>\n                                Satisfied Clients',
     'data-to="60" data-speed="3000">0</span>+</h3>\n                                Projects Delivered'),
    ('data-to="150" data-speed="3000">0</span>+</h3>\n                                Awards Winning',
     'data-to="14" data-speed="3000">0</span></h3>\n                                Cabinetmakers &amp; Finishers'),
    ('data-to="20" data-speed="3000">0</span>+</h3>\n                                Years of Design Experience',
     'data-to="5" data-speed="3000">0</span></h3>\n                                Bespoke Disciplines'),
]

CONTACT_OFFICES = [
    ('New York', '350 5th Ave, New York, NY 10118', '(212) 555-0134', 'nyc@musclecore.com',
     'Showroom &amp; Workshop', 'Royal Road, Pailles<br>Port Louis District, Mauritius', '', ''),
    ('Los Angeles', '742 S Hill St, Los Angeles, CA 90014', '(310) 555-0199', 'la@musclecore.com',
     'Call Or WhatsApp', PHONE, '', ''),
    ('Chicago', '233 S Wacker Dr, Chicago, IL 60606', '(312) 555-0147', 'chicago@musclecore.com',
     'Email Us', EMAIL, '', ''),
    ('Houston', '1200 Louisiana St, Houston, TX 77002', '(713) 555-0182', 'houston@musclecore.com',
     'Opening Hours', 'Monday to Friday, 08.00 - 16.30<br>Saturday, 08.00 - 12.00', '', ''),
    ('Miami', '100 Biscayne Blvd, Miami, FL 33132', '(305) 555-0174', 'miami@musclecore.com',
     'For Architects &amp; Designers', 'Shop drawings, site coordination<br>and off-island delivery', '', ''),
    ('Seattle', '701 5th Ave, Seattle, WA 98104', '(206) 555-0128', 'seattle@musclecore.com',
     'Visiting The Showroom', 'Free parking on site<br>Samples of every timber and finish', '', ''),
]


# Descriptive alt text. The template ships alt="" on every image; these are the
# content images the five pages actually use.
ALTS = {
    "images/services/3.webp": "Bespoke kitchen with dark shaker base units, timber shelves and a farmhouse sink",
    "images/services/4.webp": "Oak dressing room shelving under construction in the Bo Meubles workshop",
    "images/services/5.webp": "Louvred timber shutters stacked in the workshop, waiting for finishing",
    "images/services/6.webp": "Bedroom with a full height slatted timber headboard wall",
    "images/services/1.webp": "Timber bathroom vanity unit with a white countertop basin",
    "images/services/2.webp": "Office reception desk in stone and timber behind a slatted screen",
    "images/services-landscape/1.webp": "Bespoke kitchen with dark base units and timber shelving",
    "images/services-landscape/2.webp": "Oak dressing room shelving in the workshop",
    "images/services-landscape/3.webp": "Louvred timber shutters ready for finishing",
    "images/services-landscape/4.webp": "Slatted timber panelling behind a bed",
    "images/services-landscape/5.webp": "Timber bathroom vanity with a countertop basin",
    "images/services-landscape/6.webp": "Reception desk and timber claustra screen",
    "images/projects-wide/1.webp": "Arched built-in wall library with integrated lighting behind a rust coloured sofa",
    "images/projects-wide/2.webp": "Reception desk in stone and timber behind a slatted screen at the Necker offices",
    "images/projects-wide/3.webp": "Hotel bar with a dark timber counter and woven pendant lights at Tekoma",
    "images/projects-wide/4.webp": "Open plan living space with fitted joinery and a built-in timber desk",
    "images/projects-wide/5.webp": "Bedroom with slatted timber headboard panelling at Mont Choisy",
    "images/projects-wide/6.webp": "Bedroom with a timber slat screen dividing the sleeping and dressing areas",
    "images/misc/s1.webp": "Woven cane panel set into a solid oak frame on the workshop floor",
    "images/misc/s2.webp": "Tall timber shelving unit assembled in the workshop",
    "images/misc/w1.webp": "Louvred shutters leaning against the workshop wall",
    "images/background/1.webp": "Stacks of prepared timber inside the Bo Meubles workshop",
    "images/background/2.webp": "The main workshop bay with benches and machinery",
    "images/logo-white.svg": "Bo Meubles",
    "images/logo.svg": "Bo Meubles",
}


def add_alts(html):
    for src, alt in ALTS.items():
        html = html.replace('src="%s" class' % src, 'src="%s" alt="%s" class' % (src, alt))
        # normalise: drop the template's now duplicated empty alt on those tags
        html = html.replace('alt="%s" class="w-100 hover-scale-1-2" alt=""' % alt,
                            'alt="%s" class="w-100 hover-scale-1-2"' % alt)
    html = re.sub(r'(<img[^>]*\salt="[^"]+"[^>]*)\salt=""', r'\1', html)
    # The logo tags carry class before src, so they are handled by name.
    html = re.sub(r'(<img[^>]*src="images/logo(?:-white)?\.svg"[^>]*?)alt=""',
                  r'\1alt="Bo Meubles"', html)
    return html


def apply(html, pairs, label):
    """Apply replacements, reporting any that did not match so nothing fails silently."""
    missed = []
    for old, new in pairs:
        if old not in html:
            missed.append(old[:70])
            continue
        html = html.replace(old, new)
    if missed:
        print(f"  ! {label}: {len(missed)} replacement(s) did not match")
        for m in missed:
            print("      -", m)
    return html


def drop_section(html, marker):
    """Remove the whole <section> ... </section> that contains a marker string."""
    i = html.find(marker)
    if i == -1:
        print("  ! section marker not found:", marker[:50])
        return html
    start = html.rfind("<section", 0, i)
    end = html.find("</section>", i) + len("</section>")
    return html[:start] + "<!-- Blog section removed: Bo Meubles has no blog. See build-notes.md. -->\n            " + html[end:]


def common(html, slug):
    title, desc = TITLES[slug]
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, flags=re.S)
    html = re.sub(r'<meta content="Intrio[^"]*" name="description" >',
                  f'<meta content="{desc}" name="description" >', html)
    html = html.replace('<meta content="" name="keywords" >',
                        '<meta content="bespoke furniture Mauritius, made to measure kitchens, cabinetmaker, joinery, dressings, wardrobes" name="keywords" >')
    html = html.replace('<meta content="" name="author" >',
                        '<meta content="Bo Meubles &amp; Cie Ltee" name="author" >')
    html = re.sub(r'<ul id="mainmenu">.*?</ul>\s*(?=<!-- mainmenu end -->)',
                  MAINMENU + "\n                                ", html, flags=re.S)
    html = html.replace('<h2 class="hs-5">Quick Links</h2>', "@@F1@@", 1)
    html = html.replace('<h2 class="hs-5">Company</h2>', "@@F2@@", 1)
    html = re.sub(r"@@F1@@\s*<ul>.*?</ul>", FOOTER_1, html, flags=re.S)
    html = re.sub(r"@@F2@@\s*<ul>.*?</ul>", FOOTER_2, html, flags=re.S)
    html = re.sub(r'<ul class="ul-check">.*?</ul>', SIDE_SERVICES, html, flags=re.S)
    html = html.replace('src="images/logo.webp"', 'src="images/logo.svg"')  # not on every page
    # contact.js is referenced at the site root but never shipped, so it 404s.
    # It only appears on the homepage variants.
    html = html.replace('    <script src="contact.js"></script>\n', '')
    # Bo Meubles overrides load last so the template CSS stays untouched.
    # The template writes this tag with and without a trailing space.
    html = re.sub(r'(<link id="colors"[^>]*>)',
                  r'\1\n    <link href="css/bo-meubles.css" rel="stylesheet" type="text/css">',
                  html, count=1)
    html = html.replace('<main>', '<main id="main-content">')  # not "content": the template already styles #content
    html = apply(html, SHARED, slug + " shared")
    html = add_alts(html)
    # Single item pages are not part of this five page mockup
    html = html.replace('href="service-single.html"', 'href="services.html"')
    html = html.replace('href="project-single.html"', 'href="projects.html"')
    html = html.replace('href="blog-single.html"', 'href="index.html"')
    html = html.replace('href="consultation.html"', 'href="contact.html"')
    return html


def replace_titles(html, pairs, fmt):
    for old, new in pairs:
        needle = fmt.format(old)
        if needle not in html:
            print("  ! title not found:", old)
            continue
        html = html.replace(needle, fmt.format(new))
    return html


def replace_tags(html):
    for (o1, o2, o3), (n1, n2, n3) in PROJECT_TAGS:
        old = ('<div class="bg-blur p-2 me-2">%s</div>' % o1)
        # replace the trio as a group, matching whatever whitespace sits between
        pat = re.compile(r'<div class="bg-blur p-2 me-2">%s</div>(\s*)<div class="bg-blur p-2 me-2">%s</div>(\s*)<div class="bg-blur p-2 me-2">%s</div>'
                         % tuple(re.escape(x) for x in (o1, o2, o3)))
        def sub(m, n1=n1, n2=n2, n3=n3):
            return ('<div class="bg-blur p-2 me-2">%s</div>%s<div class="bg-blur p-2 me-2">%s</div>%s<div class="bg-blur p-2 me-2">%s</div>'
                    % (n1, m.group(1), n2, m.group(2), n3))
        html, n = pat.subn(sub, html)
        if n == 0:
            print("  ! tag trio not found:", o1, o2, o3)
    return html


def replace_testimonials(html, sources):
    for (quote, name), src in zip(TESTIMONIALS, sources):
        if src not in html:
            print("  ! testimonial not found:", src[:40])
            continue
        html = html.replace(src, quote)
    for old, (quote, name) in zip(NAMES, TESTIMONIALS):
        html = html.replace("<span>%s</span>" % old, "<span>%s</span>" % name)
        html = html.replace(">%s<" % old, ">%s<" % name)
    return html


def inner_hero(html, lead):
    return html.replace(INNER_LEAD, lead)


def main():
    if not TPL.exists():
        sys.exit("Template not found at %s" % TPL)

    # ---- index -----------------------------------------------------------
    html = common((TPL / "index.html").read_text(), "index.html")
    html = apply(html, INDEX, "index copy")
    html = drop_section(html, "Latest Blog")
    (HERE / "index.html").write_text(html)
    print("built index.html")

    # ---- about -----------------------------------------------------------
    html = common((TPL / "about.html").read_text(), "about.html")
    html = inner_hero(html, "Bo Meubles has been drawing, building and fitting bespoke joinery in Mauritius since 1998. Everything still passes through the same workshop floor.")
    html = html.replace("<h1 class=\"mb-3 wow fadeInUp\" data-wow-delay=\".2s\">About Us</h1>",
                        "<h1 class=\"mb-3 wow fadeInUp\" data-wow-delay=\".2s\">The Workshop</h1>")
    html = html.replace("<li class=\"active\">About Us</li>", "<li class=\"active\">About</li>")
    html = apply(html, [
        ("We\u2019re committed to turning your vision into reality",
         "We do not sell furniture, we build the way a room works"),
        ("We create spaces that go beyond being visually stunning, they are thoughtfully designed to be highly functional, deeply personal, and a true reflection of who you are. Every project we undertake is approached with a careful balance of creativity and practicality, ensuring that each element not only looks beautiful but also serves a meaningful purpose in your daily life.",
         "We keep the whole process in house: survey, drawing, machining, assembly, spraying and fitting. That is slower to set up and far easier to control. When something needs adjusting on site, the person who built it is the person who comes back. Timber comes in one end of the workshop and finished rooms leave the other."),
        # The template ships a handwritten signature of a fictional founder.
        # Bo Meubles has no such asset, so the block becomes a plain sign off.
        ("<img src=\"images/misc/signature.webp\" class=\"w-150px\" alt=\"\">\n                                <h3 class=\"hs-5\">John Smith</h3>",
         "<h3 class=\"hs-5\">Bo Meubles &amp; Cie Ltee</h3>\n                                <div class=\"fs-15 op-7\">Cabinetmakers since 1998</div>"),
        ("<div class=\"subtitle\">About Us</div>", "<div class=\"subtitle\">Our Conviction</div>"),
    ], "about copy")
    html = apply(html, COUNTERS, "about counters")
    html = replace_testimonials(html, ABOUT_TESTIMONIAL_SOURCE)
    html = drop_section(html, "Our Team")
    (HERE / "about.html").write_text(html)
    print("built about.html")

    # ---- services --------------------------------------------------------
    html = common((TPL / "services.html").read_text(), "services.html")
    html = inner_hero(html, "Kitchens, dressings, doors, panelling and bathroom furniture. Everything is drawn for your room and built in our own workshop.")
    html = html.replace("<h1 class=\"mb-3 wow fadeInUp\" data-wow-delay=\".2s\">Services</h1>",
                        "<h1 class=\"mb-3 wow fadeInUp\" data-wow-delay=\".2s\">What We Make</h1>")
    # anchors, in the order the cards appear in the markup
    anchors = ["kitchens", "dressings", "doors", "bathroom", "panelling", "commercial"]
    parts = html.split('<div class="item col-lg-4 col-sm-6">')
    if len(parts) == 7:
        html = parts[0] + "".join('<div class="item col-lg-4 col-sm-6" id="%s">%s' % (a, p)
                                  for a, p in zip(anchors, parts[1:]))
    else:
        print("  ! expected 6 service cards, found", len(parts) - 1)
    html = replace_titles(html, SERVICE_TITLES,
                          '<h2 class="fs-40 wow scale-in-mask" data-wow-delay=".6s">{}</h2>')
    (HERE / "services.html").write_text(html)
    print("built services.html")

    # ---- projects --------------------------------------------------------
    html = common((TPL / "projects.html").read_text(), "projects.html")
    html = inner_hero(html, "Private houses, offices and hotels across Mauritius and Rodrigues, built alongside the architects and interior designers who drew them.")
    html = html.replace("<h1 class=\"mb-3 wow fadeInUp\" data-wow-delay=\".2s\">Projects</h1>",
                        "<h1 class=\"mb-3 wow fadeInUp\" data-wow-delay=\".2s\">Selected Work</h1>")
    for old, new in PROJECT_TITLES:
        found = False
        for fmt in ('<h2 class="fs-36">{}</h2>', '<h2 class="fs-40">{}</h2>',
                    '<h2 class="fs-36 wow scale-in-mask" data-wow-delay=".6s">{}</h2>',
                    '<h2 class="fs-40 wow scale-in-mask" data-wow-delay=".6s">{}</h2>'):
            if fmt.format(old) in html:
                html = html.replace(fmt.format(old), fmt.format(new)); found = True
        if not found:
            print("  ! project title not found:", old)
    html = replace_tags(html)
    (HERE / "projects.html").write_text(html)
    print("built projects.html")

    # ---- contact ---------------------------------------------------------
    html = common((TPL / "contact.html").read_text(), "contact.html")
    html = inner_hero(html, "Come and see the work in person. Bring a photograph of the room and a rough measurement, and fifteen minutes in the showroom will tell you more than any brochure.")
    for city, addr, tel, mail, h4, body, _a, _b in CONTACT_OFFICES:
        old = "<h4 class=\"mb-0\">%s</h4>\n                                %s<br>\n                                %s<br>\n                                %s<br>" % (city, addr, tel, mail)
        new = "<h4 class=\"mb-0\">%s</h4>\n                                %s<br>" % (h4, body)
        if old in html:
            html = html.replace(old, new)
        else:
            print("  ! contact block not found:", city)
    html = html.replace("Have a question, suggestion, or just want to say hi? We\u2019re here and happy to hear from you!",
                        "Tell us about the space you want to change. The more you can tell us now, the more useful our first reply will be.")
    (HERE / "contact.html").write_text(html)
    print("built contact.html")


if __name__ == "__main__":
    main()
