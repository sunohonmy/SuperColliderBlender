import bpy
from collections import deque

    

class IterateNodes(bpy.types.Operator):
    bl_idname = "node.iterate_nodes"
    bl_label = "Iterate Nodes"

    def execute(self, context):
        supercollider_tree = None
        # Assuming 'SuperColliderTree' is the name of your custom node tree
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
            if node.bl_idname == "OutputNodeType":  # Replace with your output node's bl_idname
                output_node = node
                break

        if not output_node:
            self.report({'WARNING'}, "Output node not found")
            return {'CANCELLED'}

        # Perform BFS starting from the output node
        visited = set()
        queue = deque([output_node])
        scd_code = ""

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                #print(node.name)
                # Assuming all your nodes have a method called 'generate_scd_code'
                if hasattr(node, 'generate_scd_code'):
                    scd_code += node.generate_scd_code()

                for input_socket in node.inputs:
                    for link in input_socket.links:
                        queue.append(link.from_node)

        scd_code += output_node.generate_scd_code_end()
        print(scd_code)  # or handle the scd_code as needed

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