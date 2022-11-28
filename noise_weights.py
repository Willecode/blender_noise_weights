from copy import copy
import bpy
import mathutils


class NOISEWEIGHTS_OT_generate_weights(bpy.types.Operator):
    """Create noise based vertex weights"""
    bl_idname = "wm.noise_weights"
    bl_label = "Noise based weights"
    bl_description = "Generate vertex weights from noise."
    # bl_options = {'REGISTER'}

    enum_items = [
        ('BLENDER',         'BLENDER',          ''),
        ('PERLIN_ORIGINAL', 'PERLIN_ORIGINAL', ''),
        ('PERLIN_NEW',      'PERLIN_NEW',      ''),
        ('VORONOI_F1',      'VORONOI_F1',      ''),
        ('VORONOI_F2',      'VORONOI_F2',      ''),
        ('VORONOI_F3',      'VORONOI_F3',      ''),
        ('VORONOI_F4',      'VORONOI_F4',      ''),
        ('VORONOI_F2F1',    'VORONOI_F2F1',    ''),
        ('VORONOI_CRACKLE', 'VORONOI_CRACKLE', ''),
        ('CELLNOISE',       'CELLNOISE',       '')]

    # Popup fields
    noise_position: bpy.props.FloatVectorProperty(name="Noise position")
    noise_scale: bpy.props.FloatProperty(name="Noise scale", default=0.1)
    noise_type: bpy.props.EnumProperty(items=enum_items, name="Noise type")

    def invoke(self, context, event):
        """Get active object, active vertex group, show opoup dialog"""
        # Get object
        self.obj = context.active_object

        # Get active vertex group
        if len(self.obj.vertex_groups.values()) == 0:
            self.report({'INFO'}, "No active vertex group!")
            return {'FINISHED'}
        else:
            self.vert_group = self.obj.vertex_groups.active
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        """Loop through objects vertices and sample noise using their coords"""
        for vert in self.obj.data.vertices:
            weight = mathutils.noise.noise(self.noise_scale * (self.shiftPos(vert.co)), noise_basis=self.noise_type)
            self.vert_group.add([vert.index], weight, 'REPLACE')
        return {'FINISHED'}

    def shiftPos(self, inVec):
        """Shift position of inVec by self.noise_position parameter"""
        retVec = copy(inVec)
        retVec.x += self.noise_position[0]
        retVec.y += self.noise_position[1]
        retVec.z += self.noise_position[2]
        return retVec
