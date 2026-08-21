# -*- coding: utf-8 -*-
"""Yanımda Evde Sağlık — statik site üreticisi.  Çalıştırma:  python3 _src/build.py"""
import json, os, re, shutil, sys, hashlib, datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from site_data import (SITE as S, BRANCHES, DISTRICTS, EXTRA_AREAS, SEMTLER,
                       SERUM_LOCATIONS, SERVICES, SERUMS, DISCLAIMER)
from flagship import FLAGSHIP
from icons import ICONS
import media as MED
import content as C

YEAR = 2026
V = str(int(os.path.getmtime(os.path.join(OUT, 'assets/css/site.css'))))
WA_TEXT = "Merhaba%2C%20evde%20sa%C4%9Fl%C4%B1k%20hizmeti%20i%C3%A7in%20bilgi%20almak%20istiyorum."
BR = {b["slug"]: b for b in BRANCHES}

# ---------------------------------------------------------------- yardımcılar
TR = str.maketrans("çÇğĞıİöÖşŞüÜâÂîÎûÛ", "cCgGiIoOsSuUaAiIuU")
def slug(t):
    t = t.translate(TR).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)

def h(t):  # istikrarlı sayısal hash (varyasyon seçimi için)
    return int(hashlib.md5(t.encode("utf-8")).hexdigest()[:8], 16)

def pick(pool, key, off=0):
    return pool[(h(key) + off) % len(pool)]

def pick_n(pool, key, n, off=0):
    idx, seen, i = [], set(), 0
    while len(idx) < min(n, len(pool)):
        k = (h(key + str(i)) + off) % len(pool)
        if k not in seen:
            seen.add(k); idx.append(k)
        i += 1
        if i > 400: break
    return [pool[k] for k in idx]

BACK, FRONT = "aıou", "eiöü"
ROUND_ = "ouöü"
VOICELESS = "fstkçşhp"
# ek alırken araya -n- giren özel adlar (3. tekil iyelik ekiyle biten yer adları)
N_BUFFER = {"Beylikdüzü"}
# sayıyla biten adlarda son rakamın okunuşuna göre ek (ör. 2000 -> "iki bin")
DIGIT_END = {"0": ("i", "n"), "1": ("i", "r"), "2": ("i", "i"), "3": ("ü", "ç"), "4": ("ö", "t"),
             "5": ("e", "ş"), "6": ("ı", "ı"), "7": ("i", "i"), "8": ("i", "z"), "9": ("u", "z")}

def _tail(name):
    """(son ünlü, son harf) — rakamla biten adlarda okunuşa göre."""
    t = name.rstrip()
    if t and t[-1].isdigit():
        return DIGIT_END[t[-1]]
    v, l = "a", "a"
    for ch in reversed(t.lower()):
        if ch in BACK or ch in FRONT:
            v = ch; break
    for ch in reversed(t):
        if ch.isalpha():
            l = ch.lower(); break
    return v, l

def apo(name):
    """'-de / -da / -te / -ta' bulunma eki (ünlü uyumu + ünsüz benzeşmesi)."""
    v, last = _tail(name)
    e = "d" if last not in VOICELESS else "t"
    suf = e + ("a" if v in BACK else "e")
    if name in N_BUFFER:
        suf = "n" + suf
    return f"{name}'{suf}"

def apo_nin(name):
    """'-in / -ın / -un / -ün' ilgi eki."""
    v, last = _tail(name)
    if v in BACK:
        m = "un" if v in ROUND_ else "ın"
    else:
        m = "ün" if v in ROUND_ else "in"
    vowel_end = last in BACK + FRONT
    return f"{name}'n{m}" if (vowel_end or name in N_BUFFER) else f"{name}'{m}"

# ---------------------------------------------------------------- veri kurulumu
raw = json.load(open(os.path.join(HERE, "data/turkiye_ilce_mahalle.json"), encoding="utf-8"))
IST = raw["İSTANBUL"]["ilceler"]

for d in DISTRICTS:
    d["mahalleler"] = IST[d["name"]]
    d["mahalle_count"] = len(d["mahalleler"])

# aynı isimli mahalleler (ilçe ekiyle ayrıştırılır)
name_count = {}
for d in DISTRICTS:
    for mh in d["mahalleler"]:
        name_count[mh] = name_count.get(mh, 0) + 1

LOCS = {}   # slug_base -> location kaydı
def add_loc(name, district, district_slug, branch, kind, covers=None, flag=None, need_suffix=False):
    base = slug(name) + ("-" + slug(district) if need_suffix else "")
    if base in LOCS:                      # ilçe adıyla aynı olan mahalle (ör. Başakşehir)
        base = slug(name) + "-mahallesi"
        need_suffix = True
    LOCS[base] = dict(name=name, district=district, district_slug=district_slug, branch=branch,
                      kind=kind, covers=covers or [], flag=flag, base=base, dup=need_suffix)
    return base

MAH_BASE = {}
def mah_base(mh, dist):
    return MAH_BASE.get((mh, dist), slug(mh))

for d in DISTRICTS:
    add_loc(d["name"], d["name"], d["slug"], d["branch"], "ilce",
            covers=d["mahalleler"][:6])
for d in DISTRICTS:
    for mh in d["mahalleler"]:
        fk = slug(mh)
        b = add_loc(mh, d["name"], d["slug"], d["branch"], "mahalle",
                    flag=FLAGSHIP.get(fk) if FLAGSHIP.get(fk, {}).get("district") == d["name"] else None,
                    need_suffix=name_count[mh] > 1)
        MAH_BASE[(mh, d["name"])] = b
for sm in SEMTLER:
    fk = slug(sm["name"])
    if fk in LOCS: continue
    dd = next((x for x in DISTRICTS if x["name"] == sm["district"]), None)
    add_loc(sm["name"], sm["district"], dd["slug"] if dd else None,
            dd["branch"] if dd else "bahcesehir", "semt", flag=FLAGSHIP.get(fk))
# hizmet bölgesinde olup ilçesi kapsam dışı kalan büyük semtler
for fk, fv in FLAGSHIP.items():
    if fk not in LOCS:
        add_loc(fv["name"], fv["district"], fv.get("district_slug"), fv["branch"], "semt", flag=fv)
    else:
        LOCS[fk]["flag"] = LOCS[fk]["flag"] or fv

SERUM_SET = {slug(x) for x in SERUM_LOCATIONS} | {k for k, v in FLAGSHIP.items() if v.get("serum_page")}

def loc_url(base, mode="saglik"):
    return f"{base}-evde-{'serum' if mode == 'serum' else 'saglik'}/"

FLAG_TOP = [dict(name=v["name"], slug=loc_url(k).rstrip('/')) for k, v in list(FLAGSHIP.items())[:8]]
FLAG_SERUM = [dict(name=v["name"], slug=loc_url(k, 'serum').rstrip('/'))
              for k, v in FLAGSHIP.items() if v.get("serum_page")]

# ---------------------------------------------------------------- jinja
env = Environment(loader=FileSystemLoader(os.path.join(HERE, "templates")),
                  autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)

NAV = dict(services=SERVICES, serums=SERUMS, districts=DISTRICTS,
           footer_areas=[dict(slug=loc_url(d["slug"]).rstrip('/'), label=f'{d["name"]} Evde Sağlık') for d in DISTRICTS] +
                        [dict(slug=loc_url(k).rstrip('/'), label=f'{v["name"]} Evde Sağlık') for k, v in FLAGSHIP.items()])

