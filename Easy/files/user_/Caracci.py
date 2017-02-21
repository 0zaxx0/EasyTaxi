import sys

class KnightsTour:
    def __init__(self, width, height):
        self.w = width
        self.h = height

        self.board = []
        self.generate_board()

    def generate_board(self):
        """
        Creates a nested list to represent the game board
        """
        for i in range(self.h):
            self.board.append([0]*self.w)

    def print_board(self):
        print ("  ")
        print ("------")
        for elem in self.board:
            print (elem)
        print ("------")
        print ("  ")

    def generate_legal_moves(self, cur_pos, llegada):
        """
        Generates a list of legal moves for the knight to take next
        """
        possible_pos = []
        move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                        (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for move in move_offsets:
            new_x = cur_pos[0] + move[0]
            new_y = cur_pos[1] + move[1]

            if (new_x >= self.h):
                continue
            elif (new_x < 0):
                continue
            elif (new_y >= self.w):
                continue
            elif (new_y < 0):
                continue
            else:
                possible_pos.append((new_x, new_y))
        return possible_pos

    def sort_lonely_neighbors(self, to_visit, llegada, n):
        """
        It is more efficient to visit the lonely neighbors first,
        since these are at the edges of the chessboard and cannot
        be reached easily if done later in the traversal
        """
        neighbor_list = self.generate_legal_moves(to_visit, llegada)
        empty_neighbours = []

        for neighbor in neighbor_list:
            np_value = self.board[neighbor[0]][neighbor[1]]
            if np_value == 0:
                empty_neighbours.append(neighbor)

        scores = []
        for empty in empty_neighbours:
            score = [empty, 0]
            moves = self.generate_legal_moves(empty, llegada)
            for m in moves:
                if self.board[m[0]][m[1]] == 0:
                    score[1] += 1
            scores.append(score)
        scores_sort = sorted(scores, key = lambda s: s[1])
        sorted_neighbours = [s[0] for s in scores_sort]
        if len(sorted_neighbours)==0:
            print("No existe solucion porque no quedan movimientos que lleven a una posicion no usada antes")
            sys.exit(0)
        if sorted_neighbours[0]==llegada:
            if n!= self.w * self.h - 1:
                if len(sorted_neighbours)!=1:
                    sorted_neighbours[0]=sorted_neighbours[1]
                else:
                    print ("No existe solucion porque el siguiente movimiento solo es posible al espacio de termino, y no es el movimiento final")
                    sys.exit(0)

        return sorted_neighbours

    def tour(self, n, path, to_visit, llegada):
        """s
        Recursive definition of knights tour. Inputs are as follows:
        n = current depth of search tree
        path = current path taken
        to_visit = node to visit
        """
        self.board[to_visit[0]][to_visit[1]] = n
        path.append(to_visit) #append the newest vertex to the current point
        print("Salto numero:",n," ---->  Posicion actual:",to_visit)
        print("Tablero:")
        self.print_board()
        if n == self.w * self.h: #if every grid is filled
            print("El Caballo recorrio todo el tablero!")
            print("Su posicion final: ", to_visit)
            print ("El camino que recorrio fue: ",path)

            sys.exit(1)

        else:
            sorted_neighbours = self.sort_lonely_neighbors(to_visit, llegada, n)
            for neighbor in sorted_neighbours:
                self.tour(n+1, path, neighbor, llegada)

            #If we exit this loop, all neighbours failed so we reset
            self.board[to_visit[0]][to_visit[1]] = 0
            try:
                path.pop()
                print ("Going back to: ", path[-1])
            except IndexError:
                print ("No path found")
                sys.exit(1)

if __name__ == '__main__':
    print("Ingrese la dimension del tablero, los numeros tienen que ser mayor que 0, OJO: tableros de dimension mayor a 30x30 pueden ocasionar problemas de recursividad excedida")
    vertical=int(input("Tamano vertical: "))
    horizontal=int(input("Tamano horizontal: "))
    if vertical < 1 or horizontal < 1:
        print("el tamano del tablero no puede contener numeros menores a 1")
        sys.exit(0)
    kt = KnightsTour(horizontal, vertical)
    print("\nLa posiciones estan escritas de la forma (X,Y) X indica los espacios verticales, Y indica los espacios horizontales")
    print("\nIngrese las coordenadas de inicio, X tiene que ser un numero entre 0 y",vertical-1,", Y tiene que ser un numero entre 0 y",horizontal-1,"\n")
    x=int(input("X: "))
    y=int(input("Y: "))
    if x not in range (0,vertical):
        print("Las coordenadas de X no se encuentran entre 0 y ",vertical-1)
        sys.exit(0)
    if y not in range (0,horizontal):
        print("Las coordenadas de Y no se encuentran entre 0 y ",horizontal-1)
        sys.exit(0)
    print("\nIngrese las coordenadas de termino, X tiene que ser un numero entre 0 y",vertical-1,", Y tiene que ser un numero entre 0 y",horizontal-1,
          "\nsi cualquiera de estas 2 condiciones no se cumple el programa asigna su propia coordenada de termino"
          "\n(esto se puede usar para encontrar si existe solucion ya que si el programa no encuentra ni una coordenada de termino no se puede resolver)\n")
    a=int(input("X: "))
    b=int(input("Y: "))
    print("")
    if x==y and b==y:
        print("el algoritmo del caballo esta hecho de manera que al tocar una posicion no se puede volver a esta por lo tanto no puede introducir estas coordenadas de termino ")
        sys.exit(0)
    kt.tour(1, [], (x,y) , (a,b) )
    kt.print_board()
