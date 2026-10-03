from pathlib import Path
import re

root=Path('/mnt/data/sitework')
index=root/'index.html'
base=index.read_text(encoding='utf-8')

# Build the exact requested expertise dropdown. Duplicate Domestic Violence is intentionally shown once.
items=[
 ('Domestic Violence Lawyers','domestic-violence-lawyers.html'),
 ('Matrimonial Lawyers','matrimonial-lawyers.html'),
 ('Family Disputes Lawyers','family-disputes-lawyers.html'),
 ('Bail Lawyers','bail-lawyers.html'),
 ('Cheque Bounce Lawyers','cheque-bounce-lawyers.html'),
 ('Civil Lawyers','civil-lawyers.html'),
 ('Criminal Lawyers','criminal-lawyers.html'),
 ('Corporate Lawyer','corporate-lawyer.html'),
]

def nav(active=None):
    def li(label,href,cls=''):
        return f'''<li><a href="{href}"{(' class="active"' if active==label else '')}>{label}</a></li>'''
    expert='''<li class="has-dropdown">\n                    <a href="practice.html" aria-haspopup="true">\n                        Our Expertise <i class="fas fa-chevron-down nav-chevron"></i>\n                    </a>\n                    <ul class="dropdown-menu">\n'''
    for label,href in items:
        expert += f'                        <li><a href="{href}">{label}</a></li>\n'
    expert += '                    </ul>\n                </li>'
    return f'''<nav>\n            <ul class="nav-links">\n                {li('Home','index.html')}\n                {li('About','about.html')}\n                <li class="has-dropdown">\n                    <a href="services.html" aria-haspopup="true">\n                        Our Services <i class="fas fa-chevron-down nav-chevron"></i>\n                    </a>\n                    <ul class="dropdown-menu">\n                        <li><a href="services.html">Legal Consultation</a></li>\n                        <li><a href="services.html">Legal Documentation &amp; Drafting</a></li>\n                        <li><a href="services.html">Litigation &amp; Court Representation</a></li>\n                        <li><a href="services.html">Corporate Legal Services</a></li>\n                        <li><a href="services.html">Property &amp; Real Estate</a></li>\n                        <li><a href="services.html">Family &amp; Matrimonial Matters</a></li>\n                        <li><a href="services.html">Criminal Law Assistance</a></li>\n                        <li><a href="services.html">Consumer Disputes</a></li>\n                        <li><a href="services.html">Cyber Law Assistance</a></li>\n                        <li><a href="services.html">Legal Notice &amp; Reply</a></li>\n                    </ul>\n                </li>\n                {expert}\n                {li('Blogs','blog.html')}\n                {li('Contact','contact.html')}\n            </ul>\n        </nav>'''

# Replace nav in every HTML file that already uses this site's navbar.
for p in root.glob('*.html'):
    s=p.read_text(encoding='utf-8')
    m=re.search(r'<nav>\s*<ul class="nav-links">.*?</ul>\s*</nav>',s,re.S)
    if m:
        active = 'Home' if p.name=='index.html' else None
        s=s[:m.start()]+nav(active)+s[m.end():]
        p.write_text(s,encoding='utf-8')

# Ensure the dropdown remains visibly scrollable.
css=root/'css/style.css'
s=css.read_text(encoding='utf-8')
old='''    max-height: 245px;\n    overflow-y: scroll;'''
if old in s:
    s=s.replace(old,'''    max-height: 250px;\n    overflow-y: auto;''')
# Add stronger dropdown scroll styling if not already present.
if '/* Our Expertise dropdown scroll */' not in s:
    s += '''\n\n/* Our Expertise dropdown scroll */\n.dropdown-menu {\n    max-height: 250px;\n    overflow-y: auto;\n    overflow-x: hidden;\n    overscroll-behavior: contain;\n}\n'''
css.write_text(s,encoding='utf-8')

