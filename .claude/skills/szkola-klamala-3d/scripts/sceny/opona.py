"""Scena 3D: realistyczne koło samochodu osobowego (opona zimowa 205/55 R16 na alufeldze) toczy się
po zaśnieżonej drodze, pada śnieg. Tło rolki „opony zimowe”.

Geometria w prawdziwej skali (metry), całe koło powiększone współczynnikiem SKALA, żeby pasowało
do ujęć kamery (promień zewnętrzny w scenie = 1,35):
  • opona: przekrój obrócony wokół osi (bark, bok z wybrzuszeniem, stopka), bieżnik zimowy
    kierunkowy w „V” – 64 podziałki × 6 klocków z prawdziwej geometrii, lamele jako mikro-wgłębienia
    w shaderze, napisy na boku (205/55 R16, M+S, 3PMSF) wytłoczone z tekstury `assets/opona_bok.png`
    (generator: sceny/opona_bok.py);
  • felga 16" z 5 podwójnymi ramionami (boolean + fazowanie), śruby, kołpak z żółtym pierścieniem marki;
  • tarcza hamulcowa (obraca się) i żółty zacisk (nie obraca się);
  • oświetlenie: odbicia z HDRI dołączonego do Blendera + światła marki.

Ruch kamery zgrany z planszami rolki (28 s treści):
  0–14% haczyk – 3/4 z przodu, najazd · 14–43% szeroko z boku · 43–61% makro na bieżnik („1,6 mm”)
  61–77% nisko przy drodze · 77–100% odjazd w górę.

  blender -b -P sceny/opona.py -- --out klatki --sek 29 --fps 24 --szer 540 --probki 12 --odszum 1
  (ok. 16 s/klatkę na 4 rdzeniach CPU → ok. 3 h; tło podkładane polem "tlo3d" z "fps": 24)
"""
import bpy, bmesh, math, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import marka3d as M
from mathutils import Vector, Matrix

o = M.argumenty()
M.wyczysc()
sc = M.scena(o)
sc.cycles.max_bounces = 4
sc.cycles.glossy_bounces = 2
sc.cycles.diffuse_bounces = 1
sc.render.use_motion_blur = True
sc.render.motion_blur_shutter = .12
N, FPS = sc.frame_end, o["fps"]
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets")

# ── świat: granat marki widziany przez kamerę, odbicia z HDRI miasta ──
w = bpy.data.worlds.new("Tlo"); sc.world = w; w.use_nodes = True
nt = w.node_tree; nn = nt.nodes; nn.clear()
env = nn.new("ShaderNodeTexEnvironment")
env.image = bpy.data.images.load(os.path.join(bpy.utils.system_resource("DATAFILES") or os.path.join(os.path.dirname(bpy.app.binary_path), "4.2", "datafiles"), "studiolights", "world", "city.exr"))
b_env = nn.new("ShaderNodeBackground"); b_env.inputs[1].default_value = .35
b_cam = nn.new("ShaderNodeBackground"); b_cam.inputs[0].default_value = M.rgb(M.KOLOR["bg0"])
lp = nn.new("ShaderNodeLightPath"); mix = nn.new("ShaderNodeMixShader"); out = nn.new("ShaderNodeOutputWorld")
nt.links.new(env.outputs[0], b_env.inputs[0])
nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
nt.links.new(b_env.outputs[0], mix.inputs[1]); nt.links.new(b_cam.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], out.inputs[0])


def principled(nazwa, kolor, rough=.5, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(nazwa); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = M.rgb(kolor) if isinstance(kolor, str) else kolor
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    return m, b


def obiekt(nazwa, bm, mat=None, gladki=True, normalne=True):
    if normalne:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(nazwa); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(nazwa, me); sc.collection.objects.link(ob)
    if gladki:
        for p in me.polygons: p.use_smooth = True
    if mat: me.materials.append(mat)
    return ob


def wygladz_katem(ob, kat=35):
    bpy.ops.object.select_all(action="DESELECT"); ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(kat))


def obrot_profilu(profil, seg=256, zamkniety=False):
    """Bryła obrotowa wokół osi X z profilu [(x, r), …]. Zwraca bmesh."""
    bm = bmesh.new()
    rings = []
    for i in range(seg):
        t = 2 * math.pi * i / seg
        rings.append([bm.verts.new((x, r * math.sin(t), r * math.cos(t))) for x, r in profil])
    n = len(profil)
    for i in range(seg):
        a, b = rings[i], rings[(i + 1) % seg]
        for j in range(n - 1 + (1 if zamkniety else 0)):
            j2 = (j + 1) % n
            bm.faces.new((a[j], a[j2], b[j2], b[j]))
    bm.normal_update()
    return bm


