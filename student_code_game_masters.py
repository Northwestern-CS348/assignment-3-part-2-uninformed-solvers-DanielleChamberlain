from game_master import GameMaster
from read import *
import read, copy
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        peg = read.parse_input("fact: (on ?x ?y)")
        p1 = []
        p2 = []
        p3 = []
        for f in self.kb.facts:
            binding = match(f.statement, peg.statement)
            if binding:
                p = (binding.bindings_dict.get('?y'))
                b = (binding.bindings_dict.get('?x'))
                if(p == 'peg1'):
                    p1.append(int(b[4]))
                    p1.sort()
                elif (p == 'peg2'):
                    p2.append(int(b[4]))
                    p2.sort()
                elif (p == 'peg3'):
                    p3.append(int(b[4]))
                    p3.sort()
        ans = (tuple(p1), tuple(p2) , tuple(p3))
        return ans

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        if self.kb.kb_ask(Fact(movable_statement)):
            move = read.parse_input("fact: (movable ?d ?s ?f)")
            binding = match(movable_statement, move.statement)
            d = binding.bindings_dict.get('?d')
            s = binding.bindings_dict.get('?s')
            f = binding.bindings_dict.get('?f')
            f1 = read.parse_input('fact: (empty {!s})'.format(f))
            f2 = read.parse_input('fact: (Top ?q {!s})'.format(d))
            d1 = read.parse_input('fact: (onTop {!s} ?l)'.format(d))
            emptyf = False
            topoff = ''
            below = ''
            for z in self.kb.facts:
                top = match(z.statement, f2.statement)
                bb = match(z.statement, d1.statement)
                if match(z.statement,f1.statement):
                    emptyf = True
                if top:
                    topoff = top.bindings_dict.get('?q')
                if bb:
                    below = bb.bindings_dict.get('?l')
            remove1 = read.parse_input('fact: (onTop {!s} {!s})'.format(d, below))
            remove2 = read.parse_input('fact: (Top {!s} {!s})'.format(d, s))
            add3 = read.parse_input('fact: (Top {!s} {!s})'.format(d, f))
            self.kb.kb_assert(add3)
            self.kb.kb_retract(remove1)
            self.kb.kb_retract(remove2)
            if emptyf:
                remove3 = read.parse_input('fact: (empty {!s})'.format(f))
                self.kb.kb_retract(remove3)
                add4 = read.parse_input('fact: (onTop {!s} base1)'.format(d))
                self.kb.kb_assert(add4)
            if topoff != '':
                remove4 = read.parse_input('fact: (Top{!s} {!s})'.format(topoff, f))
                self.kb.kb_retract(remove4)
                add4 = read.parse_input('fact: (onTop {!s} topoff)'.format(d))
                self.kb.kb_assert(add4)
            if 'base' in below:
                add1 = read.parse_input('fact: (empty {!s})'.format(s))
                self.kb.kb_assert(add1)
            if 'disk' in below:
                add2 = read.parse_input('fact: (Top {!s} {!s})'.format(below, s))
                self.kb.kb_assert(add2)
        else:
            print("error")
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        row = read.parse_input("fact: (loc ?t ?x ?y)")
        r1 = [0,0,0]
        r2 = [0,0,0]
        r3 = [0,0,0]
        for f in self.kb.facts:
            binding = match(f.statement, row.statement)
            if binding:
                y = binding.bindings_dict.get('?y')
                x = int(binding.bindings_dict.get('?x')[3]) - 1
                t = binding.bindings_dict.get('?t')
                if(t == 'empty'):
                    tr = -1
                else:
                    tr = int(t[4])
                if (y == 'pos1'):
                    r1[int(x)] = tr
                elif (y == 'pos2'):
                    r2[int(x)] = tr
                elif (y == 'pos3'):
                    r3[int(x)] = tr
        ans = (tuple(r1), tuple(r2), tuple(r3))
        return ans

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        if self.kb.kb_ask(Fact(movable_statement)):
            move = read.parse_input("fact: (movable ?t ?x ?y ?fx ?fy)")
            binding = match(movable_statement, move.statement)
            t = binding.bindings_dict.get('?t')
            x = binding.bindings_dict.get('?x')
            y = binding.bindings_dict.get('?y')
            fx = binding.bindings_dict.get('?fx')
            fy = binding.bindings_dict.get('?fy')
            remove1 = read.parse_input('fact: (loc empty {!s} {!s})'.format(fx, fy))
            remove2 = read.parse_input('fact: (loc {!s} {!s} {!s})'.format(t, x, y))
            add1 = read.parse_input('fact: (loc empty {!s} {!s})'.format(x, y))
            add2 = read.parse_input('fact: (loc {!s} {!s} {!s})'.format(t, fx, fy))
            self.kb.kb_retract(remove1)
            self.kb.kb_retract(remove2)
            self.kb.kb_assert(add1)
            self.kb.kb_assert(add2)
        else:
            print("error")

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
