import numpy as np


# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 4--------------------------------------
# --------------------------------------------------------------------------------------------

def update_ball_bounce(board, ball, dt, bounce_status):
    """Mets à jour la position et la vitesse d'une boule si celle-ci
    a rebondi contre un bord """
    new_pos = ball.position + ball.speed * dt
    new_speed = ball.speed

    x_min = min([corner[0] for corner in board.corners]) + ball.radius
    x_max = max([corner[0] for corner in board.corners]) - ball.radius
    y_min = min([corner[1] for corner in board.corners]) + ball.radius
    y_max = max([corner[1] for corner in board.corners]) - ball.radius

    def rebond_x(x_bord, x_virt):
        return 2 * x_bord - x_virt

    def rebond_y(y_bord, y_virt):
        return 2 * y_bord - y_virt

    if bounce_status[0]:
        new_pos[0] = rebond_x(x_min, new_pos[0])
        new_speed = new_speed * np.array([-1, 1])
    if bounce_status[2]:
        new_pos[0] = rebond_x(x_max, new_pos[0])
        new_speed = new_speed * np.array([-1, 1])
    if bounce_status[3]:
        new_pos[1] = rebond_y(y_min, new_pos[1])
        new_speed = new_speed * np.array([1, -1])
    if bounce_status[1]:
        new_pos[1] = rebond_y(y_max, new_pos[1])
        new_speed = new_speed * np.array([1, -1])

    return new_pos, new_speed


def detect(board, ball, dt):
    """Cette fonction prend en argument une table, une balle et l'incrément de temps.
    Elle calcule la position de la boule après dt, et renvoie un tuple indiquant s'il y a un ou des rebonds sur les
    bandes. L'ordre du tuple part du bord de gauche, en x=0, et tourne dans le sens horaire"""

    pos_virt = ball.position + ball.speed * dt

    x_min = min([corner[0] for corner in board.corners]) + ball.radius
    x_max = max([corner[0] for corner in board.corners]) - ball.radius
    y_min = min([corner[1] for corner in board.corners]) + ball.radius
    y_max = max([corner[1] for corner in board.corners]) - ball.radius

    return pos_virt[0] < x_min, pos_virt[1] > y_max, pos_virt[0] > x_max, pos_virt[1] < y_min


def update_positions_bounce(pool, delta_t):
    """Mets à jour la position et la vitesse de toutes les boules si celles-ci
    ont rebondi contre un bord """
    balls = pool.balls
    for ball in balls.values():
        bounce_status = detect(pool.board, ball, delta_t)
        new_pos, new_speed = update_ball_bounce(pool.board, ball, delta_t, bounce_status)
        if pool.type_billard != 'francais':
            check_exit(pool, ball)
        update_ball_with_exit(pool, ball, new_pos, new_speed)


def update_ball_with_exit(pool, ball, new_pos, new_speed):
    if not ball.state:
        # ball.update_position(np.array([-10*ball.position[0],-10*ball.position[1]]))
        ball.update_position(np.array([0.1 + 1.8 * ball.radius * ball.number, pool.board.length + 0.1]))
        ball.update_speed(np.array([0, 0]))
        if ball.number == 0:
            print("La boule blanche est sortie")
    else:
        ball.update_position(new_pos)
        ball.update_speed(new_speed)


def update_position_bounceless(pool, delta_t):
    """Mets à jour la position de toutes les boules du billard à l'instant delta_t
    en considérant leur vitesse constante sur ce pas de temps"""
    number_of_balls = pool.number_of_balls
    for i in range(number_of_balls):
        new_position = pool.balls[i].position + delta_t * pool.balls[i].speed
        pool.balls[i].update_speed(pool.balls[i].speed)
        pool.balls[i].update_position(new_position)


# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 6--------------------------------------
# --------------------------------------------------------------------------------------------

def collided(ball1, ball2):
    """Vérifie si les deux boules se superposent, i.e : s'entrechoquent"""
    return np.linalg.norm(ball1.position - ball2.position) < ball1.radius + ball2.radius


def collision_matrix(pool):
    """Crée une matrice de booléen telle que matrix[i][j]
    #est True si les boules i et j s'entrechoquent
    False sinon"""
    balls = pool.balls
    number_of_balls = pool.number_of_balls
    matrix = np.zeros((number_of_balls, number_of_balls))
    for i in range(number_of_balls):
        for j in range(i + 1, number_of_balls):
            matrix[i][j] = collided(balls[i], balls[j])
            matrix[j][i] = matrix[i][j]
        matrix[i][i] = 0
    return matrix > 0


def impact_time(ball1, ball2):
    """Détermine l'instant d'impact entre deux boules qui s'entrechoquent."""

    square_radius = (ball1.radius + ball2.radius) ** 2
    Delta_Vx = ball2.speed[0] - ball1.speed[0]
    Delta_Vy = ball2.speed[1] - ball1.speed[1]
    Delta_X = ball2.position[0] - ball1.position[0]
    Delta_Y = ball2.position[1] - ball1.position[1]
    a = Delta_Vx ** 2 + Delta_Vy ** 2
    b = 2 * Delta_X * Delta_Vx + 2 * Delta_Y * Delta_Vy
    c = Delta_X ** 2 + Delta_Y ** 2 - square_radius
    if a == 0:
        sol1 = -c / b
        sol2 = sol1
    else:
        Delta = b ** 2 - 4 * a * c
        sqrt_delta = np.sqrt(Delta)
        sol1 = (-b + sqrt_delta) / (2 * a)
        sol2 = (-b - sqrt_delta) / (2 * a)
    if sol1 < 0:
        raise ValueError("Sol 1 est négative ")
    if sol2 < 0:
        raise ValueError("Sol 2 est négative ")
    return min(sol1, sol2)  # On garde la plus petite solution positive