R_B, H_B = 0.307, 0.009          # promień podstawy bieżnika i wysokość klocków (zimówka ~9 mm)
SKALA = 1.35 / (R_B + H_B)
R_OP = 1.35
RS, S_PL = 0.03, 0.078           # promień barku, połowa płaskiej części bieżnika
S_BARK = S_PL + RS * math.pi / 2


def P(s):
    """Punkt profilu bieżnika (x, r) i normalna dla współrzędnej łuku s (od środka bieżnika)."""
    zn = 1 if s >= 0 else -1
    a = abs(s)
    if a <= S_PL:
        return (s, R_B), (0.0, 1.0)
    f = min((a - S_PL) / RS, math.pi / 2)
    return (zn * (S_PL + RS * math.sin(f)), R_B - RS + RS * math.cos(f)), (zn * math.sin(f), math.cos(f))


def mapuj(u, s, h):
    (x, r), (nx, nr) = P(s)
    x, r = x + h * nx, r + h * nr
    t = u / R_B
    return (x, r * math.sin(t), r * math.cos(t))


# ── koło (obraca się) i nośnik (tylko jedzie) ──
kolo = bpy.data.objects.new("Kolo", None); sc.collection.objects.link(kolo)
nosnik = bpy.data.objects.new("Nosnik", None); sc.collection.objects.link(nosnik)
for e in (kolo, nosnik): e.scale = (SKALA,) * 3

