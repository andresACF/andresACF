// Foldbot — Brazo DIY 4 DOF + pinza (modelo paramétrico de referencia)
// Objetivo Fase 0: validar proporciones, alcance y ubicación de servos.
// Render por pieza con: openscad -D 'part="link_l1"' -o out.stl arm.scad
// Partes válidas: "full", "link_l1", "link_l2", "link_l3", "gripper_finger"

include <params.scad>;

part = "full";   // sobrescribible con -D en línea de comandos

// ---------- Primitivas ----------

// Eslabón hueco tipo "hueso de perro" con dos ejes en los extremos.
module link(len, w = arm_link_w, t = arm_link_t) {
    hole_r = 2;  // agujero de eje/tornillo M4
    difference() {
        union() {
            // cuerpo
            hull() {
                translate([0, 0, 0]) cylinder(h = w, r = w/2);
                translate([len, 0, 0]) cylinder(h = w, r = w/2);
            }
        }
        // vaciado interior para aligerar
        translate([0, 0, t])
            hull() {
                translate([0, 0, 0]) cylinder(h = w, r = w/2 - t);
                translate([len, 0, 0]) cylinder(h = w, r = w/2 - t);
            }
        // ejes en los extremos
        translate([0, 0, -1])    cylinder(h = w + 2, r = hole_r);
        translate([len, 0, -1])  cylinder(h = w + 2, r = hole_r);
    }
}

// Caja de servo (para visualizar el hueco/posición).
module servo_box() {
    color("dimgray")
        cube([servo_len, servo_w, servo_h], center = false);
}

// Base rotatoria.
module base() {
    color("steelblue")
    difference() {
        cylinder(h = 12, r = arm_base_d/2);
        translate([0, 0, -1]) cylinder(h = 14, r = 3); // eje central
    }
}

// Dedo de pinza suave (imprimible, con ranuras para almohadilla).
module gripper_finger() {
    fw = 14; fl = 55; ft = 6;
    difference() {
        // cuerpo curvo
        hull() {
            cube([ft, fw, 4]);
            translate([2, 0, fl]) cube([ft, fw, 4]);
        }
        // ranuras para espuma/silicona (superficie de agarre)
        for (z = [12 : 10 : fl - 8])
            translate([-1, 2, z]) cube([2.5, fw - 4, 3]);
        // agujero de montaje al servo
        translate([-1, fw/2, 6]) rotate([0, 90, 0]) cylinder(h = ft + 2, r = 1.6);
    }
}

// ---------- Ensamble de referencia ----------
module arm_full() {
    base();
    translate([0, 0, 12]) color("gray") cylinder(h = arm_base_h - 12, r = 10); // columna a hombro
    translate([0, 0, arm_base_h]) rotate([0, pose_shoulder, 0]) {
        color("orange") link(arm_L1);
        translate([arm_L1, 0, 0]) rotate([0, pose_elbow, 0]) {
            color("tomato") link(arm_L2);
            translate([arm_L2, 0, 0]) rotate([0, pose_wrist, 0]) {
                color("gold") link(arm_L3);
                // pinza (dos dedos) al final
                translate([arm_L3, 0, arm_link_w/2]) {
                    translate([0,  8, 0]) gripper_finger();
                    translate([0, -8 - 14, 0]) gripper_finger();
                }
            }
        }
    }
}

// ---------- Selector de parte a renderizar ----------
if (part == "full")               arm_full();
else if (part == "link_l1")       link(arm_L1);
else if (part == "link_l2")       link(arm_L2);
else if (part == "link_l3")       link(arm_L3);
else if (part == "gripper_finger") gripper_finger();
else arm_full();
