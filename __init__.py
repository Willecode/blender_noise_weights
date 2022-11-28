import bpy
from . import noise_weights

bl_info = {
    "name": "Noise Weights",
    "description": "Tool to generate vertex weights based on noise.",
    "author": "Wilkan",
    "version": (1, 0, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Weights > Noise Weights",
    "category": "Object",
}


def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("wm.noise_weights", text="Noise Weights")


def register():
    if bpy.app.background:
        return
    bpy.utils.register_class(noise_weights.NOISEWEIGHTS_OT_generate_weights)
    bpy.types.VIEW3D_MT_paint_weight.append(draw_menu)


def unregister():
    if bpy.app.background:
        return
    bpy.utils.unregister_class(noise_weights.NOISEWEIGHTS_OT_generate_weights)
    bpy.types.VIEW3D_MT_paint_weight.remove(draw_menu)


if __name__ == '__main__':
    register()
