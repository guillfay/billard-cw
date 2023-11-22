import numpy as np
import numpy.linalg as linalg

class Ball:
    def __init__(self, number, initial_position, radius, mass, state, color):
        assert type(initial_position) is np.ndarray, "la position doit être un vecteur numpy"
        assert initial_position.shape == (2,), "la position doit être un vecteur de dimension (2,)"
        assert mass > 0, "la masse doit être un nombre positive"
        assert radius > 0, "le rayon doit être un nombre positive"
        self.number = number
        self.radius = radius  # en m
        self.mass = mass  # en kg
        self.position = initial_position
        self.speed = np.array([0, 0])
        self.state = state  # un booleen pour savoir si la boule est en jeu
        self.color = color

    def set_size(self, new_radius, new_mass):
        assert new_mass > 0, "la masse doit être un nombre positive"
        assert new_radius > 0, "le rayon doit être un nombre positive"
        self.radius = new_radius
        self.mass = new_mass

    def update_position(self, vecteur_position):
        assert type(vecteur_position) is np.ndarray, "la position doit être un vecteur numpy"
        self.position = vecteur_position

    def update_speed(self, vector_vitesse):
        assert type(vector_vitesse) is np.ndarray, "la vitesse doit être un vecteur numpy"
        self.speed = vector_vitesse

    def update_state(self, new_state):
        self.state = new_state

    def __str__(self):
        if self.state:
            valeur = "en jeu"
        else:
            valeur = "hors-jeu"
        return "La boule numéro " + str(self.number) + " se trouve à la position " + str(
            self.position) + " et a un vecteur vitesse de " + str(self.speed) + ". La boule est " + valeur + " ."


class Board:
    def __init__(self, length, width):
        assert length > 0, "la longueur doit être un nombre positive"
        assert width > 0, "la largeur doit être un nombre positive"
        self.length = length
        self.width = width
        self.corners = self.get_corners()  # liste de 4 couples qui correspondent aux coordonnées des coins
        self.middle = self.get_middle()

    def get_corners(self):
        corner1 = np.array([0, 0])
        corner2 = np.array([0, self.length])
        corner3 = np.array([self.width, self.length])
        corner4 = np.array([self.width, 0])
        return [corner1, corner2, corner3, corner4]

    def get_pockets(self):
        return [np.array([0, 0]), np.array([0, self.length / 2]), np.array([0, self.length]),
                np.array([self.width, self.length]), np.array([self.width, self.length / 2]),
                np.array([self.width, 0])]

    def get_middle(self):
        return np.array([self.width / 2, self.length / 2])

    def set_size(self, new_length, new_width):
        assert new_length > 0, "la longueur doit être un nombre positive"
        assert new_width > 0, "la largeur doit être un nombre positive"
        self.length = new_length
        self.width = new_width
        self.middle = self.get_middle()
        self.corners = self.get_corners()

    def __str__(self):
        return "La table a une largeur " + str(self.width) + " et de longueur " + str(
            self.length) + " a ses coins aux position " + str(
            self.corners) + " et son milieu se trouve aux coordonnées" + str(self.middle) + "."


