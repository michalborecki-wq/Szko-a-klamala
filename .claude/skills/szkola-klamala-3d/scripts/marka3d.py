"""Wspólne elementy scen 3D „Szkoła kłamała” (uruchamiane wewnątrz Blendera).

Paleta marki, tło z gwiazdami, materiały, kamera 9:16, ustawienia Cycles na CPU
(ta maszyna nie ma karty graficznej) i poświata w kompozytorze.
"""
import bpy, math, sys, os

KOLOR = {"bg0": "#0A0E18", "bg1": "#16203A", "blue": "#2F6BFF", "yellow": "#FFC727",
         "red": "#E53935", "white": "#F4F6FB"}


def rgb(hexs, a=1.0):
    h = hexs.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]   # sRGB → liniowe
    return (*lin, a)


def argumenty():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    o = {"out": "out3d", "sek": 10.0, "fps": 30, "szer": 1080, "probki": 24, "od": 0, "do": -1, "odszum": 0}
    for k, v in zip(a[::2], a[1::2]):
        k = k.lstrip("-")
        o[k] = type(o[k])(v) if k in o else v
    return o


def wyczysc():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def scena(o):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = o["probki"]
    sc.cycles.use_denoising = o.get("odszum", 0) == 1
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = 1
    sc.cycles.diffuse_bounces = 1
    sc.cycles.glossy_bounces = 1
    sc.cycles.transmission_bounces = 0
    sc.cycles.volume_bounces = 0
    sc.cycles.transparent_max_bounces = 2
    sc.cycles.use_adaptive_sampling = True
    sc.render.resolution_x = o["szer"]
    sc.render.resolution_y = round(o["szer"] * 16 / 9)
    sc.render.resolution_percentage = 100
    sc.render.fps = o["fps"]
    sc.frame_start = 1
    sc.frame_end = max(1, round(o["sek"] * o["fps"]))
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 94
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.render.film_transparent = False
    sc.render.threads_mode = "AUTO"
    sc.render.use_persistent_data = True     # scena budowana raz, nie co klatkę
    return sc


def tlo_gwiazdy(gestosc=420.0, jasnosc=2.2):
    """Granatowe tło z drobnymi gwiazdami (proceduralne, bez tekstur z zewnątrz)."""
    w = bpy.data.worlds.new("Tlo")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    n = nt.nodes
    n.clear()
    out = n.new("ShaderNodeOutputWorld")
    tc = n.new("ShaderNodeTexCoord")
    vor = n.new("ShaderNodeTexVoronoi")
    vor.feature = "F1"
    vor.inputs["Scale"].default_value = gestosc
    ramp = n.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp.color_ramp.elements[1].position = 0.035
    ramp.color_ramp.elements[1].color = (0, 0, 0, 1)
    noise = n.new("ShaderNodeTexNoise")          # nie wszystkie komórki świecą – rzadkie gwiazdy
    noise.inputs["Scale"].default_value = gestosc * 0.5
    nramp = n.new("ShaderNodeValToRGB")
    nramp.color_ramp.elements[0].position = 0.62
    nramp.color_ramp.elements[1].position = 0.70
    mul = n.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    mul2 = n.new("ShaderNodeMath"); mul2.operation = "MULTIPLY"; mul2.inputs[1].default_value = jasnosc
    grad = n.new("ShaderNodeMix"); grad.data_type = "RGBA"
    sep = n.new("ShaderNodeSeparateXYZ")
    grad.inputs[6].default_value = rgb(KOLOR["bg0"])
    grad.inputs[7].default_value = rgb(KOLOR["bg1"])
    add = n.new("ShaderNodeMix"); add.data_type = "RGBA"; add.blend_type = "ADD"
    add.inputs[0].default_value = 1.0
    bg = n.new("ShaderNodeBackground")
    L = nt.links.new
    L(tc.outputs["Generated"], vor.inputs["Vector"])
    L(tc.outputs["Generated"], noise.inputs["Vector"])
    L(vor.outputs["Distance"], ramp.inputs["Fac"])
    L(noise.outputs["Fac"], nramp.inputs["Fac"])
    L(ramp.outputs["Color"], mul.inputs[0])
    L(nramp.outputs["Color"], mul.inputs[1])
    L(mul.outputs[0], mul2.inputs[0])
    L(tc.outputs["Generated"], sep.inputs[0])
    L(sep.outputs["Z"], grad.inputs[0])
    L(grad.outputs[2], add.inputs[6])
    L(mul2.outputs[0], add.inputs[7])
    L(add.outputs[2], bg.inputs["Color"])
    L(bg.outputs[0], out.inputs[0])
    return w


def emisja(nazwa, kolor, moc):
    m = bpy.data.materials.new(nazwa)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.clear()
    e = n.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = rgb(kolor) if isinstance(kolor, str) else kolor
    e.inputs["Strength"].default_value = moc
    o = n.new("ShaderNodeOutputMaterial")
    m.node_tree.links.new(e.outputs[0], o.inputs[0])
    return m


def kamera(lok, cel, ogniskowa=35, sledz=True):
    bpy.ops.object.camera_add(location=lok)
    cam = bpy.context.object
    cam.data.lens = ogniskowa
    cam.data.sensor_fit = "VERTICAL"
    bpy.ops.object.empty_add(location=cel)
    tgt = bpy.context.object
    tgt.name = "CelKamery"
    if not sledz:
        bpy.context.scene.camera = cam
        return cam, tgt
    c = cam.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    bpy.context.scene.camera = cam
    return cam, tgt


def poswiata(rozmiar=8, prog=0.9, mix=0.15):
    """Poświata (Fog Glow) na jasnych elementach – jak w motion designie."""
    sc = bpy.context.scene
    sc.use_nodes = True
    nt = sc.node_tree
    for x in list(nt.nodes):
        nt.nodes.remove(x)
    rl = nt.nodes.new("CompositorNodeRLayers")
    gl = nt.nodes.new("CompositorNodeGlare")
    gl.glare_type = "FOG_GLOW"
    gl.quality = "HIGH"
    gl.size = rozmiar
    gl.threshold = prog
    gl.mix = mix
    co = nt.nodes.new("CompositorNodeComposite")
    nt.links.new(rl.outputs["Image"], gl.inputs["Image"])
    nt.links.new(gl.outputs["Image"], co.inputs["Image"])


def wygladz(t):
    """Łagodny start i koniec ruchu (0..1 → 0..1)."""
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def renderuj(o):
    sc = bpy.context.scene
    os.makedirs(o["out"], exist_ok=True)
    od = max(sc.frame_start, o["od"] or sc.frame_start)
    do = sc.frame_end if o["do"] < 0 else min(sc.frame_end, o["do"])
    for f in range(od, do + 1):
        path = os.path.join(o["out"], f"{f:05d}.jpg")
        if os.path.exists(path):          # wznawianie po restarcie kontenera
            continue
        sc.frame_set(f)
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
