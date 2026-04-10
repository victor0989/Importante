# -*- coding:utf-8 -*-
# Macro FreeCAD: Detallado del cuerpo (sin paneles, sin cortes)
# - Aplica escala global
# - Crea fuselaje y añade bulkheads, stringers, refuerzos, marcos de acceso y portholes (todos sólidos)
# - Intenta fusionar en "Body_Detailed"
# =============================================================================

import FreeCAD as App, Part, math

doc = App.newDocument("Nave_DFD_Body_Detailed")

# Parámetros base (usa tu diccionario original pero reduciendo elementos innecesarios)
P = {
    'scale': 2.0,

    'nose_len': 1500.0, 'nose_base_d': 1100.0,
    'mid_len': 3000.0, 'mid_d': 1800.0,
    'rear_len': 1500.0, 'rear_d': 2200.0,

    'collar_d_delta': 300.0, 'collar_h': 120.0,

    'shield_d': 2600.0, 't_ceramic': 4.0, 't_foam': 120.0, 't_cc': 12.0,

    # detalles estructurales
    'bulkhead_count': 8, 'bulkhead_th': 60.0,
    'stringer_count': 12, 'stringer_r': 40.0,
    'longeron_count': 6, 'longeron_w': 80.0, 'longeron_th': 40.0,

    'engine_boss_r': 250.0, 'engine_boss_h': 200.0,
    'access_frame_l': 700.0, 'access_frame_w': 400.0, 'access_frame_th': 40.0,

    'porthole_r': 80.0, 'porthole_count': 6,

    'chamfer_block_size': 200.0,
}

# Aplicar escala a valores numéricos (excepto conteos)
for k, v in list(P.items()):
    if k == 'scale': continue
    if 'count' in k: continue
    if isinstance(v, (int, float)):
        P[k] = v * P['scale']

# utilidad
def add_obj(shape, name):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    return obj

# 1) Fuselaje principal: nariz, medio, cola (sólidos)
nose = Part.makeCone(0, P['nose_base_d']/2.0, P['nose_len'])
mid = Part.makeCylinder(P['mid_d']/2.0, P['mid_len'])
mid.translate(App.Vector(0, 0, P['nose_len']))
rear = Part.makeCone(P['rear_d']/2.0, P['mid_d']/2.0, P['rear_len'])
rear.translate(App.Vector(0, 0, P['nose_len'] + P['mid_len']))

hull = nose.fuse(mid).fuse(rear)
add_obj(hull, "Hull")

# 2) TPS frontal (sólido)
shield_R = P['shield_d'] / 2.0
tps = Part.makeCylinder(shield_R, P['t_ceramic'] + P['t_foam'] + P['t_cc'])
tps.translate(App.Vector(0,0,-(P['t_ceramic'] + P['t_foam'] + P['t_cc'])))
add_obj(tps, "TPS_Shield")

# 3) Collar (sólido)
collarOD = P['mid_d'] + P['collar_d_delta']
collar = Part.makeCylinder(collarOD/2.0, P['collar_h'])
collar.translate(App.Vector(0,0,P['nose_len'] + P['mid_len']/2.0 - P['collar_h']/2.0))
add_obj(collar, "Collar")

# 4) Bulkheads (anillos sólidos a lo largo del fuselaje para rigidez)
for i in range(int(P['bulkhead_count'])):
    z = P['nose_len'] + i * ( (P['mid_len'] + P['rear_len']) / max(1, (P['bulkhead_count']-1)) ) - 100.0
    # crear un "anillo" como cilindro de pequeño espesor (no hueco)
    bh_r = P['mid_d']/2.0 + 40.0 + (i * 5.0)  # variación pequeña
    bh = Part.makeCylinder(bh_r, P['bulkhead_th'])
    bh.translate(App.Vector(0,0,z))
    add_obj(bh, f"Bulkhead_{i}")

# 5) Longitudinal stringers (cylinders alineados a lo largo del fuselaje)
for i in range(int(P['stringer_count'])):
    ang = i * (360.0 / P['stringer_count'])
    # posición inicial y final a lo largo del fuselaje
    start_z = 0.0
    end_z = P['nose_len'] + P['mid_len'] + P['rear_len']
    # colocar una serie de pequeños cilindros concatenados para aproximar un stringer curvo
    segments = 6
    for s in range(segments):
        seg_len = (end_z - start_z) / segments
        # radio a lo largo del stringer (aprox en la circunferencia del mid_d)
        r = P['mid_d']/2.0 + 30.0
        cx = r * math.cos(math.radians(ang))
        cy = r * math.sin(math.radians(ang))
        cz = start_z + s * seg_len
        seg = Part.makeCylinder(P['stringer_r'], seg_len)
        seg.translate(App.Vector(cx, cy, cz))
        add_obj(seg, f"Stringer_{i}_seg_{s}")

