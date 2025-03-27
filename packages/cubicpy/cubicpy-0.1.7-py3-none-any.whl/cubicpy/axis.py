from .geom_utils import create_line_node


class Axis:
    AXIS_COLORS = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    AXIS_LINES = [(1000, 0, 0), (0, 1000, 0), (0, 0, 10000)]
    GRID_COLOR = (0.5, 0.5, 0.5)

    def __init__(self, app):
        # 軸
        for color, position in zip(self.AXIS_COLORS, self.AXIS_LINES):
            line_node = create_line_node(
                (0, 0, 0), position, color, thickness=3)
            line_node.reparentTo(app.render)

        # グリッド
        for i in range(0, 1001, 20):
            line_node = create_line_node(
                (i, 0, 0), (i, 1000, 0), self.GRID_COLOR)
            line_node.reparentTo(app.render)
            line_node = create_line_node(
                (0, i, 0), (1000, i, 0), self.GRID_COLOR)
            line_node.reparentTo(app.render)
