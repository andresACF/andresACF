// Foldbot — Tablero de plegado con 3 solapas (modelo paramétrico)
// Objetivo Fase 0: verificar dimensiones, huecos de bisagra y ubicación de servos.
// Muestra el tablero en posición "plano" (solapas a 0 grados).

include <params.scad>;

part = "full";  // "full" | "center" | "flap_side" | "flap_bottom"

// Panel rectangular con esquinas simples.
module panel(w, h, t = board_thickness) {
    cube([w, h, t]);
}

// Hueco de montaje de servo (rectángulo pasante).
module servo_pocket() {
    translate([0, 0, -1]) cube([servo_len, servo_w, board_thickness + 2]);
}

module center_panel() {
    color("burlywood")
    difference() {
        panel(board_center_w, board_center_h);
        // marcas de centrado (cruz) para colocar la prenda
        translate([board_center_w/2 - 1, 10, board_thickness - 1])
            cube([2, board_center_h - 20, 2]);
        translate([10, board_center_h/2 - 1, board_thickness - 1])
            cube([board_center_w - 20, 2, 2]);
    }
}

// Solapa lateral (izquierda/derecha) con hueco para el servo actuador.
module flap_side() {
    color("sandybrown")
    difference() {
        panel(board_side_w, board_center_h);
        // hueco de servo cerca de la bisagra
        translate([board_side_w - servo_len - 8, board_center_h/2 - servo_w/2, 0])
            servo_pocket();
    }
}

// Solapa inferior.
module flap_bottom() {
    color("peru")
    difference() {
        panel(board_center_w, board_bottom_h);
        translate([board_center_w/2 - servo_len/2, 8, 0]) servo_pocket();
    }
}

// Ensamble plano: central + 2 laterales + inferior, separados por la holgura de
// bisagra (board_hinge_gap).
module folding_board_full() {
    g = board_hinge_gap;
    // central
    translate([board_side_w + g, board_bottom_h + g, 0]) center_panel();
    // lateral izquierda
    translate([0, board_bottom_h + g, 0]) flap_side();
    // lateral derecha
    translate([board_side_w + board_center_w + 2*g, board_bottom_h + g, 0]) flap_side();
    // inferior
    translate([board_side_w + g, 0, 0]) flap_bottom();
}

if (part == "full")            folding_board_full();
else if (part == "center")     center_panel();
else if (part == "flap_side")  flap_side();
else if (part == "flap_bottom") flap_bottom();
else folding_board_full();
