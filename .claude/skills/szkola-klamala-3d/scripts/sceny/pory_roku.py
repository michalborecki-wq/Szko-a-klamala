"""Scena 3D: Ziemia na orbicie wokół Słońca z nachyloną osią (23,4°).

Fabuła ruchu (dopasowana do rolki „pory roku”):
  0–5%    Ziemia po dalekiej stronie orbity (lipiec), północ pochylona KU Słońcu,
  5–50%   przelot na bliską stronę (styczeń), północ pochylona OD Słońca,
  75–95%  kamera zbliża się do Ziemi – widać nachyloną oś (prawdziwa przyczyna pór roku).
Elipsa orbity jest celowo prawie okrągła (jak w rzeczywistości) – Słońce lekko przesunięte od środka.

Uruchomienie:
  blender -b -P sceny/pory_roku.py -- --out klatki --sek 24 --szer 1080 --probki 24
"""
import bpy, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import marka3d as M
from mathutils import Vector, Quaternion

o = M.argumenty()
M.wyczysc()
sc = M.scena(o)
M.tlo_gwiazdy()
N = sc.frame_end
FPS = o["fps"]

A, B, PRZES = 6.0, 5.9, 0.55        # półosie orbity i przesunięcie Słońca (ognisko) – lekko powiększone dla czytelności
NACHYL = math.radians(23.4)

# ── Słońce ──
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, segments=96, ring_count=48, location=(0, 0, 0))
slonce = bpy.context.object
bpy.ops.object.shade_smooth()
m = bpy.data.materials.new("Slonce"); m.use_nodes = True
nn = m.node_tree.nodes; nn.clear()
tex = nn.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 6; tex.inputs["Detail"].default_value = 8
ramp = nn.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = M.rgb("#FF8A1F"); ramp.color_ramp.elements[1].color = M.rgb("#FFE28A")
lw = nn.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.35
mix = nn.new("ShaderNodeMix"); mix.data_type = "RGBA"
mix.inputs[7].default_value = M.rgb("#FF6A00")
em = nn.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 6.0
out = nn.new("ShaderNodeOutputMaterial")
L = m.node_tree.links.new
L(tex.outputs["Fac"], ramp.inputs["Fac"]); L(ramp.outputs["Color"], mix.inputs[6])
L(lw.outputs["Fresnel"], mix.inputs[0]); L(mix.outputs[2], em.inputs["Color"])
L(em.outputs[0], out.inputs[0])
slonce.data.materials.append(m)
slonce.visible_shadow = False
bpy.ops.object.light_add(type="POINT", location=(0, 0, 0))
sw = bpy.context.object
sw.data.energy = 9000; sw.data.shadow_soft_size = 1.4; sw.data.color = M.rgb("#FFF1D6")[:3]

# ── orbita (cienka niebieska linia) ──
bpy.ops.curve.primitive_bezier_circle_add(radius=1.0, location=(-PRZES, 0, 0))
orb = bpy.context.object
orb.scale = (A, B, 1)
orb.data.bevel_depth = 0.012
orb.data.resolution_u = 64
orb.data.materials.append(M.emisja("Orbita", M.KOLOR["blue"], 4.0))


def pozycja(kat):   # kąt 0 = peryhelium (+X, styczeń), 180° = aphelium (lipiec)
    return Vector((-PRZES + A * math.cos(kat), B * math.sin(kat), 0))