# Individual expertise page content.
pages={
'domestic-violence-lawyers.html':('Domestic Violence Lawyers','Domestic Violence Lawyers in Delhi','Domestic violence matters require careful attention to safety, legal rights, evidence and the applicable legal process. Adv. Nikhil Shakarwal provides confidential legal guidance to individuals dealing with allegations or complaints relating to domestic violence.','Domestic violence legal assistance may include understanding available remedies, preparing applications and replies, representation before the appropriate court or authority, and guidance regarding related family proceedings. Each matter is considered on its facts and the applicable law.',['Protection and domestic violence proceedings','Legal consultation and case assessment','Drafting and review of applications and replies','Court representation and procedural guidance','Related matrimonial and family disputes']),
'matrimonial-lawyers.html':('Matrimonial Lawyers','Matrimonial Lawyers in Delhi','Matrimonial disputes can involve divorce, maintenance, custody, allegations, property issues and other connected proceedings. Adv. Nikhil Shakarwal provides practical and confidential legal guidance tailored to the facts and legal requirements of each matter.','Matrimonial legal assistance may cover the preparation, filing, response and representation required in family and matrimonial proceedings. The focus is on clear advice, careful documentation and professional representation.',['Divorce and matrimonial proceedings','Maintenance and related applications','Matrimonial dispute representation','Family settlements and agreements','Court representation and legal documentation']),
'family-disputes-lawyers.html':('Family Disputes Lawyers','Family Disputes Lawyers in Delhi','Family disputes often involve sensitive personal relationships as well as important legal rights. Adv. Nikhil Shakarwal assists clients with family-law matters through confidential consultation, careful preparation and representation before the appropriate forum.','Depending on the circumstances, family dispute matters can involve maintenance, custody, matrimonial issues, domestic violence proceedings, family settlements and related civil or family cases.',['Family dispute consultation','Maintenance-related matters','Child custody and visitation matters','Family settlements and mediation support','Court representation in family proceedings']),
'bail-lawyers.html':('Bail Lawyers','Bail Lawyers in Delhi','Bail proceedings can require timely preparation, review of the case record and representation before the appropriate court. Adv. Nikhil Shakarwal provides legal assistance in bail-related matters, including regular and anticipatory bail, subject to the facts and applicable law.','Bail matters are assessed individually. Legal assistance may include reviewing the allegations and available documents, preparing the necessary application, responding to objections and representing the client during proceedings.',['Regular bail matters','Anticipatory bail matters','Bail application preparation','Court representation','Procedural legal guidance']),
'cheque-bounce-lawyers.html':('Cheque Bounce Lawyers','Cheque Bounce Lawyers in Delhi','Cheque dishonour matters commonly involve statutory notices, limitation requirements, documentation and proceedings under the applicable law. Adv. Nikhil Shakarwal provides legal guidance for both initiating and responding to cheque-related disputes.','Assistance may include reviewing the transaction and documents, preparing or responding to legal notices, and representation in proceedings connected with cheque dishonour matters.',['Cheque dishonour consultation','Legal notice drafting and reply','Section 138 related proceedings','Document and transaction review','Court representation']),
'civil-lawyers.html':('Civil Lawyers','Civil Lawyers in Delhi','Civil disputes can involve property, contracts, recovery, injunctions, ownership and other private-law issues. Adv. Nikhil Shakarwal provides legal consultation, documentation support and representation in civil matters based on the facts and applicable law.','Civil litigation generally requires careful examination of documents, facts, limitation and the relief sought. Each case is approached with structured preparation and clear communication.',['Civil dispute consultation','Property and ownership disputes','Recovery and money claims','Injunction and declaration matters','Civil court representation']),
'criminal-lawyers.html':('Criminal Lawyers','Criminal Lawyers in Delhi','Criminal matters can have serious legal consequences and require prompt, careful attention to procedure and evidence. Adv. Nikhil Shakarwal provides legal consultation and representation in criminal-law matters, subject to the facts and applicable law.','Assistance may include understanding the allegations, reviewing available documents, preparing applications and representing clients before the appropriate court.',['Criminal-law consultation','Bail and anticipatory bail matters','FIR and criminal-procedure guidance','Trial and court representation','Criminal appeals and related proceedings']),
'corporate-lawyer.html':('Corporate Lawyer','Corporate Lawyer in Delhi','Businesses require clear legal documentation, contracts, compliance support and practical advice when disputes arise. Adv. Nikhil Shakarwal provides legal assistance to businesses and professionals in corporate and commercial matters.','Corporate legal support may include reviewing agreements, advising on business arrangements, assisting with legal documentation and representing clients in commercial disputes where appropriate.',['Business and commercial agreements','Contract review and drafting','Corporate legal consultation','Commercial dispute support','Legal notices and documentation'])
}

