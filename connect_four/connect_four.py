import enum

class GridPosition(enum.Enum):
    EMPTY = 0
    RED = 1
    YELLOW = 2

class Grid:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = None
        self.initGrid()

    def getRows(self):
        return self._rows
    
    def getCols(self):
        return self._cols
    
    def getGrid(self):
        return self._grid
    
    def initGrid(self):
        self._grid = [[GridPosition.EMPTY for _ in range(self._cols)] for _ in range(self._rows)]
    
    def placePiece(self, col, pieceColour):
        if pieceColour == GridPosition.EMPTY:
            raise ValueError("Invalid piece")
        if col not in range(self._cols):
            raise ValueError("Invalid column")
        
        for row in range(self._rows - 1, -1, -1):
            if self._grid[row][col] == GridPosition.EMPTY:
                self._grid[row][col] = pieceColour
                return row
        
class Player:
    def __init__(self, name, pieceColour):
        self._name = name
        self._pieceColour = pieceColour
    
    def getName(self):
        return self._name
    
    def getPieceColour(self):
        return self._pieceColour

class Game:

    def __init__(self, grid, connectN, targetScore):
        self._grid = grid
        self._connectN = connectN
        self._targetScore = targetScore
        self._score = {}
        self._players = [
            Player("Player 1", GridPosition.RED),
            Player("Player 2", GridPosition.YELLOW)
            ]
        for p in self._players:
            self._score[p.getName()] = 0

    def playGame(self):
        winner = None
        maxScore = 0
        while maxScore < self._targetScore:
            winner = self.playRound()
            print(f"{winner.getName()} wins\n")
            maxScore = max(self._score[winner.getName()], maxScore)
            self._grid.initGrid()

        print(f"{winner.getName()} won the game")


    def playRound(self):
        while True:
            for player in self._players:
                moveRow, moveCol = self.playMove(player)
                pieceColour = player.getPieceColour()
                if self.checkWin(moveRow, moveCol, pieceColour):
                    self._score[player.getName()] += 1
                    return player


    def playMove(self, player):
        self.printBoard()
        print(f"{player.getName()}'s turn\n")
        rowCnt = self._grid.getRows()
        colCnt = self._grid.getCols()
        moveCol = int(input(f"Choose a column between {0} and {colCnt - 1}: "))
        moveRow = self._grid.placePiece(moveCol, player.getPieceColour())

        return (moveRow, moveCol)

    def checkWin(self, moveRow, moveCol, pieceColour):
        row = self._grid.getRows()
        col = self._grid.getCols()
        grid = self._grid.getGrid()

        total = 0
        for c in range(col):
            if grid[moveRow][c] == pieceColour:
                total += 1
            else:
                total = 0
            if total == self._connectN:
                return True
        
        total = 0
        for r in range(row):
            if grid[r][moveCol] == pieceColour:
                total += 1
            else:
                total = 0
            if total == self._connectN:
                return True
        
        # Check diagonal
        total = 0
        for r in range(row):
            c = row + col - r
            if c >= 0 and c < col and grid[r][c] == pieceColour:
                total += 1
            else:
                total = 0
            if total == self._connectN:
                print("diagonal found")
                return True

        # Check anti-diagonal
        total = 0
        for r in range(row):
            c = col - row + r
            if c >= 0 and c < col and grid[r][c] == pieceColour:
                total += 1
            else:
                total = 0
            if total == self._connectN:
                return True
        
        return False
        
            


    def printBoard(self):
        grid = self._grid.getGrid()
        rowCount = self._grid.getRows()
        colCount = self._grid.getCols()

        for r in range(rowCount):
            row = ""
            for c in range(colCount):
                if grid[r][c] == GridPosition.EMPTY:
                    row += "O"
                elif grid[r][c] == GridPosition.RED:
                    row += "R"
                else:
                    row += "Y"
            print(row)
        print("")

grid = Grid(2, 2)
game = Game(grid, 2, 3)
game.playGame()

    
        
