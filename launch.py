import argparse
from objet import *
from graphique import *
from dynamic import *
from functools import partial


def main():
    parser = argparse.ArgumentParser(description='Launch BITE simulation')
    parser.add_argument('number of balls', metavar='n', type=int, nargs='+',
                        help='number of balls on the pool')
    parser.add_argument('mass', metavar='m', type=float, nargs='+',
                        help='mass of the cue')
    parser.add_argument('energy', metavar='e', type=float, nargs='+',
                        help='energy of the cue')
    parser.add_argument('angle', metavar='a', type=float, nargs='+',
                        help='angle of the cue en degrés')
    parser.add_argument('AfficherAnimation', metavar='AfficherAnimation', type=bool, nargs='+',
                        help='Faut-il afficher l animation ?')

    args = parser.parse_args()
    variable = vars(args)
    mass = variable["mass"][0]
    n_balls = variable["number of balls"][0]
    energy = variable["energy"][0]
    angle = variable["angle"][0]
    affichage = variable["AfficherAnimation"][0]

    # Création du billard
    pool = Pool(n_balls)
    cue = Cue(mass)
    deltaT = np.sqrt(pool.balls[0].radius / (2 * energy / mass))
    cue.frappe(energy, angle * np.pi / 180, pool.balls[0])

    # Animation
    if affichage:
        animation = trace(pool, partial(update_pool, pool=pool, deltaT=1 / 60))
        plt.show()


if __name__ == '__main__':
    main()
