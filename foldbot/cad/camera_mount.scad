// Foldbot — Soporte cenital de la cámara RGB-D (modelo paramétrico)
// Poste vertical + brazo en voladizo + placa de montaje mirando hacia abajo.

include <params.scad>;

part = "full";  // "full" | "plate"

module post() {
    color("slategray") cylinder(h = cam_height, r = cam_post_d/2);
}

module foot() {
    color("dimgray")
    difference() {
        cylinder(h = 12, r = cam_post_d);
        translate([0, 0, -1]) cylinder(h = 14, r = cam_post_d/2 - 3);
    }
}

// Placa de montaje de la cámara (patrón de agujeros genérico tipo RealSense).
module cam_plate() {
    color("teal")
    difference() {
        cube([cam_plate_w, cam_plate_h + 20, 4]);
        // dos agujeros de 1/4" (~6.3 mm) y M3 auxiliares
        for (x = [cam_plate_w*0.25, cam_plate_w*0.75])
            translate([x, (cam_plate_h + 20)/2, -1]) cylinder(h = 6, r = 3.2);
        // ventana para el conector USB-C
        translate([cam_plate_w/2 - 8, cam_plate_h + 6, -1]) cube([16, 8, 6]);
    }
}

module camera_mount_full() {
    foot();
    post();
    // brazo en voladizo arriba
    translate([0, 0, cam_height])
        rotate([0, 90, 0])
            color("slategray") cylinder(h = cam_arm_len, r = cam_post_d/2 - 4);
    // placa mirando hacia abajo al final del voladizo
    translate([cam_arm_len, -cam_plate_w/2, cam_height - 6])
        rotate([0, 0, 90]) cam_plate();
}

if (part == "full")       camera_mount_full();
else if (part == "plate") cam_plate();
else camera_mount_full();
