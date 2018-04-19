import hou
import subprocess

def getRenderNode(node):
    render_nodes = ("rop_geometry", "geometry", "Redshift_ROP", "ifd", "arnold", "opengl", "baketexture::3.0", "rib", "ris", "ribarchive", "wren", "ifdarchive", "render", "rop_alembic", "brickmap", "merge", "channel", "comp", "dsmmerge", "fetch", "wedge", "subnet", "shell", "null", "dop", "alembic", "filmboxfbx", "agent", "mdd", "switch")

    node_type_name = node.type().name()
    node_children = node.allSubChildren()

    if node_type_name in render_nodes:
        return node
    elif len(node_children) is not 0:
        for n in node_children:
            if n.type().name() in render_nodes:
                return n
    else:
        print("No render nodes were found.\n")
        return None

def bg_render(kwargs):
    nodes = hou.selectedNodes()

    if not bool( nodes ):
        print("No nodes selected.\n")
        return

    file_path = hou.hipFile.path()
    file_name = hou.hipFile.basename()

    for node in nodes:
        top_node = node
        node = getRenderNode(node)
        if node == None:
            return

        rop_path = node.path()
        top_node_path = top_node.path()

        frame_by_frame = ""
        if kwargs["altclick"]:
            frame_by_frame = "I"

        hscript_cmd = "render -Va{0} {1}; quit".format(frame_by_frame, rop_path)
        intro = "Rendering {0} in {1}".format(top_node_path, file_name)
        finish = "\\n\\nRendering was finished, press [enter] to close terminal."

        bash_render_cmd = 'hbatch -c \\"{0}\\" {1}'.format(hscript_cmd, file_path)
        
        p = subprocess.Popen(["x-terminal-emulator", "-t", intro, "-e", 'bash -c "printf \\"{0}\\" && {1} && printf \\"{2}\\" && read"'.format(intro + "\\n\\n\\n", bash_render_cmd, finish) ], stdout=subprocess.PIPE)
        output = p.communicate()[0]
