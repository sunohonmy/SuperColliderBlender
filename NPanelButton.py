import bpy

class SCDFile(bpy.types.Operator):
    

class IterateNodes(bpy.types.Operator):
    bl_idname = "node.iterate_nodes"
    bl_label = "Iterate Nodes"

    def execute(self, context):
        # Find the SuperColliderTree node tree
        supercollider_tree = None
        for tree in bpy.data.node_groups:
            if tree.bl_idname == 'SuperColliderTree':
                supercollider_tree = tree
                break

        if not supercollider_tree:
            self.report({'WARNING'}, "SuperColliderTree not found")
            return {'CANCELLED'}
        
        # Iterate over nodes in the SuperColliderTree
        print("Nodes in the SuperColliderTree:")
        for node in supercollider_tree.nodes:
            print("  Node:", node.name)
            
        # Iterate over links and print the connections
        print("\nLinks in the SuperColliderTree:")
        for link in supercollider_tree.links:
            from_node = link.from_node
            to_node = link.to_node
            from_socket = link.from_socket.name
            to_socket = link.to_socket.name
            print(f"  Link from '{from_node.name}' ({from_socket}) to '{to_node.name}' ({to_socket})")
            
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