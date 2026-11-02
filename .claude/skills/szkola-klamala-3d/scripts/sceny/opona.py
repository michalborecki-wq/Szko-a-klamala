"""Scena 3D: opona zimowa toczy się po zaśnieżonej drodze, pada śnieg (rolka „Zimowe opony nie są obowiązkowe”).

Ruch kamery zgrany z planszami rolki (długość treści 28 s):
  0–14%   (0–4 s)    haczyk – zbliżenie 3/4 na oponę, powolny najazd
  14–43%  (4–12 s)   plan szeroki z boku, widać śnieg
  43–61%  (12–17 s)  makro na bieżnik (plansza „1,6 mm”)
  61–77%  (17–21,5)  nisko przy drodze – opona przejeżdża („gdy jest ślisko”)
  77–100%            odjazd w górę, plan ogólny
Śnieg: dwie warstwy płatków (instancje na wierzchołkach) przesuwane w dół w pętli – deterministycznie, bez symulacji.

  blender -b -P sceny/opona.py -- --out klatki --sek 28 --szer 720 --probki 16
"""
import bpy, math, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import marka3d as M
from mathutils import Vector

o = M.argumenty()
M.wyczysc()
sc = M.scena(o)
N, FPS = sc.frame_end, o["fps"]

# ── tło: granat marki ──
w = bpy.data.worlds.new("Tlo"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = M.rgb(M.KOLOR["bg0"]); bg.inputs[1].default_value = 1.0


def mat(nazwa, kolor, rough=.5, metal=0.0, emis=None, moc=0.0):
    m = bpy.data.materials.new(nazwa); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = M.rgb(kolor) if isinstance(kolor, str) else kolor
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emis:
        b.inputs["Emission Color"].default_value = M.rgb(emis)
        b.inputs["Emission Strength"].default_value = moc
    return m


R_OP, SZER = 1.35, 0.95   # promień opony i szerokość (m, umownie)

# ── opona: torus spłaszczony + bloki bieżnika, oś koła wzdłuż X ──
bpy.ops.object.empty_add(location=(0, 0, 0)); kolo = bpy.context.object; kolo.name = "Kolo"
bpy.ops.mesh.primitive_torus_add(major_radius=R_OP - .36, minor_radius=.36, major_segments=96, minor_segments=32)
opona = bpy.context.object; bpy.ops.object.shade_smooth()
opona.rotation_euler = (0, math.radians(90), 0); opona.scale = (1, 1, SZER / .72)
opona.parent = kolo
guma = mat("Guma", "#0E121C", rough=.7)
opona.data.materials.append(guma)
# bloki bieżnika (kostki dookoła obwodu, w dwóch rzędach z przesunięciem – jak opona zimowa)
bloki = []
SK = SZER / .72
for rzad, dx in ((0, -.30), (1, 0.0), (2, .30)):        # trzy rzędy klocków w jodełkę (wzór zimowy)
    xl = dx / SK
    r_pow = (R_OP - .36) + math.sqrt(max(0.0, .36 ** 2 - xl ** 2))   # promień powierzchni opony w tym rzędzie
    for k in range(40):
        a = 2 * math.pi * (k + .5 * (rzad % 2)) / 40
        bpy.ops.mesh.primitive_cube_add(size=1)
        b = bpy.context.object
        b.scale = (.24, .13, .07)
        b.location = (dx, math.sin(a) * (r_pow + .015), math.cos(a) * (r_pow + .015))
        b.rotation_euler = (-a, 0, math.radians((-1) ** rzad * 22))
        bloki.append(b)
bpy.ops.object.select_all(action="DESELECT")
for b in bloki: b.select_set(True)
bpy.context.view_layer.objects.active = bloki[0]
bpy.ops.object.join(); biez = bpy.context.object; biez.parent = kolo
biez.data.materials.append(guma)
# felga: dysk + 5 ramion + piasta (srebro), w środku żółty akcent marki
bpy.ops.mesh.primitive_cylinder_add(radius=.66, depth=.5, vertices=96); felga = bpy.context.object
felga.rotation_euler = (0, math.radians(90), 0); felga.parent = kolo
srebro = mat("Felga", "#C9D3EA", rough=.25, metal=1.0)
ciemna = mat("FelgaCien", "#2A3247", rough=.4, metal=.6)
felga.data.materials.append(ciemna)
for k in range(5):
    a = 2 * math.pi * k / 5
    bpy.ops.mesh.primitive_cube_add(size=1); s = bpy.context.object
    s.scale = (.06, .09, .3); s.location = (.26, math.sin(a) * .34, math.cos(a) * .34)
    s.rotation_euler = (-a, 0, 0); s.parent = kolo; s.data.materials.append(srebro)
bpy.ops.mesh.primitive_cylinder_add(radius=.68, depth=.04, vertices=96); obr = bpy.context.object
obr.rotation_euler = (0, math.radians(90), 0); obr.location = (.27, 0, 0); obr.parent = kolo
obr.data.materials.append(srebro)
bpy.ops.mesh.primitive_cylinder_add(radius=.12, depth=.08, vertices=48); pias = bpy.context.object
pias.rotation_euler = (0, math.radians(90), 0); pias.location = (.3, 0, 0); pias.parent = kolo
pias.data.materials.append(mat("Piasta", M.KOLOR["yellow"], rough=.3, emis=M.KOLOR["yellow"], moc=2.0))

# ── droga: ciemny asfalt z pasem śniegu po bokach ──
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0)); droga = bpy.context.object
droga.scale = (40, 400, 1)
md = bpy.data.materials.new("Droga"); md.use_nodes = True; nn = md.node_tree.nodes
bs = nn["Principled BSDF"]; bs.inputs["Roughness"].default_value = .35
tc = nn.new("ShaderNodeTexCoord"); sep = nn.new("ShaderNodeSeparateXYZ")
ab = nn.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"
rp = nn.new("ShaderNodeValToRGB")
rp.color_ramp.elements[0].position = .045; rp.color_ramp.elements[0].color = M.rgb("#151A28")
rp.color_ramp.elements[1].position = .07; rp.color_ramp.elements[1].color = M.rgb("#DDE6F5")
noi = nn.new("ShaderNodeTexNoise"); noi.inputs["Scale"].default_value = 60
mx = nn.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs[0].default_value = .25
L = md.node_tree.links.new
L(tc.outputs["Object"], sep.inputs[0]); L(sep.outputs["X"], ab.inputs[0]); L(ab.outputs[0], rp.inputs["Fac"])
L(rp.outputs["Color"], mx.inputs[6]); L(noi.outputs["Color"], mx.inputs[7]); L(mx.outputs[2], bs.inputs["Base Color"])
droga.data.materials.append(md)

