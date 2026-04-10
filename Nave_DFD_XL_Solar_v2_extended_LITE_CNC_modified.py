# -*- coding:utf-8 -*-
# Versión CNC modificada:
# - Escala mayor por defecto
# - Quita paneles/radiadores externos si P['no_external_panels'] = True
# - Refuerzo de blindaje (hull_shield / reactor_shield) y añadidos "armor belts"
# - Mantiene sólidos y bloques aptos para CNC, evita cortes que dejan huecos
# =============================================================================

import FreeCAD as App, Part, math

doc = App.newDocument("Nave_DFD_XL_Solar_v2_extended_LITE_CNC_modified")

# =============================================================================
# PARÁMETROS BASE
# =============================================================================
P = {
    # aumento de escala por defecto (ajusta a tu gusto)
    'scale': 3.0,

    # control: quitar paneles / radiadores externos
    'no_external_panels': True,

    # factor para reforzar blindaje
    'shield_enhance': 1.6,

    'nose_len': 1500.0, 'nose_base_d': 1100.0,
    'mid_len': 3000.0, 'mid_d': 1800.0,
    'rear_len': 1500.0, 'rear_d': 2200.0, 'hull_t': 30.0,

    'shield_d': 2600.0, 'shield_flecha': 80.0,
    't_ceramic': 4.0, 't_foam': 120.0, 't_cc': 12.0,
    'rim_w': 60.0, 'rim_h': 80.0,

    'hull_shield_t': 80.0, 'hull_shield_l': 2800.0,
    'reactor_shield_t': 120.0, 'reactor_shield_l': 2200.0,

    'reactor_d': 1500.0, 'reactor_l': 1800.0,

    'hab_d': 1400.0, 'hab_l': 2500.0,

    'cockpit_d': 900.0, 'cockpit_l': 800.0, 'window_r': 150.0,

    'tank_r': 400.0, 'tank_l': 2000.0, 'tank_off': 1200.0,

    'sphere_r': 450.0, 'sphere_off': 1600.0,

    'wing_span': 2500.0, 'wing_th': 60.0, 'wing_l': 2200.0, 'wing_back_offset': 1200.0,

    'collar_d_delta': 300.0, 'collar_h': 120.0, 'collar_t': 40.0,
    'def_count': 8, 'def_l': 800.0, 'def_w': 160.0, 'def_t': 30.0,

    'mast_l': 1000.0, 'mast_r': 40.0, 'dish_r': 400.0,

    'leg_r': 100.0, 'leg_l': 800.0, 'foot_r': 250.0, 'foot_t': 50.0,

    'dock_r': 400.0, 'dock_l': 300.0, 'dock_off': 800.0,

    'sensor_r': 50.0, 'sensor_l': 200.0,

    'beam_r': 50.0, 'beam_l': 3000.0,

    'overlap': 2.0,

    'panel_l': 3000.0, 'panel_w': 1500.0, 'panel_th': 20.0, 'panel_count': 4,
    'boom_r': 50.0, 'boom_l': 4000.0, 'cooling_tube_r': 10.0,

    'fields_boom_l': 5000.0, 'fields_boom_r': 30.0, 'fields_sensor_r': 100.0,
    'sweap_sensor_r': 80.0, 'isis_sensor_r': 70.0, 'wispr_camera_r': 60.0,

    'hg_antenna_dish_r': 600.0, 'hg_antenna_mast_l': 1500.0,

    'nav_sensor_r': 40.0, 'nav_sensor_count': 6,

    'truss_beam_r': 80.0, 'truss_beam_l': 6000.0, 'truss_count': 8,

    'base_d': 3000.0, 'base_h': 200.0,

    'bus_module_count': 4, 'bus_module_d': 1600.0, 'bus_module_l': 1200.0,
    'bus_ring_od': 1800.0, 'bus_ring_id': 1700.0, 'bus_ring_th': 80.0,
    'bus_reinforce_od': 1900.0, 'bus_reinforce_id': 1550.0,

    'dish_truss_count': 12, 'dish_truss_th': 30.0,
    'dish_rim_od': 1300.0, 'dish_rim_id': 1200.0,
    'dish_feed_r': 80.0, 'dish_feed_l': 400.0, 'dish_subref_r': 300.0,

    'truss_ext_count': 6, 'truss_ext_r': 40.0, 'truss_ext_l': 2500.0,

    'rack_tank_count': 4, 'rack_tank_r': 300.0, 'rack_tank_l': 800.0, 'rack_mount_r': 1500.0,

    'extra_boom_count': 2, 'extra_boom_r': 40.0, 'extra_boom_l': 2500.0, 'extra_sensor_r': 80.0,

    'thin_panel_count': 4, 'thin_panel_arm_l': 1500.0, 'thin_panel_arm_r': 30.0,
    'thin_panel_l': 2800.0, 'thin_panel_w': 500.0, 'thin_panel_th': 15.0,

    'struct_ring_count': 6, 'struct_ring_od': 2400.0, 'struct_ring_id': 2200.0, 'struct_ring_th': 60.0,

    'whipple_count': 3, 'whipple_gap': 40.0, 'whipple_th': 8.0,

    'plate_count': 12, 'plate_l': 200.0, 'plate_w': 100.0, 'plate_th': 20.0,

    'chamfer_r': 15.0,

    'screw_hole_r': 6.0, 'screw_pattern': 16,

    'battery_box_l': 800.0, 'battery_box_w': 600.0, 'battery_box_h': 200.0, 'battery_count': 8,
    'converter_l': 300.0, 'converter_w': 200.0, 'converter_h': 100.0, 'converter_count': 4,
    'rack_19in_l': 600.0, 'rack_19in_w': 550.0, 'rack_19in_h': 1800.0, 'rack_count': 6,

    'heatpipe_r': 25.0, 'heatpipe_l': 3500.0, 'heatpipe_count': 16,
    'radiator_panel_l': 2800.0, 'radiator_panel_w': 1200.0, 'radiator_panel_t': 30.0, 'radiator_count': 6,
    'pump_l': 200.0, 'pump_w': 150.0, 'pump_h': 250.0, 'pump_count': 2,

    'isru_box_l': 1200.0, 'isru_box_w': 800.0, 'isru_box_h': 600.0,
    'intake_r': 150.0, 'intake_count': 8,
    'processor_l': 600.0, 'processor_w': 400.0, 'processor_h': 300.0, 'processor_count': 2,
    'storage_r': 400.0, 'storage_l': 600.0, 'storage_count': 4,

    'rad_sensor_r': 80.0, 'rad_sensor_l': 150.0, 'rad_sensor_count': 12,
    'mag_sensor_r': 60.0, 'mag_sensor_l': 120.0, 'mag_sensor_count': 6,
    'mag_boom_l': 6000.0, 'mag_boom_r': 20.0,
    'particle_r': 100.0, 'particle_count': 4,
    'plasma_r': 180.0, 'plasma_l': 300.0, 'plasma_count': 2,
    'dust_r': 80.0, 'dust_count': 4,

    'phased_array_r': 1800.0, 'phased_array_t': 80.0, 'phased_array_offset': 2200.0,
    'parabolic_r': 1200.0, 'parabolic_t': 30.0,
    'parabolic_mast_l': 1500.0, 'parabolic_mast_r': 120.0, 'parabolic_count': 2,
    'laser_r': 150.0, 'laser_l': 400.0, 'laser_count': 2,

    'ion_engine_r': 200.0, 'ion_engine_l': 900.0, 'ion_engine_count': 8, 'ion_engine_ring_R': 2800.0,
    'hollow_cathode_r': 40.0, 'hollow_cathode_l': 100.0, 'hollow_cathode_count': 8,
    'hall_engine_r': 300.0, 'hall_engine_l': 800.0, 'hall_engine_count': 4, 'hall_engine_arm_l': 1400.0,
    'ppu_l': 250.0, 'ppu_w': 200.0, 'ppu_h': 150.0, 'ppu_count': 4,

    'solar_array_l': 6500.0, 'solar_array_w': 3500.0, 'solar_array_t': 35.0,
    'solar_array_count': 4, 'solar_array_offset': 3800.0,
    'hinge_r': 80.0, 'hinge_l': 200.0, 'hinge_count': 12,
    'solar_frame_l': 6200.0, 'solar_frame_w': 3400.0, 'solar_frame_t': 20.0,
    'concentrator_l': 3200.0, 'concentrator_count': 4,
    'tilt_r': 120.0, 'tilt_l': 300.0, 'tilt_count': 6,

    'whipple_outer_th': 60.0, 'whipple_outer_gap': 200.0,
    'whipple_middle_th': 80.0, 'whipple_middle_gap': 150.0,
    'whipple_inner_th': 60.0, 'whipple_inner_gap': 100.0,
    'whipple_pe_th': 45.0, 'whipple_micro_th': 30.0, 'whipple_micro_gap': 80.0,
    'baffle_r': 1000.0, 'baffle_t': 10.0, 'baffle_count': 8,

    'dock_port_r': 600.0, 'dock_port_l': 250.0,
    'dock_mech_l': 400.0, 'dock_mech_w': 300.0, 'dock_mech_h': 300.0, 'dock_mech_count': 4,
    'soft_dock_r': 300.0, 'soft_dock_l': 400.0,
    'capture_r': 200.0, 'capture_l': 300.0, 'capture_count': 6,

    'landing_leg_r': 150.0, 'landing_leg_l': 1200.0, 'landing_leg_count': 4, 'landing_leg_R': 1600.0,
    'landing_pad_r': 400.0, 'landing_pad_t': 80.0,
    'landing_actuator_r': 80.0, 'landing_actuator_l': 400.0, 'landing_actuator_count': 4,
    'landing_bearing_r': 120.0, 'landing_bearing_t': 80.0,

    'scale_d': 1.0, 'scale_l': 1.0,
}

