import pygame
import sys

# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 80
WIDTH, HEIGHT = BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()

# Load piece images
pieces = {}
for color in ["white", "black"]:
    for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
        img = pygame.image.load(f"{color}_{piece}.png")
        img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
        pieces[f"{color}_{piece}"] = img

class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        # Override this method in child classes to define custom movesets
        pass

# Add piece classes (Pawn, Knight, Bishop, Rook, Queen, King) here

class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = "pawn"

    def get_valid_moves(self, board):
        moves = []
        direction = 1 if self.color == "white" else -1
        start_row = 1 if self.color == "white" else 6

        # Forward move
        if 0 <= self.y + direction < BOARD_SIZE and not board[self.y + direction][self.x]:
            moves.append((self.x, self.y + direction))

            # Double move if pawn is at its starting position
            if self.y == start_row and not board[self.y + 2 * direction][self.x]:
                moves.append((self.x, self.y + 2 * direction))

        # Capturing moves
        for dx in [-1, 1]:
            if 0 <= self.x + dx < BOARD_SIZE and 0 <= self.y + direction < BOARD_SIZE:
                target = board[self.y + direction][self.x + dx]
                if target and target.color != self.color:
                    moves.append((self.x + dx, self.y + direction))

        return moves


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = "knight"

    def get_valid_moves(self, board):
        moves = []
        knight_moves = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]

        for dx, dy in knight_moves:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                target = board[new_y][new_x]
                if not target or target.color != self.color:
                    moves.append((new_x, new_y))

        return moves


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = "bishop"

    def get_valid_moves(self, board):
        moves = []

        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_x, new_y = self.x + dx, self.y + dy
            while 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                target = board[new_y][new_x]
                if not target:
                    moves.append((new_x, new_y))
                else:
                    if target.color != self.color:
                        moves.append((new_x, new_y))
                    break
                new_x += dx
                new_y += dy

        return moves


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = "rook"

    def get_valid_moves(self, board):
        moves = []

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = self.x + dx, self.y + dy
            while 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                target = board[new_y][new_x]
            if not target:
                moves.append((new_x, new_y))
            else:
                if target.color != self.color:
                    moves.append((new_x, new_y))
                break
            new_x += dx
            new_y += dy

        return moves

class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = "queen"

    def get_valid_moves(self, board):
        moves = []

        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = self.x + dx, self.y + dy
            while 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                target = board[new_y][new_x]
            if not target:
                moves.append((new_x, new_y))
            else:
                if target.color != self.color:
                    moves.append((new_x, new_y))
                break
            new_x += dx
            new_y += dy
        
        return moves

class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = "king"

    def get_valid_moves(self, board):
        moves = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                    target = board[new_y][new_x]
                    if not target or target.color != self.color:
                        moves.append((new_x, new_y))

        return moves
    

def create_board():
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Place pieces on the board
    # Modify this part to change the initial position of pieces

    # Pawns
    for i in range(BOARD_SIZE):
        board[1][i] = Pawn("black", 1, i)
        board[6][i] = Pawn("white", 6, i)

    # Rooks
    board[0][0] = Rook("black", 0, 0)
    board[0][7] = Rook("black", 0, 7)
    board[7][0] = Rook("white", 7, 0)
    board[7][7] = Rook("white", 7, 7)

    # Knights
    board[0][1] = Knight("black", 0, 1)
    board[0][6] = Knight("black", 0, 6)
    board[7][1] = Knight("white", 7, 1)
    board[7][6] = Knight("white", 7, 6)

    # Bishops
    board[0][2] = Bishop("black", 0, 2)
    board[0][5] = Bishop("black", 0, 5)
    board[7][2] = Bishop("white", 7, 2)
    board[7][5] = Bishop("white", 7, 5)

    # Queens
    board[0][3] = Queen("black", 0, 3)
    board[7][3] = Queen("white", 7, 3)

    # Kings
    board[0][4] = King("black", 0, 4)
    board[7][4] = King("white", 7, 4)

    return board

def draw_board(screen, board, valid_moves=None):
    valid_moves = valid_moves or []

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, WHITE if (x + y) % 2 == 0 else BROWN, rect)

            if (x, y) in valid_moves:
                pygame.draw.rect(screen, YELLOW, rect, 5)

            piece = board[y][x]
            if piece:
                screen.blit(pieces[f"{piece.color}_{piece.name}"], rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Custom Chess")

    board = create_board()
    running = True
    turn = "white"
    selected_piece = None
    valid_moves = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // SQUARE_SIZE, y // SQUARE_SIZE
                piece = board[grid_y][grid_x]

                if selected_piece:
                    if (grid_x, grid_y) in valid_moves:
                        board[selected_piece.y][selected_piece.x] = None
                        board[grid_y][grid_x] = selected_piece
                        selected_piece.x, selected_piece.y = grid_x, grid_y
                        turn = "black" if turn == "white" else "white"
                    selected_piece = None
                    valid_moves = []
                elif piece and piece.color == turn:
                    selected_piece = piece
                    valid_moves = piece.get_valid_moves(board)

        draw_board(screen, board, valid_moves)
        pygame.display.flip()

if __name__ == "__main__":
    main()
