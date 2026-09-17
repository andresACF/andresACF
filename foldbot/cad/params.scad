// Foldbot — parámetros globales compartidos (todas las medidas en mm)
// Editar aquí para ajustar el diseño sin tocar la geometría.

// ---------- Brazo (ver docs/02-mecanica-brazo.md) ----------
arm_L1      = 150;   // eslabón hombro -> codo
arm_L2      = 120;   // eslabón codo -> muñeca
arm_L3      = 90;    // muñeca -> punta de la pinza
arm_base_h  = 70;    // altura de la base hasta el eje del hombro
arm_link_w  = 24;    // ancho de los eslabones
arm_link_t  = 8;     // espesor de pared de los eslabones
arm_base_d  = 90;    // diámetro de la base rotatoria
servo_len   = 40.5;  // caja de servo estándar (MG996R)
servo_w     = 20;
servo_h     = 38;

// Pose de ejemplo para el ensamble de referencia (grados)
pose_shoulder = 35;
pose_elbow    = -60;
pose_wrist    = -25;

// ---------- Tablero de plegado (ver docs/03-mecanica-plegado.md) ----------
board_center_w   = 200;  // ancho panel central
board_center_h   = 300;  // alto panel central
board_side_w     = 100;  // ancho de cada solapa lateral
board_bottom_h   = 150;  // alto de la solapa inferior
board_thickness  = 5;    // espesor de panel
board_hinge_gap  = 1.5;  // holgura de bisagra entre paneles

// ---------- Soporte de cámara (ver docs/01 y 05) ----------
cam_height        = 700;  // altura cenital sobre la mesa (60-80 cm)
cam_arm_len       = 250;  // voladizo del brazo de la cámara
cam_post_d        = 30;   // diámetro del poste
cam_plate_w       = 90;   // placa de montaje de la cámara (D435 ~90x25)
cam_plate_h       = 25;

// ---------- Calidad de render ----------
$fn = 48;