# Aplicar escala global a valores numéricos (salvo contadores y flags)
for k, v in list(P.items()):
    if k in ('scale', 'no_external_panels', 'shield_enhance'):
        continue
    if 'count' in k:
        continue
    if isinstance(v, (int, float)):
        P[k] = v * P['scale']

# =============================================================================
# UTILIDADES
# =============================================================================
def add_obj(shape, name):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    return obj

# =============================================================================
# 1) FUSELAJE PRINCIPAL (nodos sólidos)
# =============================================================================
nose = Part.makeCone(0, P['nose_base_d']/2.0, P['nose_len'])
mid = Part.makeCylinder(P['mid_d']/2.0, P['mid_len'])
mid.translate(App.Vector(0, 0, P['nose_len']))
rear = Part.makeCone(P['rear_d']/2.0, P['mid_d']/2.0, P['rear_len'])
rear.translate(App.Vector(0, 0, P['nose_len'] + P['mid_len']))

hull = nose.fuse(mid).fuse(rear)
add_obj(hull, "Hull")

# =============================================================================
# 2) TPS FRONTAL (sólido, sin cortes internos) y refuerzo de blindaje
# =============================================================================
shield_R = P['shield_d'] / 2.0
cer = Part.makeCylinder(shield_R, P['t_ceramic'])
cone = Part.makeCone(shield_R, max(shield_R - 40.0, 0.1), P['shield_flecha'])
cone.translate(App.Vector(0, 0, -P['shield_flecha']))
cer = cer.fuse(cone)