BASE = dict(S=S, I=ICONS, NAV=NAV, YEAR=YEAR, V=V, WA_TEXT=WA_TEXT, DISCLAIMER=DISCLAIMER,
            SRV=SERVICES, SER=SERUMS, DIST=DISTRICTS, BR=BRANCHES,
            FLAG_TOP=FLAG_TOP, FLAG_SERUM=FLAG_SERUM, MED=MED)

PAGES = []   # (path, priority, changefreq)

def write(path, tpl, prio=0.6, cf="monthly", **ctx):
    outdir = os.path.join(OUT, path)
    os.makedirs(outdir, exist_ok=True)
    depth = len([x for x in path.split("/") if x])
    ctx.setdefault("root", "../" * depth if depth else "")
    ctx.setdefault("canonical", S["domain"] + "/" + (path + "/" if path else ""))
    ctx["jsonld"] = [x for x in (ctx.get("jsonld") or []) if x]
    if ctx.get("crumbs"):
        ctx["jsonld"] = [j for j in ctx["jsonld"] if '"BreadcrumbList"' not in j]
        ctx["jsonld"].append(ld_bc(ctx["crumbs"], path))
    full = dict(BASE); full.update(ctx)
    html = env.get_template(tpl).render(**full)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    PAGES.append((ctx["canonical"], prio, cf))

def ld(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def ld_faq(items):
    return ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]})

def ld_bc(items, page_path=""):
    import posixpath
    base = "/" + (page_path + "/" if page_path else "")
    el = [{"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": S["domain"] + "/"}]
    for i, (label, url) in enumerate(items, start=2):
        e = {"@type": "ListItem", "position": i, "name": label}
        if url:
            abs_p = posixpath.normpath(posixpath.join(base, url))
            if not abs_p.endswith("/"): abs_p += "/"
            e["item"] = S["domain"] + abs_p
        el.append(e)
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el})

def ld_biz(area=None, url=None, name=None):
    return ld({
        "@context": "https://schema.org", "@type": "MedicalBusiness",
        "@id": S["domain"] + "/#kurulus",
        "name": name or S["name"], "url": url or (S["domain"] + "/"),
        "telephone": S["phone_tel"], "image": S["domain"] + "/assets/img/hero-1440.webp",
        "priceRange": "₺₺", "foundingDate": "2020",
        "medicalSpecialty": "https://schema.org/Nursing",
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "00:00", "closes": "23:59"}],
        "address": {"@type": "PostalAddress", "addressLocality": "İstanbul", "addressRegion": "İstanbul", "addressCountry": "TR"},
        "areaServed": [{"@type": "AdministrativeArea", "name": a} for a in (area or
                       [d["name"] for d in DISTRICTS] + EXTRA_AREAS)],
        "sameAs": [S["instagram"]],
        "contactPoint": {"@type": "ContactPoint", "telephone": S["phone_tel"], "contactType": "customer service",
                         "areaServed": "TR", "availableLanguage": "Turkish"},
    })

# ---------------------------------------------------------------- metin doldurma
def fmt(t, L):
    return (t.replace("{nd}", apo(L["name"])).replace("{nn}", apo_nin(L["name"]))
             .replace("{dd}", apo(L["district"])).replace("{n}", L["name"])
             .replace("{d}", L["district"]).replace("{b}", BR[L["branch"]]["title"]))

