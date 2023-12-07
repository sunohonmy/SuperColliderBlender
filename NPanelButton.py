import bpy
from collections import deque

    

class IterateNodes(bpy.types.Operator):
    bl_idname = "node.iterate_nodes"
    bl_label = "Iterate Nodes"

    def execute(self, context):
        supercollider_tree = None

        for tree in bpy.data.node_groups:
            if tree.bl_idname == 'SuperColliderTree':
                supercollider_tree = tree
                break

        if not supercollider_tree:
            self.report({'WARNING'}, "SuperColliderTree not found")
            return {'CANCELLED'}

        # Identify the output node
        output_node = None
        for node in supercollider_tree.nodes:
            if node.bl_idname == "OutputNodeType":
                output_node = node
                break

        if not output_node:
            self.report({'WARNING'}, "Output node not found")
            return {'CANCELLED'}

        # Perform BFS starting from the output node
        visited = deque([])
        queue = deque([output_node])
        scd_code = output_node.generate_scd_code()

        while queue:
            node = queue.pop()
            if node not in visited:
                visited.append(node)

                for input_socket in node.inputs:
                    for link in input_socket.links:
                        queue.append(link.from_node)

        while len(visited) > 1:
            node = visited[-1]
            if hasattr(node, 'generate_scd_code'):
                    scd_code += node.generate_scd_code()
            visited.pop()
            
        scd_code += output_node.generate_scd_code_end()
        print(scd_code)
        to_scd = open("/Users/up2071478/Desktop/blenderSCD.scd", "w")
        to_scd.write(scd_code)

        return {'FINISHED'}

class NODE_EDITOR_PT_CustomPanel(bpy.types.Panel):
    bl_label = "SuperCollider"
    #bl_idname = "NODE_EDITOR_PT_custom_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "SCD"

    def draw(self, context):
        #1 row, with 1 button to iterate over the node tree from SupercolliderNodeTree
        row = self.layout.row()
        row.operator("node.iterate_nodes", text = "Run")

classes = (
    NODE_EDITOR_PT_CustomPanel,
    IterateNodes,
)
        

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()