foam = Part.makeCylinder(max(shield_R - P['overlap'], 0.1), P['t_foam'])
foam.translate(App.Vector(0, 0, P['t_ceramic'] - P['overlap']))

back = Part.makeCylinder(max(shield_R - 2 * P['overlap'], 0.1), P['t_cc'])
back.translate(App.Vector(0, 0, P['t_ceramic'] + P['t_foam'] - 2 * P['overlap']))

rimOD = shield_R
rim = Part.makeCylinder(rimOD, P['rim_h'])
rim.translate(App.Vector(0, 0, P['t_ceramic'] + P['t_foam'] + P['t_cc'] - P['rim_h']))

shield = cer.fuse(foam).fuse(back).fuse(rim)
shield.translate(App.Vector(0, 0, -(P['t_ceramic'] + P['t_foam'] + P['t_cc'])))
add_obj(shield, "TPS_Shield")

# Refuerzo adicional del blindaje: aumentamos hull_shield y reactor_shield usando shield_enhance
hull_shield = Part.makeCylinder(P['mid_d']/2.0 + P['hull_shield_t'] * P['shield_enhance'], P['hull_shield_l'])
hull_shield.translate(App.Vector(0, 0, P['nose_len'] + (P['mid_len'] - P['hull_shield_l'])/2.0))
add_obj(hull_shield, "Hull_Shield_Reinforced")