# ── materiał gumy: czarna, półmatowa, mikro-faktura, lamele w bieżniku, wytłoczenia na boku ──
guma = bpy.data.materials.new("Guma"); guma.use_nodes = True
g = guma.node_tree; gn = g.nodes; GL = g.links.new
gb = gn["Principled BSDF"]
gb.inputs["Base Color"].default_value = M.rgb("#121315")
gb.inputs["Specular IOR Level"].default_value = .3
tc = gn.new("ShaderNodeTexCoord")
mik = gn.new("ShaderNodeTexNoise"); mik.inputs["Scale"].default_value = 900; mik.inputs["Detail"].default_value = 4
GL(tc.outputs["Object"], mik.inputs["Vector"])
plam = gn.new("ShaderNodeTexNoise"); plam.inputs["Scale"].default_value = 40
GL(tc.outputs["Object"], plam.inputs["Vector"])
rr = gn.new("ShaderNodeMapRange"); rr.inputs[3].default_value = .62; rr.inputs[4].default_value = .85
GL(plam.outputs["Fac"], rr.inputs[0])
# lamele: cienkie rowki zygzakiem równoległe do rowków poprzecznych (UV = (u, s) w metrach)
uvn = gn.new("ShaderNodeUVMap"); uvs = gn.new("ShaderNodeSeparateXYZ"); GL(uvn.outputs[0], uvs.inputs[0])
ab = gn.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"; GL(uvs.outputs["Y"], ab.inputs[0])
zz = gn.new("ShaderNodeMath"); zz.operation = "PINGPONG"; zz.inputs[1].default_value = .0012; GL(ab.outputs[0], zz.inputs[0])
k1 = gn.new("ShaderNodeMath"); k1.operation = "MULTIPLY_ADD"; k1.inputs[1].default_value = -.75
GL(ab.outputs[0], k1.inputs[0]); GL(uvs.outputs["X"], k1.inputs[2])
k2 = gn.new("ShaderNodeMath"); k2.operation = "ADD"; GL(k1.outputs[0], k2.inputs[0]); GL(zz.outputs[0], k2.inputs[1])
k3 = gn.new("ShaderNodeMath"); k3.operation = "MULTIPLY"; k3.inputs[1].default_value = 1 / .0075
GL(k2.outputs[0], k3.inputs[0])
fr = gn.new("ShaderNodeMath"); fr.operation = "FRACT"; GL(k3.outputs[0], fr.inputs[0])
lin = gn.new("ShaderNodeMapRange"); lin.inputs[1].default_value = .0; lin.inputs[2].default_value = .15
lin.inputs[3].default_value = 0; lin.inputs[4].default_value = 1; GL(fr.outputs[0], lin.inputs[0])
# napisy na boku: współrzędne biegunowe obiektu → tekstura pasa
sep = gn.new("ShaderNodeSeparateXYZ"); GL(tc.outputs["Object"], sep.inputs[0])
at = gn.new("ShaderNodeMath"); at.operation = "ARCTAN2"; GL(sep.outputs["Y"], at.inputs[0]); GL(sep.outputs["Z"], at.inputs[1])
sg = gn.new("ShaderNodeMath"); sg.operation = "SIGN"; GL(sep.outputs["X"], sg.inputs[0])
at2 = gn.new("ShaderNodeMath"); at2.operation = "MULTIPLY"; GL(at.outputs[0], at2.inputs[0]); GL(sg.outputs[0], at2.inputs[1])
uu = gn.new("ShaderNodeMath"); uu.operation = "MULTIPLY_ADD"; uu.inputs[1].default_value = 1 / (2 * math.pi); uu.inputs[2].default_value = .5
GL(at2.outputs[0], uu.inputs[0])
ln = gn.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
yz = gn.new("ShaderNodeCombineXYZ"); GL(sep.outputs["Y"], yz.inputs[0]); GL(sep.outputs["Z"], yz.inputs[1]); GL(yz.outputs[0], ln.inputs[0])
vv = gn.new("ShaderNodeMapRange"); vv.inputs[1].default_value = .222; vv.inputs[2].default_value = .272
vv.inputs[3].default_value = 0; vv.inputs[4].default_value = 1; vv.clamp = False
GL(ln.outputs["Value"], vv.inputs[0])
uvb = gn.new("ShaderNodeCombineXYZ"); GL(uu.outputs[0], uvb.inputs[0]); GL(vv.outputs[0], uvb.inputs[1])
img = gn.new("ShaderNodeTexImage"); img.image = bpy.data.images.load(os.path.join(ASSETS, "opona_bok.png"))
img.image.colorspace_settings.name = "Non-Color"; img.extension = "CLIP"
GL(uvb.outputs[0], img.inputs[0])
bok = gn.new("ShaderNodeMath"); bok.operation = "GREATER_THAN"; bok.inputs[1].default_value = .085
abx = gn.new("ShaderNodeMath"); abx.operation = "ABSOLUTE"; GL(sep.outputs["X"], abx.inputs[0]); GL(abx.outputs[0], bok.inputs[0])
napis = gn.new("ShaderNodeMath"); napis.operation = "MULTIPLY"; GL(img.outputs["Color"], napis.inputs[0]); GL(bok.outputs[0], napis.inputs[1])
nbiez = gn.new("ShaderNodeMath"); nbiez.operation = "LESS_THAN"; nbiez.inputs[1].default_value = .5
GL(bok.outputs[0], nbiez.inputs[0])
lam = gn.new("ShaderNodeMath"); lam.operation = "MULTIPLY"; GL(lin.outputs[0], lam.inputs[0]); GL(nbiez.outputs[0], lam.inputs[1])
wys = gn.new("ShaderNodeMath"); wys.operation = "ADD"; GL(napis.outputs[0], wys.inputs[0]); GL(lam.outputs[0], wys.inputs[1])
bump1 = gn.new("ShaderNodeBump"); bump1.inputs["Strength"].default_value = .9; bump1.inputs["Distance"].default_value = .0025
GL(wys.outputs[0], bump1.inputs["Height"])
bump2 = gn.new("ShaderNodeBump"); bump2.inputs["Strength"].default_value = .12
GL(mik.outputs["Fac"], bump2.inputs["Height"]); GL(bump1.outputs[0], bump2.inputs["Normal"])
GL(bump2.outputs[0], gb.inputs["Normal"])
if os.environ.get("DEBUG_LAMELE"):
    gb.inputs["Emission Color"].default_value = (1, 0, 0, 1); GL(lam.outputs[0], gb.inputs["Emission Strength"])
rmix = gn.new("ShaderNodeMix"); rmix.data_type = "FLOAT"; rmix.inputs[3].default_value = .32
GL(napis.outputs[0], rmix.inputs[0]); GL(rr.outputs[0], rmix.inputs[2]); GL(rmix.outputs[0], gb.inputs["Roughness"])