# ── śnieg: dwie warstwy płatków przesuwane w pętli ──
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=.045); platek = bpy.context.object
platek.data.materials.append(mat("Snieg", "#FFFFFF", rough=.4, emis="#EAF1FF", moc=3.0))
random.seed(7)
H = 9.0
warstwy = []
me = bpy.data.meshes.new("sniegpkt")   # ta sama chmura w obu warstwach – przejście w pętli jest niewidoczne
me.from_pydata([(random.uniform(-7, 7), random.uniform(-12, 12), random.uniform(0, H)) for _ in range(1600)], [], [])
for nr in range(2):
    ob = bpy.data.objects.new(f"Snieg{nr}", me); sc.collection.objects.link(ob)
    ob.instance_type = "VERTS"
    kopia = platek.copy(); sc.collection.objects.link(kopia); kopia.parent = ob
    warstwy.append(ob)
platek.hide_render = True; platek.hide_viewport = True
OKRES = 6.0   # s – w tym czasie płatek spada o H

# ── światła: chłodny klucz, niebieska kontra marki, żółty akcent nisko ──
bpy.ops.object.empty_add(location=(0, 0, 0)); rig = bpy.context.object; rig.name = "RigSwiatel"   # światła jadą z oponą


def swiatlo(typ, lok, energia, kolor, rozmiar=2.0, cel=(0, 0, R_OP)):
    bpy.ops.object.light_add(type=typ, location=lok); l = bpy.context.object
    l.data.energy = energia; l.data.color = M.rgb(kolor)[:3]
    if typ == "AREA": l.data.size = rozmiar
    c = l.constraints.new("TRACK_TO"); bpy.ops.object.empty_add(location=cel); t = bpy.context.object
    c.target = t; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    l.parent = rig; t.parent = rig
    return l
swiatlo("AREA", (5, 4, 6), 3200, "#F4F6FB", 4)
swiatlo("AREA", (-5, -4, 3), 4200, M.KOLOR["blue"], 3)
swiatlo("POINT", (2.5, 2.5, .4), 450, M.KOLOR["yellow"])

cam, cel = M.kamera((4, -5, 2.2), (0, 0, R_OP), ogniskowa=35)
M.poswiata(rozmiar=7, prog=1.0, mix=.08)

# ── animacja klatka po klatce ──
POZY = [  # (t, pozycja kamery względem koła, cel względem koła, ogniskowa) – koło jedzie w stronę +Y, kamera przed nim
    (0.00, (2.0, 3.8, .7), (0, 0, 0), 38),
    (0.12, (1.5, 3.1, .5), (0, 0, 0), 40),
    (0.20, (6.0, .8, 1.2), (0, 0, 0), 32),
    (0.40, (6.0, -1.5, 1.6), (0, 0, 0), 32),
    (0.46, (.7, 2.1, 1.8), (0, .95, .95), 50),      # makro na bieżnik (plansza „1,6 mm”)
    (0.59, (-.7, 2.1, 1.8), (0, .95, .95), 50),
    (0.66, (2.4, 5.2, -1.0), (0, 0, -.5), 28),       # nisko przy drodze
    (0.76, (1.8, 4.2, -1.05), (0, 0, -.6), 28),
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


PREDK = 3.2   # m/s – opona toczy się wzdłuż +Y
for f in range(1, N + 1):
    s = (f - 1) / FPS
    t = (f - 1) / max(1, N - 1)
    y = PREDK * s
    kolo.location = (0, y, R_OP); kolo.rotation_euler = (-y / R_OP, 0, 0)
    kolo.keyframe_insert("location", frame=f); kolo.keyframe_insert("rotation_euler", frame=f)
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
for ob in [kolo, rig, cam, cel, cam.data] + warstwy:
    ad = ob.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for k in fc.keyframe_points:
                k.interpolation = "CONSTANT" if ob in warstwy else "LINEAR"

M.renderuj(o)