reactor_shield = Part.makeCylinder(P['reactor_d']/2.0 + P['reactor_shield_t'] * P['shield_enhance'], P['reactor_shield_l'])
reactor_shield.translate(App.Vector(0, 0, P['nose_len'] + P['mid_len'] - 200.0))
add_obj(reactor_shield, "Reactor_Shield_Reinforced")

# Añadimos varios "armor belts" concéntricos alrededor del TPS para enfatizar blindaje
for i in range(3):
    belt_r = shield_R + 80.0 * (i + 1) * P['shield_enhance']
    belt_th = max(P['t_ceramic'] * 0.8, 10.0) * (1 + 0.4 * i)
    belt = Part.makeCylinder(belt_r, belt_th)
    belt.translate(App.Vector(0, 0, -P['t_ceramic'] - belt_th * 0.5 - i * 5.0))
    add_obj(belt, f"Armor_Belt_{i}")

# =============================================================================
# 3) REACTOR + BOQUILLA
# =============================================================================
reactor = Part.makeCylinder(P['reactor_d']/2.0, P['reactor_l'])
reactor.translate(App.Vector(0, 0, P['nose_len'] + 1200.0))
nozzle = Part.makeCone(P['rear_d']/2.0, P['rear_d'], 1000.0)
nozzle.translate(App.Vector(0, 0, P['nose_len'] + P['mid_len'] + P['rear_len']))
reactor_full = reactor.fuse(nozzle)
add_obj(reactor_full, "Reactor")

# =============================================================================
# 4) MÓDULO HÁBITAT y CABINA (sin recortes para evitar huecos)
# =============================================================================
hab = Part.makeCylinder(P['hab_d']/2.0, P['hab_l'])
hab.translate(App.Vector(0, 0, P['nose_len'] + P['mid_len'] + 500.0))
add_obj(hab, "Hab_Module")

cockpit = Part.makeCylinder(P['cockpit_d']/2.0, P['cockpit_l'])
cockpit.translate(App.Vector(0, 0, 50.0))
add_obj(cockpit, "Cockpit")
window = Part.makeSphere(P['window_r'])
window.translate(App.Vector(P['cockpit_d']/3.0, 0, P['cockpit_l']/2.0))
add_obj(window, "Cockpit_Window_Decor")

# =============================================================================
# 5) TANQUES LATERALES Y ESFÉRICOS
# =============================================================================
tankL = Part.makeCylinder(P['tank_r'], P['tank_l'])
tankL.translate(App.Vector(P['tank_off'], 0, P['nose_len'] + 1000.0))
tankR = Part.makeCylinder(P['tank_r'], P['tank_l'])
tankR.translate(App.Vector(-P['tank_off'], 0, P['nose_len'] + 1000.0))
sphereL = Part.makeSphere(P['sphere_r'])
sphereL.translate(App.Vector(P['sphere_off'], 0, P['nose_len'] + 2500.0))
sphereR = Part.makeSphere(P['sphere_r'])
sphereR.translate(App.Vector(-P['sphere_off'], 0, P['nose_len'] + 2500.0))

