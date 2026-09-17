# Foldbot CAD — render por lotes de OpenSCAD a STL
# Uso:  make        -> genera todos los STL en stl/
#       make clean  -> borra stl/
# Requiere: openscad en el PATH.

OPENSCAD ?= openscad
OUT := stl

ARM_PARTS := full link_l1 link_l2 link_l3 gripper_finger
BOARD_PARTS := full center flap_side flap_bottom
CAM_PARTS := full plate

.PHONY: all clean dirs arm board camera
all: arm board camera

dirs:
	@mkdir -p $(OUT)

arm: dirs
	@for p in $(ARM_PARTS); do \
		echo "openscad arm.scad part=$$p"; \
		$(OPENSCAD) -o $(OUT)/arm_$$p.stl -D "part=\"$$p\"" arm.scad; \
	done

board: dirs
	@for p in $(BOARD_PARTS); do \
		echo "openscad folding_board.scad part=$$p"; \
		$(OPENSCAD) -o $(OUT)/board_$$p.stl -D "part=\"$$p\"" folding_board.scad; \
	done

camera: dirs
	@for p in $(CAM_PARTS); do \
		echo "openscad camera_mount.scad part=$$p"; \
		$(OPENSCAD) -o $(OUT)/camera_$$p.stl -D "part=\"$$p\"" camera_mount.scad; \
	done

clean:
	rm -rf $(OUT)