def build_location(base, L, mode):
    key = base + mode
    name, dist = L["name"], L["district"]
    flag = L["flag"]
    is_serum = mode == "serum"
    kw = "Evde Serum" if is_serum else "Evde Sağlık"
    disp = f"{name} Mahallesi ({dist})" if L.get("dup") else name
    h1 = f"{disp} {kw} Hizmeti" + (" — 7/24" if L["kind"] == "ilce" else "")

    # --- gövde blokları
    blocks = []
    if flag:
        blocks.append((fmt(pick(C.H1_INTRO, key), L),
                       fmt_list(pick(C.SERUM_INTRO if is_serum else C.INTRO, key), L)))
        blocks.append((flag["context_title"], flag["context"]))
        blocks.append((fmt(pick(C.H2_WHY, key, 2), L), fmt_list(pick(C.WHY, key, 1), L)))
        lead = flag["lead"]
        faq = [(fmt(q, L), fmt(a, L)) for q, a in flag["faq"]]
        covers = flag.get("covers", [])
        extra = flag.get("extra")
    elif L["kind"] == "ilce":
        d = next(x for x in DISTRICTS if x["name"] == dist)
        mah = d["mahalleler"]
        lead = (f"{apo(dist)} {len(mah)} mahallenin tamamına evde sağlık hizmeti veriyoruz. "
                f"Serum, enjeksiyon, pansuman ve sonda uygulamaları için hemşire ekibimiz {apo(dist)} bulunan adrese geliyor — "
                f"gece, hafta sonu ve resmî tatil dahil.") if not is_serum else (
                f"{apo(dist)} evde serum hizmeti: hekim isteminde yazan sıvı ve ilaçlar, ilçenin {len(mah)} mahallesinin "
                f"tamamında evinizde damar yolundan uygulanır. Uygulama boyunca hemşire evde kalır.")
        blocks.append((f"{apo(dist)} evde sağlık hizmeti nasıl işliyor?", [
            f"{dist}, hizmet alanımızın merkez ilçelerinden biri. İlçedeki {len(mah)} mahallenin hepsine gidiyoruz; "
            f"{', '.join(mah[:5])} ve diğerleri için ayrı ayrı bilgi sayfası hazırladık.",
            f"Çağrılar {BR[L['branch']]['title']} konumumuzdaki ekip tarafından karşılanıyor. Telefonda şikâyetinizi, "
            f"yaşınızı, kronik hastalıklarınızı ve kullandığınız ilaçları soruyoruz; hekim isteminiz varsa doğrudan "
            f"uygulamaya geçiyoruz."]))
        blocks.append((f"{apo(dist)} en sık hangi durumlar için çağrılıyoruz?", fmt_list(pick(C.CASES, key), L)))
        blocks.append((fmt(pick(C.H2_WHY, key, 1), L), fmt_list(pick(C.WHY, key), L)))
        faq = [(fmt(q, L), fmt(a, L)) for q, a in pick_n(C.FAQ_POOL, key, 6)]
        covers = mah[:8]
        extra = None
    else:
        pool_i = C.SERUM_INTRO if is_serum else C.INTRO
        pool_c = C.SERUM_CASES if is_serum else C.CASES
        blocks.append((fmt(pick(C.H1_INTRO, key), L), fmt_list(pick(pool_i, key), L)))
        blocks.append((fmt(pick(C.H2_CASES, key), L), fmt_list(pick(pool_c, key), L)))
        blocks.append((fmt(pick(C.H2_WHY, key), L), fmt_list(pick(C.WHY, key), L)))
        lead = blocks[0][1][0]
        blocks[0] = (blocks[0][0], blocks[0][1][1:] or blocks[0][1])
        faq = [(fmt(q, L), fmt(a, L)) for q, a in pick_n(C.FAQ_POOL, key, 5)]
        covers = []
        extra = None

    # --- iç linkler
    child_links, child_title, child_lead, sibling, aside_links, aside_title = [], "", "", [], [], ""
    if L["kind"] == "ilce":
        d = next(x for x in DISTRICTS if x["name"] == dist)
        child_title = f"{apo(dist)} hizmet verdiğimiz mahalleler"
        child_lead = f"Aşağıdaki mahallelerin her biri için ayrı bir sayfa hazırladık — mahallenizin sayfasında o bölgeye özel bilgileri bulabilirsiniz."
        for mh in d["mahalleler"]:
            b2 = mah_base(mh, dist)
            if b2 in LOCS:
                child_links.append(dict(slug=loc_url(b2).rstrip("/"), label=f"{mh} evde sağlık"))
        aside_title = "Diğer ilçeler"
        aside_links = [dict(slug=loc_url(x["slug"]).rstrip("/"), label=f'{x["name"]} evde sağlık')
                       for x in DISTRICTS if x["name"] != dist]
        sibling = [dict(slug=loc_url(k).rstrip("/"), label=f'{v["name"]} evde sağlık') for k, v in FLAGSHIP.items()][:8]
    else:
        d = next((x for x in DISTRICTS if x["name"] == dist), None)
        if d:
            others = [m2 for m2 in d["mahalleler"] if m2 != name]
            picked = pick_n(others, key, 12) if others else []
            for mh in picked:
                b2 = mah_base(mh, dist)
                if b2 in LOCS and b2 != base:
                    sibling.append(dict(slug=loc_url(b2).rstrip("/"), label=f"{mh} evde sağlık"))
            aside_title = f"{dist} mahalleleri"
            aside_links = sibling[:8]
            child_title = f"{apo(dist)} diğer bölgeler"
        if is_serum:
            sibling = sibling[:8] + [dict(slug=loc_url(base).rstrip("/"), label=f"{name} evde sağlık")]
        else:
            if base in SERUM_SET:
                sibling = [dict(slug=loc_url(base, 'serum').rstrip("/"), label=f"{name} evde serum")] + sibling[:8]
    if d and L["kind"] != "ilce":
        aside_links = (aside_links or [])[:8]
        sibling = sibling[:12]

    ser_local = pick_n(SERUMS, key, 15)
    Lc = dict(L)
    Lc.update(name=name, nd=apo(name), nn=apo_nin(name), kicker=("Evde Serum Hizmeti" if is_serum else "Evde Sağlık Hizmeti") + f" · {dist}",
              lead=lead, blocks=blocks, faq=faq, covers=covers, extra=extra,
              branch_title=BR[L["branch"]]["title"], branch_pb=BR[L["branch"]]["pb"],
              child_links=child_links if L["kind"] == "ilce" else [], child_title=child_title, child_lead=child_lead,
              sibling_links=sibling, aside_links=aside_links, aside_title=aside_title,
              cta_h=f"{name} için şimdi arayın",
              cta_t=f"{apo(name)} 7/24 çağrı alıyoruz. Telefonda durumunuzu dinler, hekim istemi gerekip gerekmediğini söyler ve gerçekçi bir varış saati veririz.")

    crumbs = [("Hizmet Bölgeleri", "../hizmet-bolgeleri/")]
    if L["kind"] != "ilce" and L["district_slug"]:
        crumbs.append((dist, f'../{L["district_slug"]}-evde-saglik/'))
    crumbs.append((h1, None))

    desc = (f"{disp} evde serum hizmeti — hekim istemiyle damar yolundan uygulama, 7/24. {dist} bölgesinde "
            f"bulantı, ishal, ateş ve grip serumu için hemşire ekibimiz evinize gelir. {S['phone_display']}"
            if is_serum else
            f"{disp} evde sağlık hizmeti: serum, enjeksiyon, pansuman ve sonda uygulamaları için hemşire ekibimiz "
            f"{apo(name)} adresinize gelir. 7/24 — {dist}, İstanbul. {S['phone_display']}")[:300]

    path = loc_url(base, mode).rstrip("/")
    prio = 0.9 if L["kind"] == "ilce" else (0.8 if flag else 0.65)
    pool = MED.SERUM_POOL if is_serum else MED.ROTATE
    i1 = img(pick(pool, key), "(max-width:1024px) 92vw, 700px")
    i2 = img(pick(MED.ROTATE, key, 3), "(max-width:1024px) 92vw, 700px") if L["kind"] != "mahalle" or flag else None
    if i2 and i1 and i2["key"] == i1["key"]:
        i2 = img(pick(MED.ROTATE, key, 5), "(max-width:1024px) 92vw, 700px")
    write(path, "location.html", prio, "weekly",
          title=f"{h1} | {S['name']}", description=desc, h1=h1, L=Lc, crumbs=crumbs,
          SER_LOCAL=ser_local, og_img="default", IMG=i1, IMG2=i2,
          jsonld=[ld_biz(area=[name, dist, "İstanbul"], url=S["domain"] + "/" + path + "/",
                         name=f"{S['name']} — {name}"),
                  ld_faq(faq)])

def fmt_list(lst, L):
    return [fmt(x, L) for x in lst]