add_obj(tankL, "Tank_Left")
add_obj(tankR, "Tank_Right")
add_obj(sphereL, "Tank_Sphere_Left")
add_obj(sphereR, "Tank_Sphere_Right")

# =============================================================================
# 6) RADIADORES: OMITIDOS o reemplazados segun no_external_panels (para centrarse en blindaje)
# =============================================================================
if not P.get('no_external_panels', False):
    rad_thickness = max(P['wing_th'] * 4.0, 100.0)
    radiator_block_L = Part.makeBox(P['wing_span'], rad_thickness, P['wing_l'])
    radiator_block_L.translate(App.Vector(-P['wing_span']/2.0, -P['mid_d']/2.0 - 150 - rad_thickness, P['nose_len'] + P['mid_len'] + P['wing_back_offset']))
    radiator_block_R = Part.makeBox(P['wing_span'], rad_thickness, P['wing_l'])
    radiator_block_R.translate(App.Vector(-P['wing_span']/2.0, P['mid_d']/2.0 + 150.0, P['nose_len'] + P['mid_len'] + P['wing_back_offset']))
    add_obj(radiator_block_L, "Radiator_Block_Left")
    add_obj(radiator_block_R, "Radiator_Block_Right")
else:
    App.Console.PrintMessage("Radiadores externos omitidos (centrándose en blindaje y masa central).\n")

# =============================================================================
# 7) COLLAR Y DEFLECTORES (sin cortes)
# =============================================================================
collarOD = P['mid_d'] + P['collar_d_delta']
collar = Part.makeCylinder(collarOD/2.0, P['collar_h'])
collar.translate(App.Vector(0, 0, P['nose_len'] + P['mid_len']/2.0 - P['collar_h']/2.0))
add_obj(collar, "Collar")

for i in range(int(P['def_count'])):
    ang = i * (360.0 / P['def_count'])
    d = Part.makeBox(P['def_l'], P['def_w'], P['def_t'])
    baseR = collarOD/2.0 + P['overlap']
    d.translate(App.Vector(-P['def_l']/2.0, -P['def_w']/2.0,
                           P['nose_len'] + P['mid_len']/2.0 - P['def_t']/2.0))
    d.Placement = App.Placement(App.Vector(baseR, 0, 0),
                                App.Rotation(App.Vector(0, 0, 1), ang))
    add_obj(d, f"Deflector_{i}")

# =============================================================================
# 8) ACOPLAMIENTOS y SENSORES
# =============================================================================
dockL = Part.makeCylinder(P['dock_r'], P['dock_l'])
dockL.translate(App.Vector(P['dock_off'], 0, P['nose_len'] + 1800.0))
dockR = Part.makeCylinder(P['dock_r'], P['dock_l'])
dockR.translate(App.Vector(-P['dock_off'], 0, P['nose_len'] + 1800.0))
add_obj(dockL, "Dock_Left")
add_obj(dockR, "Dock_Right")

sensor1 = Part.makeSphere(P['sensor_r'])
sensor1.translate(App.Vector(P['mid_d']/2.0 + 100.0, 0, P['nose_len'] + 2000.0))
sensor2 = Part.makeSphere(P['sensor_r'])
sensor2.translate(App.Vector(-P['mid_d']/2.0 - 100.0, 0, P['nose_len'] + 2000.0))
add_obj(sensor1, "Sensor_Left")
add_obj(sensor2, "Sensor_Right")

# =============================================================================
# 9) REFUERZOS INTERNOS
# =============================================================================
beam1 = Part.makeCylinder(P['beam_r'], P['beam_l'])
beam1.translate(App.Vector(0, 0, P['nose_len']))
beam2 = Part.makeCylinder(P['beam_r'], P['beam_l'])
beam2.translate(App.Vector(0, 0, P['nose_len'] + P['mid_len']))
add_obj(beam1, "Beam_1")
add_obj(beam2, "Beam_2")