# ── opona: korpus obrotowy ──
prof = [P(-S_BARK + 2 * S_BARK * i / 40)[0] for i in range(41)]
bokp = [(.109, .262), (.1095, .248), (.1065, .234), (.1015, .222), (.097, .213), (.094, .206), (.094, .201)]
profil = [(-x, r) for x, r in reversed(bokp)] + prof + bokp
opona = obiekt("Opona", obrot_profilu(profil, seg=320), guma); opona.parent = kolo
opona.data.uv_layers.new(name="UVMap")

# ── bieżnik: klocki w „V”, 64 podziałki × 3 strefy × 2 strony ──
PODZ = 64
PITCH = 2 * math.pi * R_B / PODZ
ROWEK = .0045
STREFY = [  # (s0, s1, nachylenie, przesunięcie, siatka u, siatka s)
    (.004, .035, .75, 0.0, 3, 3),
    (.041, .071, .65, .006, 3, 3),
    (.077, .118, .12, .013, 3, 5),
]
bm = bmesh.new()
uvl = bm.loops.layers.uv.new("UVMap")


def sciana(vs, uvsy):
    f = bm.faces.new(vs)
    for l, q in zip(f.loops, uvsy): l[uvl].uv = q


for k in range(PODZ):
    for strona in (1, -1):
        for s0, s1, nach, przes, nu, ns in STREFY:
            u0 = k * PITCH + przes
            dl = PITCH - ROWEK
            gora, dol, uvg = {}, {}, {}
            for i in range(nu + 1):
                for j in range(ns + 1):
                    s = s0 + (s1 - s0) * j / ns
                    u = u0 + nach * (s - s0) + dl * i / nu
                    ss = strona * s
                    gora[i, j] = bm.verts.new(mapuj(u, ss, H_B))
                    dol[i, j] = bm.verts.new(mapuj(u, ss, -.002))
                    uvg[i, j] = (u, ss)
            for i in range(nu):
                for j in range(ns):
                    q = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
                    if strona < 0: q.reverse()
                    sciana([gora[x] for x in q], [uvg[x] for x in q])
            obw = [(i, 0) for i in range(nu)] + [(nu, j) for j in range(ns)] + \
                  [(i, ns) for i in range(nu, 0, -1)] + [(0, j) for j in range(ns, 0, -1)]
            for a, b in zip(obw, obw[1:] + obw[:1]):
                q = [dol[a], dol[b], gora[b], gora[a]]
                uq = [uvg[a], uvg[b], uvg[b], uvg[a]]
                if strona < 0: q.reverse(); uq.reverse()
                sciana(q, uq)
bm.normal_update()
biez = obiekt("Bieznik", bm, guma, gladki=False, normalne=False); biez.parent = kolo
fa = biez.modifiers.new("Faza", "BEVEL"); fa.width = .0009; fa.segments = 2; fa.limit_method = "ANGLE"
wygladz_katem(biez, 40)

# ── felga 16": rant + bęben ──
alu, _ = principled("Felga", "#AEB4BD", rough=.24, metal=1.0)
ranty = [(.094, .200), (.098, .212), (.092, .216), (.086, .205), (.080, .196), (.080, .190),
         (-.080, .190), (-.080, .196), (-.086, .205), (-.092, .216), (-.098, .212), (-.094, .200)]
ran = obiekt("Rant", obrot_profilu(ranty, seg=256), alu); ran.parent = kolo
wygladz_katem(ran, 40)
# lico felgi: zamknięty profil obrotowy (wklęsłe), potem okna boolean
lico = [(.060, .032), (.062, .055), (.050, .085), (.050, .120), (.062, .160), (.078, .186), (.082, .198),
        (.072, .198), (.056, .182), (.040, .150), (.030, .110), (.034, .070), (.040, .045), (.040, .032)]
fe = obiekt("Lico", obrot_profilu(lico, seg=256, zamkniety=True), alu); fe.parent = kolo