# 6) Longeron-placas: placas rectangulares curvadas aproximadas (boxes colocadas tangencialmente)
for i in range(int(P['longeron_count'])):
    ang = i * (360.0 / P['longeron_count'])
    r = P['mid_d']/2.0 + P['longeron_th']/2.0 + 20.0
    lx = P['longeron_w']
    lz = P['nose_len'] + P['mid_len'] + P['rear_len']
    plate = Part.makeBox(lx, P['longeron_th'], lz)
    # centrar la placa respecto a su espesor y girarla
    plate.translate(App.Vector(-lx/2.0, -P['longeron_th']/2.0, 0))
    plate.Placement = App.Placement(App.Vector(r * math.cos(math.radians(ang)),
                                              r * math.sin(math.radians(ang)),
                                              0),
                                    App.Rotation(App.Vector(0,0,1), ang))
    add_obj(plate, f"Longeron_Plate_{i}")

# 7) Refuerzos de motor (bosses) en la cola (sólidos)
for i in range(3):
    ang = i * (360.0 / 3)
    r = (P['rear_d']/2.0) - 200.0
    bx = r * math.cos(math.radians(ang))
    by = r * math.sin(math.radians(ang))
    bz = P['nose_len'] + P['mid_len'] + P['rear_len'] - P['engine_boss_h']/2.0 - 50.0
    boss = Part.makeCylinder(P['engine_boss_r'], P['engine_boss_h'])
    boss.translate(App.Vector(bx, by, bz))
    add_obj(boss, f"Engine_Boss_{i}")

# 8) Marco de acceso (sólido elevado, sin cortar hull)
# Colocado en el lateral superior del fuselaje
af = Part.makeBox(P['access_frame_l'], P['access_frame_th'], P['access_frame_w'])
# ubicar en la parte media superior
af.translate(App.Vector(-P['access_frame_l']/2.0, P['mid_d']/2.0 + 10.0, P['nose_len'] + P['mid_len']/2.0 - P['access_frame_w']/2.0))
add_obj(af, "Access_Frame")

# 9) Portholes decorativos (pequeñas cúpulas sólidas, no agujereadas)
for i in range(int(P['porthole_count'])):
    ang = i * (360.0 / P['porthole_count'])
    r = P['mid_d']/2.0 + 10.0
    x = r * math.cos(math.radians(ang))
    y = r * math.sin(math.radians(ang))
    z = P['nose_len'] + P['mid_len']/2.0 + ( (i%2) * 80.0 - 40.0 )
    dome = Part.makeSphere(P['porthole_r'])
    dome.translate(App.Vector(x, y, z))
    add_obj(dome, f"Porthole_Dome_{i}")

# 10) Chaflanes aproximados en la unión nariz-base (pequeños bloques biselados)
cb = P['chamfer_block_size']
for i in range(4):
    ang = i * 90
    cx = (P['nose_base_d']/4.0) * math.cos(math.radians(ang))
    cy = (P['nose_base_d']/4.0) * math.sin(math.radians(ang))
    ch = Part.makeBox(cb, cb/2.0, cb/2.0)
    ch.translate(App.Vector(cx - cb/2.0, cy - cb/4.0, P['nose_len'] - cb/2.0))
    ch.Placement = App.Placement(App.Vector(cx, cy, P['nose_len'] - cb/2.0),
                                 App.Rotation(App.Vector(0,0,1), ang))
    add_obj(ch, f"Chamfer_Block_{i}")

# 11) Intenta fusionar los elementos principales en un solo sólido para cuerpo CNC
# Selección de piezas a fusionar (hull + collar + tps + bulkheads + stringers + longerons + bosses + access frame)
# Recolectar shapes
shapes_to_fuse = []
names_to_collect_prefix = ["Hull","Collar","TPS_Shield","Bulkhead_","Stringer_","Longeron_Plate_","Engine_Boss_","Access_Frame","Porthole_Dome_","Chamfer_Block_"]
for o in doc.Objects:
    if any(o.Name.startswith(pref) for pref in names_to_collect_prefix):
        shapes_to_fuse.append(o.Shape)

try:
    if shapes_to_fuse:
        main = shapes_to_fuse[0]
        for s in shapes_to_fuse[1:]:
            main = main.fuse(s)
        add_obj(main, "Body_Detailed")
except Exception as e:
    App.Console.PrintMessage("Fusión de Body_Detailed fallida (operación pesada). Mantener piezas individuales.\n")

doc.recompute()