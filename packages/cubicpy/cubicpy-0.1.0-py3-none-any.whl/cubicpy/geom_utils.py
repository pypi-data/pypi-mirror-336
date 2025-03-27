from panda3d.core import *


def create_line_node(start, end, color, thickness=1):
    """ランドマーク配列とラインペアから LineSegs を作り、GeomNodeにまとめて返す。"""
    lines = LineSegs()
    lines.setThickness(thickness)
    lines.setColor(*color)
    lines.moveTo(*start)  # ここから（5）
    lines.drawTo(*end)  # ここまで（5）

    # LineSegsからGeomNodeを作る
    geom_node = lines.create()
    return NodePath(geom_node)


def create_geom(parent, vertices, color, thickness=1.0):  # （1）
  """共通のGeomオブジェクトを作成する関数"""
  # GeomVertexDataを作成
  vdata = GeomVertexData('shape', GeomVertexFormat.getV3(), Geom.UHStatic)
  vdata.setNumRows(len(vertices))

  # GeomVertexWriterを使って頂点データを設定
  vertex = GeomVertexWriter(vdata, 'vertex')
  for v in vertices:
    vertex.addData3f(*v)

  if len(vertices) == 3:
    # GeomTrianglesの場合、頂点を三つずつ追加
    primitive = GeomTriangles(Geom.UHStatic)
    primitive.addVertices(0, 1, 2)
  else:
    # GeomLinesの場合、頂点をペアで追加
    primitive = GeomLines(Geom.UHStatic)
    for i in range(len(vertices) - 1):
      primitive.addVertices(i, i + 1)

  primitive.closePrimitive()

  # Geomを作成してGeomPrimitiveを追加
  geom = Geom(vdata)
  geom.addPrimitive(primitive)

  # GeomNodeを作成してGeomを設定
  node = GeomNode('shape_node')
  node.addGeom(geom)

  # ノードパスを作成してシーンに追加
  node_path = parent.attachNewNode(node)
  node_path.setColor(*color)  # 色を設定
  node_path.setRenderModeThickness(thickness)  # 線の太さを設定

  # 三角形の場合のみ透過属性を設定
  if len(vertices) == 3:
    node_path.setTransparency(TransparencyAttrib.MAlpha)

  return node_path  # ここまで（1）


def draw_line(parent, point1, point2, color, thickness=1.0):
  """直線を描画する関数"""
  return create_geom(parent, [point1, point2], color, thickness)


def draw_circumference(parent, radius, color, thickness=1.0, segs=64):
  """円周を描画する関数（ZX平面）"""
  vertices = [(radius * sin(2 * pi * i / segs), 0, radius * cos(2 * pi * i / segs)) for i in range(segs + 1)]
  return create_geom(parent, vertices, color, thickness)


def draw_triangle(parent, point1, point2, point3, color):
  """三角形を描画する関数（面に色を付ける）"""
  return create_geom(parent, [point1, point2, point3], color)
