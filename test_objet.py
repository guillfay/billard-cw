from objet import Ball, Board, Pool, Cue
import numpy as np
import pytest

# utiliser la commande ERROR: file or directory not found: test_*.py

def test_ball_init():
    ball=Ball(1,np.array([2, 3]))
    assert ball.number==1
    assert ball.radius==0.0286
    assert ball.mass==0.162
    assert (ball.position==np.array([2, 3])).all()
    assert (ball.speed==np.array([0,0])).all()

def test_set_size_ball():
    ball=Ball(1,np.array([2, 3]))
    ball.set_size(1,2)
    assert ball.radius==1
    assert ball.mass==2

def test_update_position():
    ball=Ball(1,np.array([2, 3]))
    ball.update_position(np.array([1,2]))
    assert (ball.position==np.array([1,2])).all()

def test_update_speed():
    ball=Ball(1,np.array([2, 3]))
    ball.update_speed(np.array([1,2]))
    assert (ball.speed==np.array([1,2])).all()

def test_str_ball():
    ball=Ball(1,np.array([2, 3]))
    assert ball.__str__()=="La boule numéro " + str(1) + " se trouve à la position " + str(np.array([2, 3])) + " et a un vecteur vitesse de " + str(np.array([0,0])) + "."

def test_board_init():
    board=Board()
    assert board.length==2.54
    assert board.width==1.27
    assert np.array_equal(board.corners,[np.array([0, 0]), np.array([0.  , 2.54]), np.array([1.27, 2.54]), np.array([1.27, 0.  ])])
    assert (board.middle==np.array([1.27/2,2.54/2])).all()

def test_get_corners():
    board=Board()
    assert np.array_equal(board.get_corners(),[np.array([0, 0]),np.array([0, 2.54]),np.array([1.27, 2.54]),np.array([1.27, 0])])

def test_get_middle():
    board=Board()
    assert (board.get_middle()==np.array([1.27/2,2.54/2])).all()

def test_set_size_board():
    board=Board()
    board.set_size(1,2)
    assert board.length==1
    assert board.width==2
    assert (board.middle==np.array([1,0.5])).all()
    assert np.array_equal(board.corners,[np.array([0, 0]),np.array([0, 1]),np.array([2, 1]),np.array([2, 0])])

def test_str_board():
    board=Board()
    assert board.__str__()=="La table a une largeur " + str(1.27) + " et de longueur " + str(2.54) + " a ses coins aux position " + str(
            [np.array([0, 0]),np.array([0, 2.54]),np.array([1.27, 2.54]),np.array([1.27, 0])]) + " et son milieu se trouve aux coordonnées" + str(np.array([1.27/2,2.54/2])) + "."

def test_pool_init():
    pool=Pool(3)
    assert pool.number_of_balls==3

def test_str_pool():
    pool=Pool(3)
    assert pool.__str__()=="La boule numéro 0 se trouve à la position [0.635 1.27 ] et a un vecteur vitesse de [0 0]. - La boule numéro 1 se trouve à la position [0.635 1.27 ] et a un vecteur vitesse de [0 0]. - La boule numéro 2 se trouve à la position [0.635 1.27 ] et a un vecteur vitesse de [0 0]. - "

def test_cue_init():
    cue=Cue(1)
    assert cue.mass==1

def test_frappe():
    cue=Cue(1)
    ball=Ball(1,np.array([2, 3]))
    cue.frappe(0,0,ball)
    assert (ball.speed==np.array([0,0])).all()