class Pool:
    def __init__(self, type_billard):
        self.type_billard = type_billard
        match type_billard:
            case 'anglais':
                number_of_balls = 16
                length, width = 2.14, 1.22
                radius = 0.0262
                mass = 0.140

                def construct_liste_pos():
                    liste_pos = []
                    pos_b = [width / 2, 0.425]
                    liste_pos.append(pos_b)
                    x1, y1 = width / 2, length - 0.495
                    pos_1 = [x1, y1]
                    liste_pos.append(pos_1)
                    eps = radius / 100
                    for k in range(2, 4):
                        y = y1 + eps + 2 * radius * np.cos(30 * np.pi / 180)
                        x = x1 - 2 * eps - 2 * radius * np.sin(30 * np.pi / 180) + k % 2 * 2 * (radius + eps)
                        liste_pos.append([x, y])
                    for k in range(4, 7):
                        y = y1 + 2 * eps + 4 * radius * np.cos(30 * np.pi / 180)
                        x = x1 - 4 * eps - 4 * radius * np.sin(30 * np.pi / 180) + k % 4 * 2 * (radius + eps)
                        liste_pos.append([x, y])
                    for k in range(7, 11):
                        y = y1 + 3 * eps + 6 * radius * np.cos(30 * np.pi / 180)
                        x = x1 - 6 * eps - 6 * radius * np.sin(30 * np.pi / 180) + k % 7 * 2 * (radius + eps)
                        liste_pos.append([x, y])
                    for k in range(11, 16):
                        y = y1 + 4 * eps + 8 * radius * np.cos(30 * np.pi / 180)
                        x = x1 - 8 * eps - 8 * radius * np.sin(30 * np.pi / 180) + k % 11 * 2 * (radius + eps)
                        liste_pos.append([x, y])
                    return liste_pos

                liste_pos = construct_liste_pos()
                liste_color = ['w', 'r', 'r', 'y', 'y', 'k', 'r', 'r', 'y', 'r', 'y', 'y', 'r', 'y', 'y', 'r']
            case 'americain':
                number_of_balls = 16
                length, width = 2.54, 1.27
                radius = 0.0286
                mass = 0.162

                def construct_liste_pos():
                    liste_pos = []
                    pos_b = [width / 2, length / 4]
                    liste_pos.append(pos_b)
                    x1, y1 = width / 2, length * 3 / 4
                    pos_1 = [x1, y1]
                    liste_pos.append(pos_1)
                    eps = radius / 100
                    for k in range(2, 4):
                        y = y1 + eps + 2 * radius * np.cos(30 * np.pi / 180)
                        x = x1 - 2 * eps - 2 * radius * np.sin(30 * np.pi / 180) + k % 2 * 2 * (radius + eps)
                        liste_pos.append([x, y])
                    for k in range(4, 7):
                        y = y1 + 2 * eps + 4 * radius * np.cos(30 * np.pi / 180)
                        x = x1 - 4 * eps - 4 * radius * np.sin(30 * np.pi / 180) + k % 4 * 2 * (radius + eps)
                        liste_pos.append([x, y])
                    for k in range(7, 11):
                        y = y1 + 3 * eps + 6 * radius * np.cos(30 * np.pi / 180)
                        x = x1 - 6 * eps - 6 * radius * np.sin(30 * np.pi / 180) + k % 7 * 2 * (radius + eps)
                        liste_pos.append([x, y])
                    for k in range(11, 16):
                        y = y1 + 4 * eps + 8 * radius * np.cos(30 * np.pi / 180)
                        x = x1 - 8 * eps - 8 * radius * np.sin(30 * np.pi / 180) + k % 11 * 2 * (radius + eps)
                        liste_pos.append([x, y])
                    return liste_pos

                liste_pos = construct_liste_pos()
                liste_color = ['w', 'y', 'b', 'r', 'purple', 'orange', 'g', 'brown', 'k', 'y', 'b', 'r', 'purple',
                               'orange', 'g', 'brown']
            case 'francais':
                number_of_balls = 3
                length, width = 3.1, 1.68
                radius = 0.0305
                mass = 0.210

                def construct_liste_pos():
                    pos_b = np.array([width / 2, length / 4])
                    pos_1 = np.array([width / 2 - 0.1825, length * 3 / 4])
                    pos_2 = np.array([width / 2, length * 3 / 4])
                    return [pos_b, pos_1, pos_2]

                liste_pos = construct_liste_pos()
                liste_color = ['r', 'w', 'w']
            case _:
                raise Exception("Billard '" + str(type_billard) + "' non géré")

        self.board = Board(length=length, width=width)
        self.balls = {}
        for i in range(0, number_of_balls):
            self.balls[i] = Ball(i, np.array(liste_pos[i]), radius, mass, True, liste_color[i])
        self.number_of_balls = number_of_balls
     
    def __str__(self):
        chaine = ""
        for i in range(self.number_of_balls):
            chaine += str(self.balls[i]) + " - "
        return chaine


class Cue:
    def __init__(self, mass):
        self.mass = mass

    def frappe(self, energie, angle, ball):
        """Energie en J, angle en rad par rapport à l'axe x"""
        v_cue = np.sqrt(2 * energie / self.mass)
        v_ball = self.mass / ball.mass * v_cue
        ball.update_speed(np.array([np.sin(angle*np.pi/180) * v_ball, np.cos(angle*np.pi/180) * v_ball]))

# billard = Pool('americain')
# print(billard.balls[0].radius)
# C = Cue(0.5)
# print(billard.balls["0"])
# C.frappe(1, 0, billard.balls["0"])
# print(billard.balls["0"])