def okno(kat_sr, pol_kata, pol_ramion, r0, r1, n=14):
    """Wycinak okna: krawędzie boczne w stałej odległości (pol_ramion, m) od osi ramion."""
    lewa = lambda r: kat_sr - pol_kata + pol_ramion / r
    prawa = lambda r: kat_sr + pol_kata - pol_ramion / r
    pts = [(r0 + (r1 - r0) * i / n, None, 0) for i in range(n + 1)]
    pts = [(r, lewa(r)) for r, _, _ in pts]
    pts += [(r1, lewa(r1) + (prawa(r1) - lewa(r1)) * i / n) for i in range(1, n)]
    pts += [(r0 + (r1 - r0) * i / n, prawa(r0 + (r1 - r0) * i / n)) for i in range(n, -1, -1)]
    pts += [(r0, lewa(r0) + (prawa(r0) - lewa(r0)) * i / n) for i in range(n - 1, 0, -1)]
    bm = bmesh.new()
    lo = [bm.verts.new((-.1, r * math.sin(a), r * math.cos(a))) for r, a in pts]
    hi = [bm.verts.new((.2, r * math.sin(a), r * math.cos(a))) for r, a in pts]
    m = len(pts)
    for i in range(m):
        bm.faces.new((lo[i], lo[(i + 1) % m], hi[(i + 1) % m], hi[i]))
    bm.faces.new(list(reversed(lo))); bm.faces.new(hi)
    bm.normal_update()
    return bm


wyc_me = bpy.data.meshes.new("Wycinaki")
wyc = bmesh.new()
for k in range(5):
    a = 2 * math.pi * k / 5
    for bmo in (okno(a + math.pi / 5, math.pi / 5, .031, .088, .168, n=28),   # duże okno między parami ramion
                okno(a, 0.0, -.004, .104, .160, n=20)):                         # szczelina 8 mm w parze ramion
        tmp = bpy.data.meshes.new("t"); bmo.to_mesh(tmp); bmo.free()
        wyc.from_mesh(tmp); bpy.data.meshes.remove(tmp)
wyc_ob = obiekt("Wycinaki", wyc, gladki=False)
wyc_ob.parent = kolo
zaok = wyc_ob.modifiers.new("Zaokr", "BEVEL"); zaok.width = .006; zaok.segments = 4
zaok.limit_method = "ANGLE"; zaok.angle_limit = math.radians(40); zaok.affect = "EDGES"
wyc_ob.hide_render = True; wyc_ob.hide_viewport = True
bo = fe.modifiers.new("Okna", "BOOLEAN"); bo.object = wyc_ob; bo.operation = "DIFFERENCE"; bo.solver = "EXACT"
wygladz_katem(fe, 35)

# śruby, kołpak z żółtym pierścieniem marki
chrom, _ = principled("Chrom", "#E6E9EE", rough=.08, metal=1.0)
for k in range(5):
    a = 2 * math.pi * (k + .5) / 5
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=.0105, radius2=.0105, depth=.014)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"))
    bmesh.ops.translate(bm, verts=bm.verts, vec=(.066, .052 * math.sin(a), .052 * math.cos(a)))
    s = obiekt(f"Sruba{k}", bm, chrom, gladki=False); s.parent = kolo
    fs = s.modifiers.new("F", "BEVEL"); fs.width = .0012; fs.segments = 2
kap = obiekt("Kolpak", obrot_profilu([(.058, .0), (.070, .010), (.072, .024), (.066, .031), (.058, .031)], seg=96),
             principled("Kolpak", "#0D0F14", rough=.12, coat=1.0)[0]); kap.parent = kolo
zolty, zb = principled("ZoltyPierscien", M.KOLOR["yellow"], rough=.25)
zb.inputs["Emission Color"].default_value = M.rgb(M.KOLOR["yellow"]); zb.inputs["Emission Strength"].default_value = 1.2
pier = obiekt("Pierscien", obrot_profilu([(.0715, .0255), (.0735, .0255), (.0735, .0215), (.0715, .0215)], seg=96, zamkniety=True), zolty)
pier.parent = kolo

# tarcza hamulcowa (obraca się) i zacisk (nie obraca się)
stal, _ = principled("Tarcza", "#8C9097", rough=.32, metal=1.0)
tarcza = obiekt("Tarcza", obrot_profilu([(-.008, .072), (-.008, .150), (-.032, .150), (-.032, .072)], seg=160, zamkniety=True), stal)
tarcza.parent = kolo
zac_m, _ = principled("Zacisk", M.KOLOR["yellow"], rough=.28, coat=.8)
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1)
bmesh.ops.scale(bm, vec=(.07, .085, .05), verts=bm.verts)
bmesh.ops.translate(bm, verts=bm.verts, vec=(-.02, -.075, .135))
zac = obiekt("Zacisk", bm, zac_m, gladki=False); zac.parent = nosnik
zf = zac.modifiers.new("F", "BEVEL"); zf.width = .012; zf.segments = 4
wygladz_katem(zac, 50)