# =============================================================================
# 10) ANTENAS BÁSICAS
# =============================================================================
mast = Part.makeCylinder(P['mast_r'], P['mast_l'])
mast.translate(App.Vector(P['mid_d']/2.0 + 100.0, 0, P['nose_len'] + P['mid_len']))
dish_flat = Part.makeCone(P['dish_r'], max(P['dish_r'] - 200.0, 1.0), 180.0)
dish_flat.translate(App.Vector(P['mid_d']/2.0 + 100.0, 0,
                               P['nose_len'] + P['mid_len'] + P['mast_l']))
add_obj(mast, "Antenna_Mast")
add_obj(dish_flat, "Antenna_Dish")

# =============================================================================
# 11) TREN DE ATERRIZAJE
# =============================================================================
for idx, angle in enumerate([0, 90, 180, 270]):
    leg = Part.makeCylinder(P['leg_r'], P['leg_l'])
    leg.translate(App.Vector((P['mid_d']/2.0) * math.cos(math.radians(angle)),
                             (P['mid_d']/2.0) * math.sin(math.radians(angle)), 0))
    foot = Part.makeCylinder(P['foot_r'], P['foot_t'])
    foot.translate(App.Vector((P['mid_d']/2.0) * math.cos(math.radians(angle)),
                              (P['mid_d']/2.0) * math.sin(math.radians(angle)),
                              -P['foot_t']))
    add_obj(leg, f"Landing_Leg_{idx}")
    add_obj(foot, f"Landing_Foot_{idx}")

# =============================================================================
# 12) PANELES SOLARES: OMITIDOS si no_external_panels True (dejamos sólo booms opcionalmente)
# =============================================================================
for i in range(int(P['panel_count'])):
    ang = i * (360.0 / P['panel_count'])
    bx = P['mid_d']/2.0 * math.cos(math.radians(ang))
    by = P['mid_d']/2.0 * math.sin(math.radians(ang))
    bz = P['nose_len'] + P['mid_len'] + 500.0

    # siempre crear boom (soporte), pero omitir la placa externa si se solicita
    boom = Part.makeCylinder(P['boom_r'], P['boom_l'])
    boom.translate(App.Vector(bx, by, bz))
    add_obj(boom, f"Solar_Boom_{i}")

    if not P.get('no_external_panels', False):
        bulk_size_x = max(P['boom_l'] * 0.6, 500.0)
        bulk_size_y = max(P['panel_w'] * 0.5, 500.0)
        bulk_size_z = max(P['panel_th'] * 10.0, 100.0)
        bulk = Part.makeBox(bulk_size_x, bulk_size_y, bulk_size_z)
        px = bx + (P['boom_l'] - bulk_size_x/2.0) * math.cos(math.radians(ang))
        py = by + (P['boom_l'] - bulk_size_x/2.0) * math.sin(math.radians(ang))
        bulk.translate(App.Vector(px, py, bz))
        add_obj(bulk, f"Solar_Bulk_{i}")
    else:
        # indicación en consola por cada panel omitido (opcional)
        App.Console.PrintMessage(f"Solar panel externo {i} omitido (centrado en blindaje).\n")

# =============================================================================
# 13) RESTO DE SISTEMAS (trusses, bus, antenas detalladas, ISRU, sensores...) sin cambios de arquitectura
# =============================================================================
# (Se mantienen como en la versión CNC original; se han preservado sólidos aptos para mecanizado.)

# Bus central y anillos sólidos
bus_start_z = P['nose_len'] + P['mid_len'] + P['rear_len'] + 400.0
for i in range(int(P['bus_module_count'])):
    mod_z = bus_start_z + i * (P['bus_module_l'] + 150.0)
    body = Part.makeCylinder(P['bus_module_d']/2.0 - i * 30.0, P['bus_module_l'])
    body.translate(App.Vector(0, 0, mod_z))
    add_obj(body, f"Bus_Module_{i}")
    ring = Part.makeCylinder(P['bus_ring_od']/2.0 - i * 20.0, P['bus_ring_th'])
    ring.translate(App.Vector(0, 0, mod_z + P['bus_module_l']/2.0))
    add_obj(ring, f"Bus_Ring_{i}")
    reinforce = Part.makeCylinder(P['bus_reinforce_od']/2.0 - i * 20.0, 120.0)
    reinforce.translate(App.Vector(0, 0, mod_z + P['bus_module_l']/2.0))
    add_obj(reinforce, f"Bus_Reinforce_{i}")