# ── Ziemia: pivot (stała orientacja osi w przestrzeni) → kula obracająca się wokół osi ──
bpy.ops.object.empty_add(location=pozycja(math.pi))
piv = bpy.context.object; piv.name = "ZiemiaPivot"
piv.rotation_euler = (0, NACHYL, 0)          # północ pochylona w stronę +X (od Słońca w styczniu)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.78, segments=128, ring_count=64)
ziemia = bpy.context.object
bpy.ops.object.shade_smooth()
ziemia.parent = piv
mz = bpy.data.materials.new("Ziemia"); mz.use_nodes = True
nn = mz.node_tree.nodes; nn.clear()
tc = nn.new("ShaderNodeTexCoord")
noise = nn.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 2.2
noise.inputs["Detail"].default_value = 10; noise.inputs["Roughness"].default_value = 0.6
lad = nn.new("ShaderNodeValToRGB")
e = lad.color_ramp.elements
e[0].position = 0.50; e[0].color = M.rgb("#123C9C")      # ocean (niebieski marki, ciemniejszy)
e[1].position = 0.53; e[1].color = M.rgb("#2F7D4F")      # ląd
e3 = lad.color_ramp.elements.new(0.62); e3.color = M.rgb("#B59A62")
sep = nn.new("ShaderNodeSeparateXYZ")
pol = nn.new("ShaderNodeMath"); pol.operation = "ABSOLUTE"
polr = nn.new("ShaderNodeValToRGB")                         # czapy lodowe
polr.color_ramp.elements[0].position = 0.80; polr.color_ramp.elements[0].color = (0, 0, 0, 1)
polr.color_ramp.elements[1].position = 0.86; polr.color_ramp.elements[1].color = (1, 1, 1, 1)
mixl = nn.new("ShaderNodeMix"); mixl.data_type = "RGBA"; mixl.inputs[7].default_value = M.rgb("#EEF3FF")
rough = nn.new("ShaderNodeMapRange")
bsdf = nn.new("ShaderNodeBsdfPrincipled")
lw = nn.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
atm = nn.new("ShaderNodeEmission"); atm.inputs["Color"].default_value = M.rgb("#5B8CFF")
atmm = nn.new("ShaderNodeMath"); atmm.operation = "MULTIPLY"; atmm.inputs[1].default_value = 1.4
add = nn.new("ShaderNodeAddShader")
outz = nn.new("ShaderNodeOutputMaterial")
L = mz.node_tree.links.new
L(tc.outputs["Object"], noise.inputs["Vector"]); L(noise.outputs["Fac"], lad.inputs["Fac"])
L(tc.outputs["Object"], sep.inputs[0]); L(sep.outputs["Z"], pol.inputs[0])
L(pol.outputs[0], polr.inputs["Fac"])
L(lad.outputs["Color"], mixl.inputs[6]); L(polr.outputs["Color"], mixl.inputs[0])
L(mixl.outputs[2], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.55
L(lw.outputs["Fresnel"], atmm.inputs[0]); L(atmm.outputs[0], atm.inputs["Strength"])
L(bsdf.outputs[0], add.inputs[0]); L(atm.outputs[0], add.inputs[1]); L(add.outputs[0], outz.inputs[0])
ziemia.data.materials.append(mz)

# oś obrotu – żółta (akcent marki), przechodzi przez bieguny
bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=2.5)
os_ = bpy.context.object; os_.parent = piv
os_.data.materials.append(M.emisja("Os", M.KOLOR["yellow"], 6.0))
# równik – cienki pierścień, żeby nachylenie było czytelne
bpy.ops.mesh.primitive_torus_add(major_radius=0.88, minor_radius=0.008)
rw = bpy.context.object; rw.parent = piv
rw.data.materials.append(M.emisja("Rownik", M.KOLOR["white"], 1.5))

cam, cel = M.kamera((0, -15.5, 6.2), (0, 0, 0), ogniskowa=30, sledz=False)
cam.rotation_mode = "QUATERNION"
M.poswiata(rozmiar=8, prog=1.2, mix=0.1)

# ── animacja klatka po klatce ──
for f in range(1, N + 1):
    t = (f - 1) / max(1, N - 1)
    kat = math.pi + math.pi * M.wygladz((t - 0.05) / 0.45) + 0.25 * t   # lipiec → styczeń
    p = pozycja(kat)
    piv.location = p
    piv.keyframe_insert("location", frame=f)
    ziemia.rotation_euler = (0, 0, 2 * math.pi * 1.6 * t * (N / FPS) / 10)
    ziemia.keyframe_insert("rotation_euler", frame=f)
    # kamera: plan ogólny obrócony o 90° (orbita stoi pionowo i mieści się w kadrze 9:16:
    # lipiec u góry, styczeń na dole) → w końcówce zbliżenie na Ziemię i powrót do poziomu (widać nachylenie osi)
    z = M.wygladz((t - 0.75) / 0.2)
    ogolny = Vector((0.6 * math.sin(t * 1.3), -15.8, 11.8))
    blisko = p + Vector((0.6, -4.2, 1.1))
    cam.location = ogolny.lerp(blisko, z)
    cel_p = Vector((0, 0, 0)).lerp(p, z)
    kier = cel_p - cam.location
    q = kier.to_track_quat("-Z", "Y")
    przechyl = math.radians(90 + 4 * math.sin(t * 2.0)) * (1 - z)
    cam.rotation_quaternion = q @ Quaternion((0, 0, 1), przechyl)
    cam.keyframe_insert("rotation_quaternion", frame=f)
    cam.keyframe_insert("location", frame=f)
    orb.data.bevel_depth = 0.012 - 0.008 * z          # w zbliżeniu orbita cieńsza, nie zasłania Ziemi
    orb.data.keyframe_insert("bevel_depth", frame=f)
for ob in (piv, ziemia, cam):
    for fc in ob.animation_data.action.fcurves:
        for k in fc.keyframe_points:
            k.interpolation = "LINEAR"

M.renderuj(o)