# ── droga: asfalt (ziarno kruszywa), mokre plamy, śnieg na poboczu ──
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0)); droga = bpy.context.object
droga.scale = (40, 400, 1); bpy.ops.object.transform_apply(scale=True)
md = bpy.data.materials.new("Droga"); md.use_nodes = True; dn = md.node_tree.nodes; DL = md.node_tree.links.new
dout = dn["Material Output"]; dn.remove(dn["Principled BSDF"])
asf = dn.new("ShaderNodeBsdfPrincipled"); sn = dn.new("ShaderNodeBsdfPrincipled")
tcd = dn.new("ShaderNodeTexCoord")
vor = dn.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 70.0     # kruszywo ~1 cm w skali koła
DL(tcd.outputs["Object"], vor.inputs["Vector"])
nz = dn.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = .35; nz.inputs["Detail"].default_value = 6
DL(tcd.outputs["Object"], nz.inputs["Vector"])
kol = dn.new("ShaderNodeValToRGB"); kol.color_ramp.elements[0].color = M.rgb("#16181D"); kol.color_ramp.elements[1].color = M.rgb("#30333A")
DL(vor.outputs["Distance"], kol.inputs["Fac"]); DL(kol.outputs["Color"], asf.inputs["Base Color"])
mokre = dn.new("ShaderNodeMapRange"); mokre.inputs[1].default_value = .45; mokre.inputs[2].default_value = .6
mokre.inputs[3].default_value = .62; mokre.inputs[4].default_value = .16
DL(nz.outputs["Fac"], mokre.inputs[0]); DL(mokre.outputs[0], asf.inputs["Roughness"])
bd = dn.new("ShaderNodeBump"); bd.inputs["Strength"].default_value = .18; DL(vor.outputs["Distance"], bd.inputs["Height"])
DL(bd.outputs[0], asf.inputs["Normal"])
sn.inputs["Base Color"].default_value = M.rgb("#E4EAF4"); sn.inputs["Roughness"].default_value = .75
sn.inputs["Subsurface Weight"].default_value = .2
nzs = dn.new("ShaderNodeTexNoise"); nzs.inputs["Scale"].default_value = 3; nzs.inputs["Detail"].default_value = 8
DL(tcd.outputs["Object"], nzs.inputs["Vector"])
bs = dn.new("ShaderNodeBump"); bs.inputs["Strength"].default_value = .5; DL(nzs.outputs["Fac"], bs.inputs["Height"]); DL(bs.outputs[0], sn.inputs["Normal"])
sx = dn.new("ShaderNodeSeparateXYZ"); DL(tcd.outputs["Object"], sx.inputs[0])
ax = dn.new("ShaderNodeMath"); ax.operation = "ABSOLUTE"; DL(sx.outputs["X"], ax.inputs[0])
zab = dn.new("ShaderNodeMath"); zab.operation = "MULTIPLY_ADD"; zab.inputs[1].default_value = .9
DL(nzs.outputs["Fac"], zab.inputs[0]); DL(ax.outputs[0], zab.inputs[2])
mask = dn.new("ShaderNodeMapRange"); mask.inputs[1].default_value = 2.6; mask.inputs[2].default_value = 2.9
DL(zab.outputs[0], mask.inputs[0])
ms = dn.new("ShaderNodeMixShader"); DL(mask.outputs[0], ms.inputs[0]); DL(asf.outputs[0], ms.inputs[1]); DL(sn.outputs[0], ms.inputs[2])
DL(ms.outputs[0], dout.inputs[0])
droga.data.materials.append(md)

# ── śnieg: dwie warstwy płatków w pętli (bez rozmycia ruchu – skok pętli byłby widoczny) ──
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=.03); platek = bpy.context.object
pm, pb = principled("Snieg", "#FFFFFF", rough=.5)
pb.inputs["Emission Color"].default_value = M.rgb("#EAF1FF"); pb.inputs["Emission Strength"].default_value = 1.6
platek.data.materials.append(pm)
random.seed(7)
H = 9.0
warstwy = []
me = bpy.data.meshes.new("sniegpkt")
me.from_pydata([(random.uniform(-7, 7), random.uniform(-12, 12), random.uniform(0, H)) for _ in range(1800)], [], [])
for nr in range(2):
    ob = bpy.data.objects.new(f"Snieg{nr}", me); sc.collection.objects.link(ob)
    ob.instance_type = "VERTS"
    kopia = platek.copy(); sc.collection.objects.link(kopia); kopia.parent = ob
    kopia.cycles.use_motion_blur = False; ob.cycles.use_motion_blur = False
    warstwy.append(ob)