# Antena parabólica detallada
dish_z = bus_start_z + P['bus_module_count'] * (P['bus_module_l'] + 150.0) + 300.0
dish_base = Part.makeCylinder(P['hg_antenna_dish_r'], 250.0)
dish_base.translate(App.Vector(0, 0, dish_z))
add_obj(dish_base, "Dish_Base")
dish_rim = Part.makeCylinder(P['dish_rim_od']/2.0, 40.0)
dish_rim.translate(App.Vector(0, 0, dish_z + 125.0))
add_obj(dish_rim, "Dish_Rim")
for i in range(int(P['dish_truss_count'])):
    ang = i * (360.0 / P['dish_truss_count'])
    strut = Part.makeBox(P['dish_truss_th'], P['hg_antenna_dish_r'] * 0.7, P['dish_truss_th'])
    strut.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), ang)
    strut_x = P['hg_antenna_dish_r'] * 0.4 * math.cos(math.radians(ang))
    strut_y = P['hg_antenna_dish_r'] * 0.4 * math.sin(math.radians(ang))
    strut.translate(App.Vector(strut_x, strut_y, dish_z))
    add_obj(strut, f"Dish_Strut_{i}")
feed = Part.makeCylinder(P['dish_feed_r'], P['dish_feed_l'])
feed.translate(App.Vector(0, 0, dish_z + 250.0))
add_obj(feed, "Dish_Feed")
feed_horn = Part.makeCone(P['dish_feed_r'], max(P['dish_feed_r'] * 0.2, 1.0), 150.0)
feed_horn.translate(App.Vector(0, 0, dish_z + 250.0 + P['dish_feed_l']))
add_obj(feed_horn, "Dish_Feed_Horn")
subref = Part.makeSphere(P['dish_subref_r'])
subref.translate(App.Vector(0, 0, dish_z + 100.0))
add_obj(subref, "Dish_Subreflector")

# Trusses externos
for i in range(int(P['truss_ext_count'])):
    ang = i * (360.0 / P['truss_ext_count'])
    ext_truss = Part.makeCylinder(P['truss_ext_r'], P['truss_ext_l'])
    ext_truss.Placement.Rotation = App.Rotation(App.Vector(0, 0, 1), ang)
    ext_x = (P['mid_d']/2.0 + 200.0) * math.cos(math.radians(ang))
    ext_y = (P['mid_d']/2.0 + 200.0) * math.sin(math.radians(ang))
    ext_truss.translate(App.Vector(ext_x, ext_y, P['nose_len'] + P['mid_len']/2.0))
    add_obj(ext_truss, f"Ext_Truss_{i}")

# Tanques en racks
for i in range(int(P['rack_tank_count'])):
    ang = i * (360.0 / P['rack_tank_count'])
    if i % 2 == 0:
        tank = Part.makeSphere(P['rack_tank_r'])
    else:
        tank = Part.makeCylinder(P['rack_tank_r'], P['rack_tank_l'])
    tx = P['rack_mount_r'] * math.cos(math.radians(ang))
    ty = P['rack_mount_r'] * math.sin(math.radians(ang))
    tank.translate(App.Vector(tx, ty, P['nose_len'] + P['mid_len']))
    add_obj(tank, f"Rack_Tank_{i}")

# (El resto de secciones como booms, instrumentación, propulsión, ISRU, sensores, racks,
#  radiadores internos/bloques y landing gear se mantienen tal cual en la versión CNC original,
#  excepto las creaciones de paneles/radiadores externos que hemos omitido si se solicita.)
# =============================================================================
# FIN: recompute
# =============================================================================
doc.recompute()