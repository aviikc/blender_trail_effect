# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


# ====================
# BLENDER_TRAIL_EFFECT
# ====================
#
#
# blender_trail_effect - fork @ https://github.com/aviik/blender_trail_effect.git
# @ author       : Aviik C
# @ date-created : Jun 18, 2020
# @ email        : aviik.chakraborty@gmail.com
# @ file-name    : traileff.py
#
#
"""
First animate the object.
This add on can be used on animated objects to generate a polycurve that looks like a trail.
"""
bl_info = {
    "name": "blender_trail_effect",
    "author": "Aviik C",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3DView",
    "description": "test",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


import bpy


def main(context):
    coords_list = []
    
#    target = bpy.context.scene.objects['Cube']
    target = context.active_object
#    print("abc")
    if int(target.animation_data.action.fcurves[0].range()[1])>0:
        for i in range(bpy.data.scenes['Scene'].frame_current ):
            coords_list.append([spline_point.evaluate(i) for spline_point in target.animation_data.action.fcurves ])
        print(coords_list)    
    #        coords_list = getKFlocations(x)
        # make a new curve
        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '3D'

        # make a new spline in that curve
        spline = crv.splines.new(type='NURBS')

        # a spline point for each point
        spline.points.add(len(coords_list)-1) # theres already one point by default

        # assign the point coordinates to the spline points
        for p, new_co in zip(spline.points, coords_list):
            p.co = (new_co + [1.0]) # (add nurbs weight)

        # make a new object with the curve
        obj = bpy.data.objects.new('object_name', crv)
        bpy.context.scene.collection.objects.link(obj)     
        
        

class MYADDON_OT_path_tracer(bpy.types.Operator):
    """A Basic Single line Path Tracer"""
    bl_idname = "myaddon.path_tracer"
    bl_label = "Simple Path Tracer"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MYADDON_OT_path_tracer)


def unregister():
    bpy.utils.unregister_class(MYADDON_OT_path_tracer)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.path_tracer()

    