platek.hide_render = True; platek.hide_viewport = True
OKRES = 6.0

# ── światła: chłodny klucz, niebieska kontra marki, wypełnienie boku, żółty akcent; jadą z kołem ──
rig = bpy.data.objects.new("RigSwiatel", None); sc.collection.objects.link(rig)


def swiatlo(typ, lok, energia, kolor, rozmiar=2.0, cel=(0, 0, R_OP)):
    bpy.ops.object.light_add(type=typ, location=lok); l = bpy.context.object
    l.data.energy = energia; l.data.color = M.rgb(kolor)[:3]
    if typ == "AREA": l.data.size = rozmiar
    t = bpy.data.objects.new("cel_" + l.name, None); sc.collection.objects.link(t); t.location = cel
    c = l.constraints.new("TRACK_TO"); c.target = t; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    l.parent = rig; t.parent = rig
    return l


swiatlo("AREA", (5, 4, 6), 1500, "#F4F6FB", 4)
swiatlo("AREA", (-5, -4, 3), 3600, M.KOLOR["blue"], 3)
swiatlo("AREA", (6, -2, 1.6), 450, "#F4F6FB", 1.5)
swiatlo("POINT", (2.5, 2.5, .4), 220, M.KOLOR["yellow"])

cam, cel = M.kamera((4, -5, 2.2), (0, 0, R_OP), ogniskowa=35)
M.poswiata(rozmiar=7, prog=1.2, mix=.06)

POZY = [  # (t, kamera wzgl. koła, cel wzgl. koła, ogniskowa) – koło jedzie w stronę +Y
    (0.00, (2.6, 3.6, .5), (0, 0, 0), 38),
    (0.12, (2.0, 3.0, .35), (0, 0, 0), 40),
    (0.20, (6.0, .8, 1.0), (0, 0, 0), 32),
    (0.40, (6.0, -1.5, 1.4), (0, 0, 0), 32),
    (0.46, (.9, 2.2, 1.6), (0, .95, .95), 50),      # makro na bieżnik (plansza „1,6 mm”)
    (0.59, (-.5, 2.2, 1.7), (0, .95, .95), 50),
    (0.66, (2.6, 5.2, -1.0), (0, 0, -.5), 28),       # nisko przy drodze
    (0.76, (2.0, 4.2, -1.05), (0, 0, -.6), 28),
    (0.86, (5.5, 6.5, 3.5), (0, 0, 0), 30),
    (1.00, (7.5, 8.5, 6.0), (0, -2, 0), 30),
]


def poza(t):
    for (t0, p0, c0, f0), (t1, p1, c1, f1) in zip(POZY, POZY[1:]):
        if t <= t1:
            u = M.wygladz((t - t0) / max(1e-6, t1 - t0))
            lerp = lambda a, b: tuple(x + (y - x) * u for x, y in zip(a, b))
            return lerp(p0, p1), lerp(c0, c1), f0 + (f1 - f0) * u
    return POZY[-1][1:]


PREDK = 3.2
for f in range(1, N + 1):
    s = (f - 1) / FPS
    t = (f - 1) / max(1, N - 1)
    y = PREDK * s
    for e in (kolo, nosnik):
        e.location = (0, y, R_OP); e.keyframe_insert("location", frame=f)
    kolo.rotation_euler = (-y / R_OP, 0, 0); kolo.keyframe_insert("rotation_euler", frame=f)
    rig.location = (0, y, 0); rig.keyframe_insert("location", frame=f)
    p, c, fl = poza(t)
    cam.location = Vector(p) + Vector((0, y, R_OP)); cel.location = Vector(c) + Vector((0, y, R_OP))
    cam.data.lens = fl
    cam.keyframe_insert("location", frame=f); cel.keyframe_insert("location", frame=f)
    cam.data.keyframe_insert("lens", frame=f)
    spad = (s % OKRES) / OKRES * H
    for nr, ob in enumerate(warstwy):
        ob.location = (0, y, (nr * H - spad) % (2 * H) - .5)
        ob.keyframe_insert("location", frame=f)
for ob in [kolo, nosnik, rig, cam, cel, cam.data] + warstwy:
    ad = ob.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for k in fc.keyframe_points:
                k.interpolation = "CONSTANT" if ob in warstwy else "LINEAR"

M.renderuj(o)