# ---------------------------------------------------------------- sayfa üretimi
def build_all():
    # --- konum sayfaları
    for base, L in LOCS.items():
        build_location(base, L, "saglik")
        if L["kind"] == "ilce" or base in SERUM_SET:
            build_location(base, L, "serum")

    # --- hizmet sayfaları
    for i, sv in enumerate(SERVICES):
        others = SERVICES[i+1:] + SERVICES[:i]
        crumbs = [("Hizmetler", "../"), (sv["title"], None)]
        write(f"hizmetler/{sv['slug']}", "service.html", 0.9, "monthly",
              title=f"{sv['title']} | İstanbul Avrupa Yakası 7/24 | {S['name']}",
              description=f"{sv['title']} — {sv['short']} Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'de 7/24 evde uygulama. {S['phone_display']}",
              SV=sv, OTHERS=others[:4], crumbs=crumbs,
              IMG=img(MED.SERVICE_IMG.get(sv["slug"]), "(max-width:1024px) 92vw, 700px"),
              jsonld=[ld({"@context":"https://schema.org","@type":"Service","name":sv["title"],
                          "serviceType":sv["kw"],"description":sv["lead"],
                          "provider":{"@type":"MedicalBusiness","name":S["name"],"telephone":S["phone_tel"],
                                      "url":S["domain"]+"/"},
                          "areaServed":[{"@type":"AdministrativeArea","name":x["name"]} for x in DISTRICTS],
                          "availableChannel":{"@type":"ServiceChannel","servicePhone":
                              {"@type":"ContactPoint","telephone":S["phone_tel"]}}}),
                      ld_faq(sv["faq"])])

    # --- serum sayfaları
    for i, sm in enumerate(SERUMS):
        others = SERUMS[i+1:] + SERUMS[:i]
        crumbs = [("Serum Tedavileri", "../"), (sm["title"], None)]
        faq = [
            (f"{sm['title']} evde uygulanabilir mi?",
             "Evet. Hekim isteminde yazması hâlinde uygulama evinizde yapılır; serum bitene kadar hemşire yanınızda kalır."),
            ("Reçete olmadan yapılır mı?",
             "Hayır. Serum ve içine eklenen ilaçlar hekim istemi olmadan uygulanmaz. Hekim değerlendirmeniz yoksa önce muayene için yönlendirme yaparız."),
            ("Ne kadar sürer?",
             "İçeriğine ve akış hızına göre genellikle 30-90 dakika arasında değişir."),
            ("Hangi bölgelerde uygulanıyor?",
             "Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'in tüm mahallelerinde; ayrıca Hadımköy ve Boğazköy yönünde."),
            ("Gece de geliyor musunuz?",
             "Evet, 7/24 çalışıyoruz — gece, hafta sonu ve resmî tatiller dahil."),
        ]
        write(f"serum-tedavileri/{sm['slug']}", "serum.html", 0.9, "monthly",
              title=f"{sm['title']} | Evde Uygulama 7/24 | {S['name']}",
              description=f"{sm['title']}: ne zaman gerekir, içeriğinde neler olabilir, nelere dikkat edilir. İstanbul Avrupa Yakası'nda 7/24 evde uygulama. {S['phone_display']}",
              SM=sm, OTHERS=others, crumbs=crumbs, FAQ=faq,
              IMG=img(pick(MED.SERUM_POOL, sm["slug"]), "(max-width:1024px) 92vw, 700px"),
              jsonld=[ld({"@context":"https://schema.org","@type":"MedicalWebPage",
                          "name":sm["title"],"description":sm["lead"],
                          "about":{"@type":"MedicalTherapy","name":sm["title"]},
                          "audience":{"@type":"Patient"},
                          "lastReviewed":"2026-08-21",
                          "publisher":{"@type":"MedicalBusiness","name":S["name"],"url":S["domain"]+"/"}}),
                      ld_faq(faq)])

    # --- hizmetler hub
    crumbs = [("Hizmetler", None)]
    write("hizmetler", "hub.html", 0.9, "monthly",
          title=f"Evde Sağlık Hizmetleri | Serum, Enjeksiyon, Pansuman, Sonda | {S['name']}",
          description="Evde serum, enjeksiyon, pansuman, idrar sondası ve nazogastrik sonda hizmetleri. İstanbul Avrupa Yakası'nda 7/24 hemşire hizmeti. " + S["phone_display"],
          kicker="Hizmetlerimiz", h1="Evde Sağlık Hizmetleri",
          lead="Hastanede yapılabilen ama hastane gerektirmeyen uygulamaları evinizde tamamlıyoruz. Hepsi hekim istemi doğrultusunda, steril şartlarda ve tıbbi atık geri alınarak yapılır.",
          grid="ye-g4", crumbs=crumbs, IMG=img(MED.HUB_SERVICE), IMG2=img("evde-saglikci"),
          cards=[dict(url=f"hizmetler/{x['slug']}/".replace("hizmetler/", ""), title=x["title"], text=x["short"], icon=x["icon"]) for x in SERVICES],
          body="<h2>Hangi hizmeti seçmeliyim?</h2><p>Emin değilseniz aramanız yeterli. Telefonda şikâyetinizi dinler, elinizdeki hekim istemine bakar ve hangi uygulamanın gerektiğini söyleriz. Hekim değerlendirmesi olmayan durumlarda önce muayene için yönlendirme yaparız.</p>"
               "<h2>Nerelere geliyoruz?</h2><p>Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'in <strong>tüm mahallelerine</strong>; ayrıca Hadımköy, Boğazköy, Silivri ve Çatalca yönüne. <a href=\"../hizmet-bolgeleri/\">Hizmet bölgeleri sayfasından</a> mahallenizi bulabilirsiniz.</p>",
          cta_h="Hangi hizmete ihtiyacınız olduğundan emin değil misiniz?",
          cta_t="Arayın, telefonda konuşalım. Gerekiyorsa hekime yönlendirir, gerekmiyorsa doğrudan ekibi yola çıkarırız.",
          jsonld=[])

    # --- serum hub
    crumbs = [("Serum Tedavileri", None)]
    sfaq = [("Evde serum takmak güvenli mi?","Hekim istemi doğrultusunda, deneyimli bir hemşire tarafından ve uygulama boyunca gözlem yapılarak uygulandığında evde serum güvenli bir işlemdir. Serum takılıp gidilmez; hemşire uygulama bitene kadar evde kalır."),
            ("Serumun içine ne konacağına kim karar verir?","Hekiminiz. Ekibimiz hekim isteminde yazandan farklı bir ilaç eklemez, doz değiştirmez."),
            ("Reçetem yok, yine de gelir misiniz?","Damar içi uygulama için hekim istemi şarttır. Reçeteniz yoksa nasıl ilerlemeniz gerektiğini telefonda anlatırız."),
            ("Serum kaç dakika sürer?","İçeriğine ve akış hızına göre çoğunlukla 30-90 dakika."),
            ("Damar yolu bulunamazsa ne oluyor?","Deneyimli hemşirelerimiz farklı bölgeleri değerlendirir. Uygun damar yolu bulunamazsa işlem zorlanmaz, sağlık kuruluşuna yönlendirme yapılır.")]
    write("serum-tedavileri", "hub.html", 0.9, "monthly",
          title=f"Evde Serum Tedavileri | Hangi Şikâyet İçin Hangi Serum? | {S['name']}",
          description="Bulantı, ishal, ateş, grip, migren, alerji ve daha fazlası için evde serum uygulaması. Belirtiler, içerik ve dikkat edilecekler. 7/24 — " + S["phone_display"],
          kicker="Serum Tedavileri", h1="Evde Serum Tedavileri",
          lead="Aşağıdaki başlıkların her biri için ayrı bir bilgi sayfası hazırladık: hangi durumda gündeme gelir, içeriğinde neler olabilir, uygulama nasıl ilerler ve nelere dikkat edilmelidir.",
          grid="ye-g3", crumbs=crumbs, IMG=img(MED.HUB_SERUM), IMG2=img("evde-serum-yaptir"),
          cards=[dict(url=f"{x['slug']}/", title=x["title"], text=x["lead"][:118] + "…", icon="drop") for x in SERUMS],
          intro="<div class=\"ye-box ye-box-r\"><h3>Önce şunu söyleyelim</h3><p style=\"margin:0\">Hangi serumun uygulanacağına ve içine hangi ilaçların ekleneceğine <strong>hekim</strong> karar verir. Bu sayfalar tanı koymak için değil, ne olduğunu anlamanız için hazırlandı. Ekibimiz hekim istemi olmadan damar içi uygulama yapmaz.</p></div>",
          faq=sfaq,
          cta_h="Hangi serumun gerektiğini bilmiyorsanız", cta_t="Arayın. Şikâyetinizi dinler, hekim istemi gerekip gerekmediğini söyler ve doğru adımı beraber belirleriz.",
          jsonld=[ld_faq(sfaq)])

    # --- hizmet bölgeleri hub
    groups = []
    for d in DISTRICTS:
        links = []
        for mh in d["mahalleler"]:
            b2 = mah_base(mh, d["name"])
            if b2 in LOCS:
                links.append(dict(slug=loc_url(b2).rstrip("/"), label=mh))
        groups.append(dict(title=f'{d["name"]} Evde Sağlık', url=f'../{d["slug"]}-evde-saglik/',
                           sub=f'{len(links)} mahalle · {BR[d["branch"]]["title"]} ekibi', links=links))
    semt_links = [dict(slug=loc_url(k).rstrip("/"), label=v["name"]) for k, v in FLAGSHIP.items()]
    groups.insert(0, dict(title="Öne çıkan semtler", url="../hizmet-bolgeleri/",
                          sub="Bahçeşehir, Hadımköy, Esenkent, Kıraç ve diğerleri — bölgeye özel sayfalar",
                          links=semt_links))
    crumbs = [("Hizmet Bölgeleri", None)]
    write("hizmet-bolgeleri", "hub.html", 0.9, "weekly",
          title=f"Hizmet Bölgeleri | İstanbul Avrupa Yakası Evde Sağlık | {S['name']}",
          description="Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'in tüm mahallelerinde evde sağlık ve serum hizmeti. Mahallenizi seçin. " + S["phone_display"],
          kicker="Hizmet Bölgeleri", h1="Hangi bölgelere geliyoruz?",
          lead="Beş ilçenin tüm mahallelerine gidiyoruz. Ayrıca Hadımköy, Boğazköy, Silivri ve Çatalca yönündeki adresler için de arayabilirsiniz.",
          crumbs=crumbs, groups=groups, IMG=img(MED.HUB_AREA), IMG2=img("7-24-evde-saglik"),
          body="<h2>Bölgede üç ayrı konumumuz var</h2><p>Beylikdüzü, Esenyurt ve Bahçeşehir'deki konumlarımız sayesinde Avrupa Yakası'nın batı hattındaki çağrılara aynı anda yanıt verebiliyoruz. Adresinize hangi ekibin geleceğini telefonda söylüyoruz.</p><p>Listede mahallenizi göremiyorsanız yine de arayın — hizmet alanımızın sınırında olan adresler için teyit ediyoruz.</p>",
          cta_h="Mahallenizi listede bulamadınız mı?", cta_t="Arayın, adresinizi teyit edelim. Hizmet alanımızın sınırındaki bölgelere de gidiyoruz.",
          jsonld=[ld_biz()])

    # --- bilgi merkezi
    from posts import POSTS
    crumbs = [("Bilgi Merkezi", None)]
    write("blog", "hub.html", 0.8, "weekly",
          title=f"Bilgi Merkezi | Evde Sağlık Rehberleri | {S['name']}",
          description="Evde serum, pansuman, sonda bakımı, ateş takibi ve sıvı kaybı üzerine hasta yakınları için hazırlanmış pratik rehberler.",
          kicker="Bilgi Merkezi", h1="Evde bakım rehberleri",
          lead="Telefonda en sık aldığımız soruların uzun cevapları. Hepsi hasta yakınının evde uygulayabileceği bilgiler üzerine kurulu.",
          grid="ye-g3", crumbs=crumbs, IMG=img("evde-saglikci-numarasi"),
          cards=[dict(url=f"{p['slug']}/", title=p["title"], text=p["excerpt"], icon=None) for p in POSTS],
          cta_h="Yazıda cevabını bulamadığınız bir şey mi var?", cta_t="Arayın. Telefonda durumunuza özel konuşmak, genel bilgiden her zaman daha yararlıdır.",
          jsonld=[])

    for i, p in enumerate(POSTS):
        others = POSTS[i+1:] + POSTS[:i]
        crumbs = [("Bilgi Merkezi", "../"), (p["title"], None)]
        write(f"blog/{p['slug']}", "article.html", 0.7, "monthly",
              title=f"{p['title']} | {S['name']}", description=p["excerpt"][:300],
              og_type="article", P=p, OTHERS=others, crumbs=crumbs,
              IMG=img(pick(MED.ROTATE, p["slug"]), "(max-width:1024px) 92vw, 700px"),
              jsonld=[ld({"@context":"https://schema.org","@type":"Article","headline":p["title"],
                          "description":p["excerpt"],"datePublished":p["date"],"dateModified":p["date"],
                          "inLanguage":"tr-TR",
                          "author":{"@type":"Organization","name":S["name"]},
                          "publisher":{"@type":"Organization","name":S["name"],
                                       "logo":{"@type":"ImageObject","url":S["domain"]+"/assets/img/logo.png"}},
                          "mainEntityOfPage":{"@type":"WebPage","@id":S["domain"]+f"/blog/{p['slug']}/"}}),
                      ld_faq(p["faq"]) if p.get("faq") else None])

    # --- kurumsal sayfalar
    write("hakkimizda", "page.html", 0.7, "yearly",
          title=f"Hakkımızda | {S['name']}",
          description="Yanımda Evde Sağlık; Beylikdüzü, Esenyurt ve Bahçeşehir'deki üç konumuyla İstanbul Avrupa Yakası'nda 7/24 evde hemşire hizmeti veriyor.",
          kicker="Hakkımızda", h1="Yanımda Evde Sağlık", crumbs=[("Hakkımızda", None)],
          IMG=img(MED.PAGE_HAKKIMIZDA),
          lead="Yanımda Evde Sağlık ekibi uzman kadrosuyla 6 yıldır hizmet vermektedir. Evde sağlık ihtiyaçlarınız için verilen konuma uzman ekibimiz gelir, hasta ile özel olarak ilgilenir.",
          body="""
<p>Hastanede yapılabilen ama hastane gerektirmeyen uygulamaları, hastanın kendi evinde ve doğru koşullarda tamamlıyoruz.</p>
<h2>Ne yapıyoruz?</h2>
<p>Evde serum uygulaması, kas içi ve cilt altı enjeksiyon, yara pansumanı, idrar sondası takma-değiştirme, nazogastrik sonda uygulaması ve hekim istemine bağlı vitamin takviyeleri. Hepsi hemşire ekibimiz tarafından, hastanın evinde yapılıyor.</p>
<h2>Nerede çalışıyoruz?</h2>
<p>Beylikdüzü, Esenyurt ve Bahçeşehir'de olmak üzere üç ayrı konumumuz var. Bu sayede Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'in tüm mahallelerine; ayrıca Hadımköy, Boğazköy, Silivri ve Çatalca yönüne çağrı karşılayabiliyoruz.</p>
<h2>Nasıl çalışıyoruz?</h2>
<ul class="ye-check">
<li><strong>7/24.</strong> Gece, hafta sonu ve resmî tatil ayrımı yapmıyoruz.</li>
<li><strong>Hekim istemi olmadan damar içi uygulama yapmıyoruz.</strong> Bu, size hayır demek anlamına gelse bile değişmiyor.</li>
<li><strong>Serum takıp gitmiyoruz.</strong> Uygulama bitene kadar hemşire evde kalıyor.</li>
<li><strong>Tıbbi atığı geride bırakmıyoruz.</strong> Kullanılan tüm kesici-delici malzeme ekiple geri götürülüyor.</li>
<li><strong>Gerçekçi süre söylüyoruz.</strong> Olmayacak varış saati vaat etmiyoruz.</li>
</ul>
<h2>Neyi yapmıyoruz?</h2>
<p>Acil müdahale kuruluşu değiliz. Göğüs ağrısı, nefes darlığı, bilinç kaybı, felç belirtisi ve ağır travma gibi durumlarda yapılacak tek şey <strong>112'yi aramaktır</strong>. Bu tabloların hiçbiri evde serumla çözülmez ve biz de böyle bir vaatte bulunmuyoruz.</p>
<h2>İletişim</h2>
<p>Bize <a href="tel:+905518448295">0551 844 82 95</a> numarasından 7/24 ulaşabilir, <a href="https://wa.me/905518448295" rel="noopener">WhatsApp</a> üzerinden yazabilir veya <a href="https://www.instagram.com/evdesaglikyanimda" rel="noopener nofollow" target="_blank">Instagram hesabımızı</a> takip edebilirsiniz.</p>
""",
          cta_h="Bir sorunuz mu var?", cta_t="Telefonda konuşmak en hızlısı. 7/24 çağrı alıyoruz.",
          jsonld=[ld_biz()])

    ifaq = [("Hangi saatlerde arayabilirim?","7/24. Gece, hafta sonu ve resmî tatiller dahil aynı numara açık."),
            ("Hangi bölgelere geliyorsunuz?","Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'in tüm mahalleleri; ayrıca Hadımköy, Boğazköy, Silivri ve Çatalca yönü."),
            ("WhatsApp'tan yazabilir miyim?","Evet. Konum paylaşımı ve reçete fotoğrafı için çoğu zaman daha pratik."),
            ("Ne kadar sürede gelirsiniz?","Adrese ve o anki ekip yoğunluğuna göre değişir; aradığınızda gerçekçi bir süre söyleriz.")]
    write("iletisim", "hub.html", 0.8, "yearly",
          title=f"İletişim | 7/24 Evde Sağlık Çağrı Hattı | {S['name']}",
          description=f"Yanımda Evde Sağlık iletişim: {S['phone_display']} — 7/24 çağrı hattı. Beylikdüzü, Esenyurt ve Bahçeşehir konumları.",
          kicker="İletişim", h1="Bize ulaşın", crumbs=[("İletişim", None)],
          lead=f"7/24 açığız. En hızlı yol telefon: {S['phone_display']}. WhatsApp'tan yazarak konum ve reçete fotoğrafı da gönderebilirsiniz.",
          body=f"""
<h2>Çağrı hattı</h2>
<p><a class="ye-btn ye-btn-p" href="tel:{S['phone_tel']}">{ICONS['phone']} {S['phone_display']}</a>
<a class="ye-btn ye-btn-wa" style="margin-left:8px" href="https://wa.me/{S['wa']}?text={WA_TEXT}" rel="noopener">{ICONS['wa']} WhatsApp</a></p>
<h2>Ararken hazır bulundurun</h2>
<ul class="ye-check">
<li>Şikâyet ve ne zamandır sürdüğü</li>
<li>Hastanın yaşı ve kronik hastalıkları</li>
<li>Kullandığı ilaçlar</li>
<li>Varsa hekim istemi / reçete (fotoğrafı yeterli)</li>
<li>Açık adres — site ve blok adı dahil</li>
</ul>
<h2>Sosyal medya</h2>
<p><a href="{S['instagram']}" rel="noopener nofollow" target="_blank">Instagram: @evdesaglikyanimda</a></p>
<h2>Konumlarımız</h2>
<div class="ye-maps">{''.join(f'<div class="ye-map"><div class="ye-map-t">{ICONS["pin"]} {b["title"]}</div><div data-map="https://www.google.com/maps/embed?pb={b["pb"]}" data-title="{b["title"]} konumu" style="min-height:250px"></div></div>' for b in BRANCHES)}</div>
""",
          IMG=img(MED.PAGE_ILETISIM), faq=ifaq, cta_h="Şimdi mi gerekiyor?", cta_t="Arayın; telefonda durumunuzu dinler, ne gerektiğini söyleriz.",
          jsonld=[ld_biz(), ld_faq(ifaq)])

    gfaq = ([(q, a) for sv in SERVICES for q, a in sv["faq"][:2]] +
            [("Reçetesiz serum takıyor musunuz?","Hayır. Damar içi uygulamalar hekim istemi olmadan yapılmaz."),
             ("Tıbbi atıklar ne oluyor?","Kullanılan tüm kesici-delici ve tıbbi atık malzeme ekiple geri götürülür.")])
    write("sikca-sorulan-sorular", "hub.html", 0.7, "monthly",
          title=f"Sıkça Sorulan Sorular | Evde Sağlık ve Serum | {S['name']}",
          description="Evde serum, enjeksiyon, pansuman ve sonda hizmetleri hakkında en sık sorulan sorular ve net cevaplar.",
          kicker="SSS", h1="Sıkça sorulan sorular", crumbs=[("Sıkça Sorulan Sorular", None)],
          lead="Telefonda en sık duyduğumuz sorular ve dolambaçsız cevapları.",
          IMG=img("evde-saglik-hizmeti"), faq=gfaq, cta_h="Sorunuz listede yok mu?", cta_t="Arayın, doğrudan konuşalım.",
          jsonld=[ld_faq(gfaq)])

    write("gizlilik-politikasi", "page.html", 0.3, "yearly",
          title=f"Gizlilik Politikası | {S['name']}",
          description="Yanımda Evde Sağlık gizlilik politikası ve kişisel verilerin korunması hakkında bilgilendirme.",
          kicker="Yasal", h1="Gizlilik Politikası", crumbs=[("Gizlilik Politikası", None)], lead=None,
          body="""
<h2>Toplanan bilgiler</h2>
<p>Bu web sitesi üzerinden form yoluyla veri toplanmamaktadır. İletişim yalnızca telefon ve WhatsApp üzerinden kurulur. Çağrı sırasında paylaştığınız sağlık bilgileri, yalnızca talep ettiğiniz hizmetin planlanması amacıyla kullanılır.</p>
<h2>Sağlık verileri</h2>
<p>Sağlık verileri, 6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında özel nitelikli kişisel veri sayılır. Bu veriler yalnızca hizmetin yürütülmesi amacıyla işlenir, üçüncü kişilerle paylaşılmaz ve amaç ortadan kalktığında silinir.</p>
<h2>Çerezler</h2>
<p>Bu sitede reklam veya takip amaçlı çerez kullanılmamaktadır. Sayfalarda gösterilen Google Haritalar içerikleri, siz o bölüme gelene kadar yüklenmez; yüklendiğinde Google'ın kendi çerez politikası geçerli olur.</p>
<h2>Haklarınız</h2>
<p>KVKK kapsamında kişisel verilerinize erişme, düzeltilmesini veya silinmesini isteme haklarına sahipsiniz. Talepleriniz için bize telefon ya da WhatsApp üzerinden ulaşabilirsiniz.</p>
<h2>Sorumluluk sınırı</h2>
<p>Sitedeki tüm içerik bilgilendirme amaçlıdır ve hekim muayenesi, tanı ya da tedavi yerine geçmez. Acil durumlarda 112 aranmalıdır.</p>
""",
          cta_h="Sorularınız için", cta_t="Bize telefon ya da WhatsApp üzerinden ulaşabilirsiniz.",
          jsonld=[ld_bc([("Gizlilik Politikası", None)])])


    # --- site haritası (görünür sayfa)
    sm_groups = []
    sm_groups.append(dict(
        title="Evde Sağlık Hizmetleri", url="../hizmetler/",
        sub=f"{len(SERVICES)} hizmet sayfası",
        links=[dict(slug=f"hizmetler/{x['slug']}", label=x["title"]) for x in SERVICES]))
    sm_groups.append(dict(
        title="Serum Tedavileri", url="../serum-tedavileri/",
        sub=f"{len(SERUMS)} serum sayfası",
        links=[dict(slug=f"serum-tedavileri/{x['slug']}", label=x["title"]) for x in SERUMS]))

    ilce_links = []
    for d in DISTRICTS:
        ilce_links.append(dict(slug=loc_url(d["slug"]).rstrip("/"), label=f'{d["name"]} Evde Sağlık'))
        ilce_links.append(dict(slug=loc_url(d["slug"], "serum").rstrip("/"), label=f'{d["name"]} Evde Serum'))
    sm_groups.append(dict(title="İlçeler", url="../hizmet-bolgeleri/",
                          sub=f"{len(DISTRICTS)} ilçe · her biri için evde sağlık ve evde serum sayfası",
                          links=ilce_links))

    semt_links, semt_n = [], 0
    for k, v in LOCS.items():
        if v["kind"] != "semt":
            continue
        semt_n += 1
        semt_links.append(dict(slug=loc_url(k).rstrip("/"), label=f'{v["name"]} Evde Sağlık'))
        if k in SERUM_SET:
            semt_links.append(dict(slug=loc_url(k, "serum").rstrip("/"), label=f'{v["name"]} Evde Serum'))
    sm_groups.append(dict(title="Öne Çıkan Semtler", url="../hizmet-bolgeleri/",
                          sub=f"{semt_n} semt · bölgeye özel içerikle",
                          links=semt_links))

    for d in DISTRICTS:
        ml = []
        for mh in d["mahalleler"]:
            b2 = mah_base(mh, d["name"])
            if b2 not in LOCS:
                continue
            ml.append(dict(slug=loc_url(b2).rstrip("/"), label=mh))
            if b2 in SERUM_SET:
                ml.append(dict(slug=loc_url(b2, "serum").rstrip("/"), label=f"{mh} (serum)"))
        sm_groups.append(dict(title=f'{d["name"]} Mahalleleri', url=f'../{d["slug"]}-evde-saglik/',
                              sub=f'{len(d["mahalleler"])} mahalle', links=ml))

    sm_groups.append(dict(title="Bilgi Merkezi", url="../blog/",
                          sub=f"{len(POSTS)} rehber yazısı",
                          links=[dict(slug=f"blog/{x['slug']}", label=x["title"]) for x in POSTS]))
    sm_groups.append(dict(title="Kurumsal", url="../hakkimizda/", sub="Kurumsal ve yasal sayfalar",
                          links=[dict(slug="", label="Ana Sayfa"),
                                 dict(slug="hakkimizda", label="Hakkımızda"),
                                 dict(slug="iletisim", label="İletişim"),
                                 dict(slug="hizmet-bolgeleri", label="Hizmet Bölgeleri"),
                                 dict(slug="sikca-sorulan-sorular", label="Sıkça Sorulan Sorular"),
                                 dict(slug="gizlilik-politikasi", label="Gizlilik Politikası")]))

    # eksiksizlik ağı — üretilmiş hiçbir sayfa listenin dışında kalmasın
    kapsanan = {g["url"].lstrip("./") for g in sm_groups}
    kapsanan |= {l["slug"].strip("/") + "/" for g in sm_groups for l in g["links"]}
    kapsanan |= {"", "site-haritasi/", "404.html"}
    kacak = []
    for u, _, _ in PAGES:
        rel = u.replace(S["domain"] + "/", "")
        if rel not in kapsanan:
            kacak.append(dict(slug=rel.rstrip("/"), label=rel.rstrip("/").replace("-", " ")))
    if kacak:
        sm_groups.append(dict(title="Diğer sayfalar", url="../", sub=f"{len(kacak)} sayfa", links=kacak))
        print(f"  ! site haritasına ek: {[k['slug'] for k in kacak]}")

    toplam = sum(len(g["links"]) for g in sm_groups) + 7
    write("site-haritasi", "hub.html", 0.4, "weekly",
          title=f"Site Haritası | {S['name']}",
          description=f"Yanımda Evde Sağlık site haritası — {toplam} sayfa: evde sağlık hizmetleri, serum tedavileri, ilçe ve mahalle sayfaları, bilgi merkezi.",
          kicker="Site Haritası", h1="Site haritası",
          lead=f"Sitedeki tüm sayfalar tek listede. Aradığınız hizmeti, serum tedavisini ya da mahallenizi buradan bulabilirsiniz.",
          crumbs=[("Site Haritası", None)], groups=sm_groups,
          body='<h2>Arama motorları için</h2><p>Makine tarafından okunan XML site haritası <a href="../sitemap.xml">/sitemap.xml</a> adresindedir ve her yayında otomatik güncellenir.</p>',
          cta_h="Mahallenizi listede bulamadınız mı?",
          cta_t="Arayın, adresinizi teyit edelim. Hizmet alanımızın sınırındaki bölgelere de gidiyoruz.")

    # --- anasayfa
    hfaq = [("Evde serum takmak güvenli mi?","Hekim istemi doğrultusunda, deneyimli bir hemşire tarafından ve uygulama boyunca gözlem yapılarak uygulandığında güvenlidir. Serum takılıp gidilmez; hemşire uygulama bitene kadar evde kalır."),
            ("Reçetem yok, yine de gelir misiniz?","Damar içi uygulama için hekim istemi şarttır. Reçeteniz yoksa telefonda nasıl ilerlemeniz gerektiğini anlatırız."),
            ("Gece ve hafta sonu geliyor musunuz?","Evet, 7/24 çalışıyoruz — gece saatleri, hafta sonu ve resmî tatiller dahil."),
            ("Hangi bölgelere geliyorsunuz?","Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'in tüm mahalleleri; ayrıca Hadımköy, Boğazköy, Silivri ve Çatalca yönü."),
            ("Ne kadar sürede gelirsiniz?","Adresin yerine ve o anki ekip yoğunluğuna göre değişir. Aradığınızda gerçekçi bir varış saati söyleriz."),
            ("Malzemeleri kim getiriyor?","Reçeteli ilaç ve serum size aittir; branül, set, flaster, eldiven ve tıbbi atık kutusu ekiple gelir."),
            ("Yatağa bağımlı hastaya hizmet veriyor musunuz?","Evet. Sonda değişimi, yatak yarası pansumanı, enjeksiyon ve serum uygulamaları yatağa bağımlı hastalarda evde yapılır."),
            ("Tıbbi atıklar ne oluyor?","Kullanılan tüm kesici-delici malzeme tıbbi atık kutusunda toplanır ve ekiple geri götürülür; ev çöpüne bırakılmaz.")]
    dist_ctx = []
    for d in DISTRICTS:
        tops = []
        for mh in d["mahalleler"][:7]:
            b2 = mah_base(mh, d["name"])
            if b2 in LOCS: tops.append(dict(name=mh, slug=loc_url(b2).rstrip("/")))
        dd = dict(d); dd["top"] = tops; dd["rest"] = max(0, len(d["mahalleler"]) - len(tops))
        dist_ctx.append(dd)
    write("", "home.html", 1.0, "weekly",
          title="Evde Sağlık ve Serum Hizmeti | 7/24 Hemşire | Yanımda Evde Sağlık",
          description="6 yıldır evde serum, enjeksiyon, pansuman ve sonda hizmeti. Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'de 7/24 uzman ekibimiz evinize gelir. 0551 844 82 95",
          DIST=dist_ctx, FAQ=hfaq, POSTS=POSTS, EXTRA_TXT=", ".join(EXTRA_AREAS),
          IMG_HERO=img(MED.HOME_HERO, "(max-width:1024px) 92vw, 46vw", eager=True),
          IMG_MID=img(MED.HOME_MID, "(max-width:1024px) 94vw, 1160px"),
          IMG_SERUM=img(MED.HOME_SERUM, "(max-width:760px) 92vw, 560px"),
          IMG_SERUM2=img("evde-saglikci", "(max-width:760px) 92vw, 560px"),
          jsonld=[ld_biz(), ld_faq(hfaq),
                  ld({"@context":"https://schema.org","@type":"WebSite","name":S["name"],
                      "url":S["domain"]+"/","inLanguage":"tr-TR"})])