def first_impact(pool, potential_collisions):
    """Détermine le premier choc chronologiquement et son instant."""
    number_of_balls = pool.number_of_balls
    matrix = np.zeros((number_of_balls, number_of_balls))
    for i in range(number_of_balls):
        matrix[i][i] = np.inf
        for j in range(i + 1, number_of_balls):
            if potential_collisions[i][j]:
                matrix[i][j] = impact_time(pool.balls[i], pool.balls[j])
            else:
                matrix[i][j] = np.inf
            matrix[j][i] = matrix[i][j]
    index = np.array(np.unravel_index(np.argmin(matrix), matrix.shape))
    return np.min(matrix), index


def update_speed_2collidedBalls(pool, index):
    """Met à jour la vitesse de deux boules qui s'entrechoquent"""
    ball1 = pool.balls[index[0]]
    ball2 = pool.balls[index[1]]
    vec_1to2 = ball2.position - ball1.position
    vec_1to2 = vec_1to2 / np.linalg.norm(vec_1to2)
    deltaV = np.dot(ball1.speed + ball2.speed, vec_1to2)
    v1 = ball1.speed
    v1n = np.dot(ball1.speed, vec_1to2) * vec_1to2
    v1t = ball1.speed - v1n
    v2 = ball2.speed
    v2n = np.dot(ball2.speed, vec_1to2) * vec_1to2
    v2t = ball2.speed - v2n
    if deltaV >= 0:
        deltaV_2 = np.sqrt(
            np.linalg.norm(v1) ** 2 + np.linalg.norm(v2) ** 2 - np.linalg.norm(v1t) ** 2 - np.linalg.norm(
                v2t) ** 2) * vec_1to2 - v2n
        deltaV_1 = - v1n
    else:
        deltaV_1 = np.sqrt(
            np.linalg.norm(v1) ** 2 + np.linalg.norm(v2) ** 2 - np.linalg.norm(v1t) ** 2 - np.linalg.norm(v2t) ** 2) * (
                       -vec_1to2) - v1n
        deltaV_2 = - v2n
    new_speed1 = ball1.speed + deltaV_1
    new_speed2 = ball2.speed + deltaV_2
    pool.balls[index[0]].update_speed(new_speed1)
    pool.balls[index[1]].update_speed(new_speed2)


# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 7--------------------------------------
# --------------------------------------------------------------------------------------------

def friction(pool, delta_t, alpha=0.95, v_min=0.01):
    """Met à jour la vitesse de toutes les boules de sorte que toutes les secondes
    elles perdent alpha (en pourcentage) de leur vitesse. De plus,
    elle arrête les boules qui ont une vitesse inférieure en norme a v_min"""

    balls = pool.balls
    number_of_balls = pool.number_of_balls
    for i in range(number_of_balls):
        if np.linalg.norm(balls[i].speed) < v_min:
            balls[i].update_speed(np.array([0, 0]))
        else:
            deltaV = delta_t * alpha * balls[i].speed / np.linalg.norm(balls[i].speed)
            new_speed = balls[i].speed - deltaV
            balls[i].update_speed(new_speed)


# --------------------------------------------------------------------------------------------
# -------------------------------------- IMPLEMENTATION --------------------------------------
# --------------------------------------------------------------------------------------------

def at_equilibrium(pool):
    """Renvoie True si toutes les boules sont à l'arrêt, False sinon."""
    balls = pool.balls
    number_of_balls = pool.number_of_balls
    for i in range(number_of_balls):
        if np.linalg.norm(balls[i].speed) > 0:
            return False
    return True


def update_pool(pool, delta_t):
    """Met a jour un billard nommé pool qui se trouve à un instant t à son état à l'instant t + delta_t.
    De plus, cette fonction retourne un booléen qui correspond à l'état du billard.
    C'est-à-dire True si toutes les boules sont à l'arrêt et False sinon."""
    update_position_bounceless(pool, delta_t)  # Itération naïve sans interactions physiques
    potential_collisions = collision_matrix(pool)  # Détection des chocs
    update_position_bounceless(pool, -delta_t)  # Retour à l'état initial
    if np.any(potential_collisions):
        t_0, collided_balls = first_impact(pool, potential_collisions)  # On extrait le moment du premier choc
        if t_0 < delta_t:
            friction(pool, t_0, alpha=0.3, v_min=0.05)
            update_positions_bounce(pool, t_0)  # On update les boules au moments du premier choc
            update_speed_2collidedBalls(pool, collided_balls)
            update_pool(pool, delta_t - t_0)
    else:
        friction(pool, delta_t, alpha=0.3, v_min=0.05)
        update_positions_bounce(pool, delta_t)
    return at_equilibrium(pool)


def check_exit(pool, ball):
    pos = ball.position
    pockets = pool.board.get_pockets()
    for j in range(len(pockets)):
        if np.linalg.norm(pos - pockets[j]) < 2 * ball.radius:
            ball.update_state(False)


if __name__ == "__main__":
    import graphique
    import objet_game as objet_game
    import matplotlib.pyplot as plt
    from functools import partial

    billard = objet_game.Pool('americain')
    billard.balls[0].update_speed(np.array([2.01, 2]))

    ani = graphique.trace(billard, partial(update_pool, billard, 0.02), objet_game.Cue(0.2))
    plt.show()
