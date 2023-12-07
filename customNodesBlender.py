import bpy
from bpy.types import NodeTree, Node, NodeSocket

# Implementation of custom nodes from Python


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class SuperColliderTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'SuperColliderTree'
    # Label for nice name display
    bl_label = "SuperCollider"
    # Icon identifier
    bl_icon = 'NODETREE'


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class SuperColliderTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'SuperColliderTree'


# Derived from the Node base type.

#==== Oscillators ====

#SinOsc node
class SinOscNode(SuperColliderTreeNode, Node):
    # === Basics ===
    # Description string
    '''A Sine oscillator ndoe'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'SinOscNodeType'
    # Label for nice name display
    bl_label = "SinOsc"
    # Icon identifier
    bl_icon = 'SOUND'

    # === Custom Properties ===
    frequency: bpy.props.FloatProperty(name="frequency", default=440.0)
    phase: bpy.props.FloatProperty(name="phase", default=0.0)
    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    def init(self, context):
        #inputs
        self.inputs.new('NodeSocketFloat', "frequency").default_value = 440.0
        self.inputs.new('NodeSocketFloat', "phase").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0
        #outputs
        self.outputs.new('NodeSocketFloat', "ar")


    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def generate_scd_code(self):
        node_id = self.name.replace(".", "_").lower()

        # Get values
        if self.inputs["frequency"].is_linked:
            from_node = self.inputs["frequency"].links[0].from_node
            frequency = f"{from_node.name.replace('.', '_').lower()}"
        else:
            frequency = self.inputs["frequency"].default_value

        if self.inputs["phase"].is_linked:
            from_node = self.inputs["phase"].links[0].from_node
            phase = f"{from_node.name.replace('.', '_').lower()}"
        else:
            phase = self.inputs["phase"].default_value
        
        if self.inputs["mul"].is_linked:
            from_node = self.inputs["mul"].links[0].from_node
            mul = f"{from_node.name.replace('.', '_').lower()}"
        else:
            mul = self.inputs["mul"].default_value

        if self.inputs["add"].is_linked:
            from_node = self.inputs["add"].links[0].from_node
            add = f"{from_node.name.replace('.', '_').lower()}"
        else:
            add = self.inputs["add"].default_value

        # Format as SuperCollider code
        sc_code = f"var {node_id}_freq = {frequency}, {node_id}_phase = {phase}, {node_id}_mul = {mul}, {node_id}_add = {add};\n"
        sc_code += f"var {node_id} = SinOsc.ar({node_id}_freq, {node_id}_phase, {node_id}_mul, {node_id}_add);\n"
        return sc_code

 #Saw node   
class SawNode(SuperColliderTreeNode, Node):
    bl_idname = 'SawNodeType'
    bl_label = "Saw"
    bl_icon = 'SOUND'

    frequency: bpy.props.FloatProperty(name="frequency", default=440.0)
    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "frequency").default_value = 440.0
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0
        self.outputs.new('NodeSocketFloat', "ar")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def generate_scd_code(self):
        node_id = self.name.replace(".", "_").lower()

        # Get values
        if self.inputs["frequency"].is_linked:
            from_node = self.inputs["frequency"].links[0].from_node
            frequency = f"{from_node.name.replace('.', '_').lower()}"
        else:
            frequency = self.inputs["frequency"].default_value

        if self.inputs["mul"].is_linked:
            from_node = self.inputs["mul"].links[0].from_node
            mul = f"{from_node.name.replace('.', '_').lower()}"
        else:
            mul = self.inputs["mul"].default_value

        if self.inputs["add"].is_linked:
            from_node = self.inputs["add"].links[0].from_node
            add = f"{from_node.name.replace('.', '_').lower()}"
        else:
            add = self.inputs["add"].default_value

        # Format as SuperCollider code
        sc_code = f"var {node_id}_freq = {frequency}, {node_id}_mul = {mul}, {node_id}_add = {add};\n"
        sc_code += f"var {node_id} = Saw.ar({node_id}_freq, {node_id}_mul, {node_id}_add);\n"
        return sc_code

#Pulse node
class PulseNode(SuperColliderTreeNode, Node):
    bl_idname = 'PulseNodeType'
    bl_label = "Pulse"
    bl_icon = 'SOUND'

    frequency: bpy.props.FloatProperty(name="frequency", default=440.0)
    width: bpy.props.FloatProperty(name="width", default=0.5)
    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "frequency").default_value = 440.0
        self.inputs.new('NodeSocketFloat', "Width").default_value = 0.5
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0

        self.outputs.new('NodeSocketFloat', "ar")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def generate_scd_code(self):
        node_id = self.name.replace(".", "_").lower()

        # Get values
        if self.inputs["frequency"].is_linked:
            from_node = self.inputs["frequency"].links[0].from_node
            frequency = f"{from_node.name.replace('.', '_').lower()}"
        else:
            frequency = self.inputs["frequency"].default_value

        if self.inputs["width"].is_linked:
            from_node = self.inputs["width"].links[0].from_node
            width = f"{from_node.name.replace('.', '_').lower()}"
        else:
            width = self.inputs["width"].default_value

        if self.inputs["mul"].is_linked:
            from_node = self.inputs["mul"].links[0].from_node
            mul = f"{from_node.name.replace('.', '_').lower()}"
        else:
            mul = self.inputs["mul"].default_value

        if self.inputs["add"].is_linked:
            from_node = self.inputs["add"].links[0].from_node
            add = f"{from_node.name.replace('.', '_').lower()}"
        else:
            add = self.input['add'].default_value

        # Format as SuperCollider code
        sc_code = f"var {node_id}_freq = {frequency}, {node_id}_width = {width}, {node_id}_mul = {mul}, {node_id}_add = {add};\n"
        sc_code += f"var {node_id} = Pulse.ar({node_id}_freq, {node_id}_width, {node_id}_mul, {node_id}_add);\n"
        return sc_code

#WhiteNoise node
class WhiteNoiseNode(SuperColliderTreeNode, Node):
    bl_idname = 'WhiteNoiseNodeType'
    bl_label = "WhiteNoise"
    bl_icon = 'SOUND'

    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0

        self.outputs.new('NodeSocketFloat', "ar")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def generate_scd_code(self):
        node_id = self.name.replace(".", "_").lower()

        # Get values
        if self.inputs["mul"].is_linked:
            from_node = self.inputs["mul"].links[0].from_node
            mul = f"{from_node.name.replace('.', '_').lower()}"
        else:
            mul = self.inputs["mul"].default_value

        if self.inputs["add"].is_linked:
            from_node = self.inputs["add"].links[0].from_node
            add = f"{from_node.name.replace('.', '_').lower()}"
        else:
            add = self.inputs["add"].default_value

        # Format as SuperCollider code
        sc_code = f"var {node_id}_mul = {mul}, {node_id}_add = {add};\n"
        sc_code += f"var {node_id} = WhiteNoise.ar({node_id}_mul, {node_id}_add);\n"
        return sc_code

#PinkNoise node
class PinkNoiseNode(SuperColliderTreeNode, Node):
    bl_idname = 'PinkNoiseNodeType'
    bl_label = "PinkNoise"
    bl_icon = 'SOUND'

    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0

        self.outputs.new('NodeSocketFloat', "ar")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")
        
    def generate_scd_code(self):
        node_id = self.name.replace(".", "_").lower()

        # Get values
        if self.inputs["mul"].is_linked:
            from_node = self.inputs["mul"].links[0].from_node
            mul = f"{from_node.name.replace('.', '_').lower()}"
        else:
            mul = self.inputs["mul"].default_value

        if self.inputs["add"].is_linked:
            from_node = self.inputs["add"].links[0].from_node
            add = f"{from_node.name.replace('.', '_').lower()}"
        else:
            add = self.inputs["add"].default_value

        # Format as SuperCollider code
        sc_code = f"var {node_id}_mul = {mul}, {node_id}_add = {add};\n"
        sc_code += f"var {node_id} = PinkNoise.ar({node_id}_mul, {node_id}_add);\n"
        return sc_code

#==== Envelope ====
class EnvelopeNode(SuperColliderTreeNode, Node):
    bl_idname = 'EnvelopeNodeType'
    bl_label = "Envelope"
    bl_icon = 'SOUND'

    attack: bpy.props.FloatProperty(name="attack", default=0.0)
    decay: bpy.props.FloatProperty(name="decay", default=0.0)
    sustain: bpy.props.FloatProperty(name="sustain", default=0.0)
    release: bpy.props.FloatProperty(name="release", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "input").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "attack").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "decay").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "sustain").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "release").default_value = 0.0

        self.outputs.new('NodeSocketFloat', "kr")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

#==== Filters ====
class HighPassFilterNode(SuperColliderTreeNode, Node):
    bl_idname = 'HighPassFilterNodeType'
    bl_label = "HighPassFilter"
    bl_icon = 'SOUND'

    #input: bpy.props.FloatProperty(name="input", default=0.0)
    frequency: bpy.props.FloatProperty(name="frequency", default=440.0)
    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "input").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "frequency").default_value = 440.0
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0

        self.outputs.new('NodeSocketFloat', "ar")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

class LowPassFilterNode(SuperColliderTreeNode, Node):
    bl_idname = 'LowPassFilterNodeType'
    bl_label = "LowPassFilter"
    bl_icon = 'SOUND'

    #input: bpy.props.FloatProperty(name="input", default=0.0)
    frequency: bpy.props.FloatProperty(name="frequency", default=440.0)
    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "input").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "frequency").default_value = 440.0
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0

        self.outputs.new('NodeSocketFloat', "ar")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

class BandPassFilterNode(SuperColliderTreeNode, Node):
    bl_idname = 'BandPassFilterNodeType'
    bl_label = "BandPassFilter"
    bl_icon = 'SOUND'

    #input: bpy.props.FloatProperty(name="input", default=0.0)
    frequency: bpy.props.FloatProperty(name="frequency", default=440.0)
    rq: bpy.props.FloatProperty(name="rq", default=1.0)
    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "input").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "frequency").default_value = 440.0
        self.inputs.new('NodeSocketFloat', "rq").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0

        self.outputs.new('NodeSocketFloat', "ar")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

class BandRejectFilterNode(SuperColliderTreeNode, Node):
    bl_idname = 'BandRejectFilterNodeType'
    bl_label = "BandRejectFilter"
    bl_icon = 'SOUND'

    #input: bpy.props.FloatProperty(name="input", default=0.0)
    frequency: bpy.props.FloatProperty(name="frequency", default=440.0)
    rq: bpy.props.FloatProperty(name="rq", default=1.0)
    mul: bpy.props.FloatProperty(name="mul", default=1.0)
    add: bpy.props.FloatProperty(name="add", default=0.0)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "input").default_value = 0.0
        self.inputs.new('NodeSocketFloat', "frequency").default_value = 440.0
        self.inputs.new('NodeSocketFloat', "rq").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "mul").default_value = 1.0
        self.inputs.new('NodeSocketFloat', "add").default_value = 0.0

        self.outputs.new('NodeSocketFloat', "ar")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

#==== Output ====
class OutputNode(SuperColliderTreeNode, Node):
    bl_idname = 'OutputNodeType'
    bl_label = "Output"
    bl_icon = 'SOUND'

    def init(self, context):
        self.inputs.new('NodeSocketFloat', "input").default_value = 0.0

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def generate_scd_code(self):
        # Format as SuperCollider code
        sc_code = "( \n SynthDef('from_blender', {\n"
        
        return sc_code
    
    def generate_scd_code_end(self):
        # Format as SuperCollider code
        from_node = self.inputs["input"].links[0].from_node
        sc_code = f"\n Out.ar(0, {from_node.name.replace('.','_').lower()})\n"
        sc_code += "}).add\n)"
        
        return sc_code


### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type

class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'SuperColliderTree'


# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory('OSCILLATORS', "Oscillators", items=[
        # our basic node
        NodeItem("SinOscNodeType"),
        NodeItem("SawNodeType"),
        NodeItem("PulseNodeType"),
        NodeItem("WhiteNoiseNodeType"),
        NodeItem("PinkNoiseNodeType"),
    ]),
    MyNodeCategory('ENVELOPE', "Envelope", items=[
        NodeItem("EnvelopeNodeType"),
    ]),
    MyNodeCategory('FILTERS', "Filters", items=[
        NodeItem("HighPassFilterNodeType"),
        NodeItem("LowPassFilterNodeType"),
        NodeItem("BandPassFilterNodeType"),
        NodeItem("BandRejectFilterNodeType"),
    ]),
    MyNodeCategory('OUTPUT', "Output", items=[
        NodeItem("OutputNodeType"),
    ]),
]

classes = (
    SuperColliderTree,
    #MyCustomSocket,
    SinOscNode,
    SawNode,
    PulseNode,
    WhiteNoiseNode,
    PinkNoiseNode,
    EnvelopeNode,
    HighPassFilterNode,
    LowPassFilterNode,
    BandPassFilterNode,
    BandRejectFilterNode,
    OutputNode,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('SCD_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('SCD_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

