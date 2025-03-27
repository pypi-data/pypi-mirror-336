from math import sin, cos, radians
from panda3d.core import Point3, OrthographicLens



class CameraControl:
    BASE_FILM_SIZE = (800, 600)
    BASE_RADIUS = 50
    BASE_THETA = 80
    BASE_PHI = -80
    MIN_PHI = 0.0000001

    def __init__(self, app):
        self.app = app
        self.app.disableMouse()
        self.camera_radius = self.BASE_RADIUS
        self.camera_theta = self.BASE_THETA
        self.camera_phi = self.BASE_PHI
        self.camera_set_pos()

        # # カメラを平行投影に変更
        # self.lens = OrthographicLens()
        # self.film_size = self.BASE_FILM_SIZE
        # self.lens.setFilmSize(*self.film_size)  # 表示範囲のサイズを設定
        # self.app.cam.node().setLens(self.lens)

        self.app.accept('arrow_right', self.change_camera_angle, [0, 1])
        self.app.accept('arrow_left', self.change_camera_angle, [0, -1])
        self.app.accept('arrow_up', self.change_camera_angle, [-1, 0])
        self.app.accept('arrow_down', self.change_camera_angle, [1, 0])
        self.app.accept('arrow_right-repeat', self.change_camera_angle, [0, 1])
        self.app.accept('arrow_left-repeat', self.change_camera_angle, [0, -1])
        self.app.accept('arrow_up-repeat', self.change_camera_angle, [-1, 0])
        self.app.accept('arrow_down-repeat', self.change_camera_angle, [1, 0])
        self.app.accept('wheel_up', self.change_camera_radius, [1.1])
        self.app.accept('wheel_down', self.change_camera_radius, [0.9])
        self.app.accept('r', self.reset_camera)

    def change_camera_angle(self, theta, phi):
        self.camera_theta += theta
        self.camera_phi += phi
        if self.camera_theta <= 0:
            self.camera_theta = self.MIN_PHI
        if 180 <= self.camera_theta:
            self.camera_theta = 180 - self.MIN_PHI
        self.camera_set_pos()

    def change_camera_radius(self, ratio):
        self.camera_radius *= ratio
        self.camera_set_pos()

    # def change_film_size(self, rate):
    #     self.film_size = tuple([int(size * rate) for size in self.film_size])
    #     self.lens.setFilmSize(*self.film_size)  # 表示範囲のサイズを設定
    #     self.app.cam.node().setLens(self.lens)

    def camera_set_pos(self):
        radius = self.camera_radius
        theta = self.camera_theta
        phi = self.camera_phi
        position = Point3(*self.convert_to_cartesian(radius, theta, phi))
        self.app.camera.setPos(position)
        self.app.camera.lookAt(0, 0, 0)

    def reset_camera(self):
        self.camera_radius = self.BASE_RADIUS
        self.camera_theta = self.BASE_THETA
        self.camera_phi = self.BASE_PHI
        self.camera_set_pos()
        # self.lens.setFilmSize(*self.BASE_FILM_SIZE)  # 表示範囲のサイズを設定
        # self.app.cam.node().setLens(self.lens)

    @staticmethod
    def convert_to_cartesian(r, theta, phi):
        rad_theta, rad_phi = radians(theta), radians(phi)
        x = r * sin(rad_theta) * cos(rad_phi)
        y = r * sin(rad_theta) * sin(rad_phi)
        z = r * cos(rad_theta)
        return x, y, z