# ---------------------------------------------------------------- yardımcı dosyalar
def build_extras():
    today = "2026-08-21"
    urls = "".join(
        f"<url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>{cf}</changefreq><priority>{p}</priority></url>\n"
        for u, p, cf in sorted(set(PAGES), key=lambda x: (-x[1], x[0])))
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls + "</urlset>\n")

    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\nDisallow: /_src/\n\nSitemap: " + S["domain"] + "/sitemap.xml\n")

    open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8").write("yanimdaevdesaglik.com\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    # 404
    html = env.get_template("hub.html").render(
        **dict(BASE, root="", canonical=S["domain"] + "/404.html", jsonld=[], noindex=True,
               title="Sayfa bulunamadı | " + S["name"],
               description="Aradığınız sayfa bulunamadı.",
               kicker="404", h1="Aradığınız sayfayı bulamadık",
               lead="Bağlantı değişmiş ya da adres yanlış yazılmış olabilir. Aşağıdan devam edebilir, acil bir durum varsa doğrudan arayabilirsiniz.",
               crumbs=[("404", None)], grid="ye-g3",
               cards=[dict(url="hizmetler/", title="Evde Sağlık Hizmetleri", text="Serum, enjeksiyon, pansuman, sonda.", icon="cross"),
                      dict(url="serum-tedavileri/", title="Serum Tedavileri", text="Hangi şikâyet için hangi serum?", icon="drop"),
                      dict(url="hizmet-bolgeleri/", title="Hizmet Bölgeleri", text="Mahallenizi bulun.", icon="pin")],
               cta_h="Acil bir durum mu var?", cta_t="7/24 çağrı alıyoruz. Telefonla ulaşmak en hızlısı."))
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(html)

    # favicon
    open(os.path.join(OUT, "assets/img/favicon.svg"), "w", encoding="utf-8").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="15" fill="#0F8A80"/>'
        '<path fill="#fff" d="M32 12c-2.6 0-4.6 2-4.6 4.6v10.8H16.6c-2.6 0-4.6 2-4.6 4.6v0c0 2.6 2 4.6 4.6 4.6h10.8v10.8c0 2.6 2 4.6 4.6 4.6'
        'h0c2.6 0 4.6-2 4.6-4.6V36.6h10.8c2.6 0 4.6-2 4.6-4.6v0c0-2.6-2-4.6-4.6-4.6H36.6V16.6c0-2.6-2-4.6-4.6-4.6z"/></svg>')