# Pull common footer from service page and use the premium service layout as the page shell.
template=(root/'service.html').read_text(encoding='utf-8')
for filename,(title,h2,intro,body,bullets) in pages.items():
    s=template
    # Head metadata/title
    s=re.sub(r'<meta name="description" content=".*?">',f'<meta name="description" content="{title} by Adv. Nikhil Shakarwal.">',s,count=1)
    s=re.sub(r'<title>.*?</title>',f'<title>{title} | Adv. Nikhil Shakarwal</title>',s,count=1)
    # Use a proper hero immediately after <main>
    main_start=s.find('<main>')
    layout_start=s.find('<section class="service-main">')
    if main_start!=-1 and layout_start!=-1:
        s=s[:main_start+len('<main>')]+'''\n    <section class="service-hero">\n        <div class="container"><h1>'''+title+'''</h1></div>\n    </section>\n'''+s[layout_start:]
    # Replace article contents only, preserving the sidebar and CTA.
    a=s.find('<article class="service-content">')
    b=s.find('<!-- SIDEBAR -->',a)
    article='''<article class="service-content">\n                <img class="service-feature-image" src="images/law.jpg" alt="'''+title+'''">\n\n                <h2>'''+h2+'''</h2>\n                <p>'''+intro+'''</p>\n                <p>'''+body+'''</p>\n\n                <h2>Areas We Can Assist With</h2>\n                <ul class="service-list">\n'''+''.join(f'                    <li><strong>{x}</strong> — Legal guidance and representation based on the facts and applicable law.</li>\n' for x in bullets)+'''                </ul>\n\n                <h2>Professional &amp; Confidential Legal Guidance</h2>\n                <p>Every matter is reviewed on its own facts. The focus is on clear communication, careful preparation, confidentiality and appropriate legal representation throughout the process.</p>\n\n                <ul class="service-list check-list">\n                    <li><i class="fas fa-check-circle"></i> Clear and practical legal guidance</li>\n                    <li><i class="fas fa-check-circle"></i> Detailed case and document review</li>\n                    <li><i class="fas fa-check-circle"></i> Transparent communication</li>\n                    <li><i class="fas fa-check-circle"></i> Confidential handling of information</li>\n                    <li><i class="fas fa-check-circle"></i> Professional court and legal representation</li>\n                </ul>\n\n                <div class="service-cta">\n                    <h3>Need Legal Assistance?</h3>\n                    <p>Contact Adv. Nikhil Shakarwal for a consultation regarding your legal matter.</p>\n                    <a href="contact.html" class="btn">Contact Us <i class="fas fa-arrow-right"></i></a>\n                </div>\n            </article>\n\n            '''
    if a!=-1 and b!=-1:
        s=s[:a]+article+s[b:]
    # Update sidebar list links
    sb_start=s.find('<div class="service-side-links">')
    sb_end=s.find('</div>', sb_start)
    if sb_start!=-1:
        # locate closing div by targeted old content
        old_end=s.find('</aside>',sb_start)
        if old_end!=-1:
            side='''<div class="service-side-links">\n                    <h3>Our Expertise</h3>\n'''+''.join(f'                    <a href="{href}"'+(' class="selected"' if href==filename else '')+f'>{label}</a>\n' for label,href in items)+'''                </div>\n            '''
            # replace everything in aside after contact card block by using known marker
            marker=s.find('<div class="service-side-links">',sb_start)
            aside_end=s.find('</aside>',marker)
            if marker!=-1 and aside_end!=-1:
                s=s[:marker]+side+s[aside_end:]
    # Insert the current dropdown nav after shell was built (template has old nav).
    m=re.search(r'<nav>\s*<ul class="nav-links">.*?</ul>\s*</nav>',s,re.S)
    if m:
        s=s[:m.start()]+nav(None)+s[m.end():]
    # Update subject field in sidebar form if present.
    s=s.replace('value="Legal Documentation"','value="'+title+'"')
    (root/filename).write_text(s,encoding='utf-8')

# Also make Practice Areas link in old content point to the first expertise page as a neutral landing page.
(root/'practice.html').write_text((root/'practice.html').read_text(encoding='utf-8').replace('href="practice.html" class="active"','href="practice.html" class="active"'),encoding='utf-8')
print('Created:', ', '.join(pages))
