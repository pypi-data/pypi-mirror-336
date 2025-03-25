from nicegui.elements.scene import Scene


class ExtendedScene(Scene,
                    component='mesh_scene.js',):

    from .objects3d import Mesh as mesh, Wire as wire, Spline as spline

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