def build_images():
    """images/ içindeki her görselin TAM BOY (kırpmasız) türevlerini üretir.
    Ayrıca afişin içinden logo ve OG görselini ayıklar."""
    from PIL import Image, ImageDraw, ImageFont
    outdir = os.path.join(OUT, "assets/img/p")
    os.makedirs(outdir, exist_ok=True)
    for key, m in MED.IMAGES.items():
        src = os.path.join(OUT, "images", m["file"])
        if not os.path.exists(src):
            print(f"  ! görsel yok: {m['file']}")
            continue
        im = Image.open(src).convert("RGB")
        m["w"], m["h"] = im.size
        widths = [w for w in (480, 760, 1100, 1440) if w <= im.width] or [im.width]
        if im.width not in widths and im.width < 1440:
            widths.append(im.width)
        m["srcw"] = sorted(set(widths))
        for w in m["srcw"]:
            h = round(w * im.height / im.width)
            im.resize((w, h), Image.LANCZOS).save(
                os.path.join(outdir, f"{key}-{w}.webp"), "WEBP", quality=80, method=4)

    # --- marka varlıkları: 1. afişin içinden
    src = os.path.join(OUT, "images/evde-saglik.webp")
    if not os.path.exists(src):
        return
    a = Image.open(src).convert("RGB")
    mark = a.crop((75, 50, 218, 202))
    sq = Image.new("RGB", (240, 240), (255, 255, 255))
    mm = mark.resize((216, round(216 * mark.height / mark.width)), Image.LANCZOS)
    sq.paste(mm, ((240 - mm.width) // 2, (240 - mm.height) // 2))
    sq.save(os.path.join(OUT, "assets/img/logo-mark.png"), "PNG", optimize=True)
    sq.resize((180, 180), Image.LANCZOS).save(
        os.path.join(OUT, "assets/img/apple-touch-icon.png"), "PNG", optimize=True)
    word = a.crop((70, 45, 500, 200))
    lg = Image.new("RGB", (600, 220), (255, 255, 255))
    w2 = word.resize((560, round(560 * word.height / word.width)), Image.LANCZOS)
    lg.paste(w2, (20, (220 - w2.height) // 2))
    lg.save(os.path.join(OUT, "assets/img/logo.png"), "PNG", optimize=True)

    # --- OG görseli (fotoğraf bölgesi + degrade + marka)
    og = a.crop((705, 25, 1335, 585))
    ow, oh = og.size
    th = round(ow * 630 / 1200)
    top = max(0, (oh - th) // 2)
    og = og.crop((0, top, ow, top + min(th, oh))).resize((1200, 630), Image.LANCZOS)
    ov = Image.new("RGBA", (1200, 630), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    for y in range(630):
        dr.line([(0, y), (1200, y)], fill=(8, 32, 43, int(220 * (y / 630) ** 1.5)))
    og = Image.alpha_composite(og.convert("RGBA"), ov).convert("RGB")
    dr = ImageDraw.Draw(og)
    fp = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    try:
        f1 = ImageFont.truetype(fp, 60); f2 = ImageFont.truetype(fp, 30)
    except Exception:
        f1 = f2 = ImageFont.load_default()
    dr.text((60, 396), "Yanımda Evde Sağlık", font=f1, fill=(255, 255, 255))
    dr.text((60, 480), "Evde serum · enjeksiyon · pansuman · 7/24", font=f2, fill=(180, 240, 232))
    dr.text((60, 528), S["phone_display"], font=f2, fill=(255, 255, 255))
    dr.rectangle([(0, 618), (1200, 630)], fill=(15, 138, 128))
    og.save(os.path.join(OUT, "assets/img/og-default.jpg"), "JPEG", quality=84, optimize=True)

def img(key, sizes="(max-width:900px) 92vw, 760px", eager=False):
    """Şablonlara geçilecek görsel sözlüğü."""
    m = MED.IMAGES.get(key)
    if not m or "srcw" not in m:
        return None
    ws = m["srcw"]
    best = ws[-1]
    return dict(key=key, alt=m["alt"], cap=m["cap"], w=m["w"], h=m["h"], sizes=sizes, eager=eager,
                src=f"/assets/img/p/{key}-{best}.webp",
                srcset=", ".join(f"/assets/img/p/{key}-{w}.webp {w}w" for w in ws))

if __name__ == "__main__":
    # eski çıktıları temizle (kaynak ve varlıklar hariç)
    keep = {"_src", "assets", "images", ".git", ".gitignore", "README.md", "BRIEF.md"}
    for e in os.listdir(OUT):
        if e in keep: continue
        p = os.path.join(OUT, e)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    build_images()
    build_all()
    build_extras()
    print(f"✓ {len(set(PAGES))} sayfa üretildi")
    print(f"  konum: {sum(1 for u,_,_ in PAGES if '-evde-' in u)}  ·  toplam LOCS: {len(LOCS)}")
