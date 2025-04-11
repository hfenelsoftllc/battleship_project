from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple


# Ship Class
class Ship:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.hits = set()

    def is_sunk(self):
        return self.hits == set(self.coordinates)

    def register_hit(self, coord):
        if coord in self.coordinates:
            self.hits.add(coord)


# Grid Class
class Grid:
    def __init__(self, size=10):
        self.size = size
        self.cells = [["-" for _ in range(size)] for _ in range(size)]
        self.ships = []

    def add_ship(self, ship):
        self.ships.append(ship)
        for coord in ship.coordinates:
            x, y = coord
            self.cells[x][y] = "S"

    def track_shot(self, coord):
        x, y = coord
        if self.cells[x][y] == "S":
            self.cells[x][y] = "H"
            for ship in self.ships:
                ship.register_hit(coord)
                if ship.is_sunk():
                    return f"Hit and sunk {ship.name}!"
            return "Hit!"
        elif self.cells[x][y] == "-":
            self.cells[x][y] = "M"
            return "Miss!"
        else:
            return "Already targeted!"


# Player Class
class Player:
    def __init__(self, name):
        self.name = name
        self.grid = Grid()
        self.shots = []

    def fire_shot(self, coord):
        if coord in self.shots:
            return "Invalid: You've already targeted this coordinate!"
        self.shots.append(coord)
        return self.grid.track_shot(coord)

    def check_win(self):
        return all(ship.is_sunk() for ship in self.grid.ships)


# GameManager Class
class GameManager:
    def __init__(self, players):
        self.players = players
        self.current_turn = 0

    def notify_sink(self, ship):
        print(f"{ship.name} has been sunk!")

    def evaluate_win(self):
        for player in self.players:
            if player.check_win():
                return f"{player.name} wins!"
        return "Game continues..."

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)


# Pydantic Models
class ShipModel(BaseModel):
    name: str
    coordinates: List[Tuple[int, int]]


class FireShotModel(BaseModel):
    coord: Tuple[int, int]


class GridConfig(BaseModel):
    size: int
    ships: List[ShipModel]


# FastAPI Initialization
app = FastAPI(
    title="Battleship Game API",
    description="API for managing the Battleship game. Players can initialize grids, fire shots, and check game status.",
    version="1.0.0",
    contact={
        "name": "Battleship Game Support",
        "email": "hfenelsoftllc@gmail.com",
    },
    license_info={
        "name": "MIT License",
    },
)
# Add CORS middleware
origins = [
    "http://localhost:3000",  # Allow local frontend development
    "https://hfenelsoftllc.com",  # Allow your deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create Game Manager and Players
player1 = Player("Player 1")
player2 = Player("Player 2")
game_manager = GameManager([player1, player2])


# API Endpoints
@app.post(
    "/initialize-grid/{player_name}",
    summary="Initialize Player Grid",
    tags=["Battleship Setup"]
)
def initialize_grid(player_name: str, config: GridConfig):
    """
    Initialize a player's grid with ships and size.

    - **player_name**: Name of the player (e.g., Player 1, Player 2).
    - **config**: Configuration object containing the grid size and list of ships.
    """
    player = next((p for p in game_manager.players if p.name == player_name), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player.grid = Grid(config.size)
    for ship_data in config.ships:
        ship = Ship(ship_data.name, ship_data.coordinates)
        player.grid.add_ship(ship)
    return {"message": f"Grid initialized for {player_name}"}


@app.post("/fire-shot/{player_name}", summary="Fire Shot", tags=["Gameplay"])
def fire_shot(player_name: str, shot: FireShotModel):
    """
    Fire a shot at the opponent's grid.

    - **player_name**: Name of the player firing the shot.
    - **shot.coord**: Coordinate to target (e.g., [1,1]).
    """
    player = next((p for p in game_manager.players if p.name == player_name), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    result = player.fire_shot(shot.coord)
    if result == "Hit and sunk":
        game_manager.notify_sink(shot.coord)
    return {"result": result}


@app.get(
    "/check-win/{player_name}", summary="Check Win Condition", tags=["Game Status"]
)
def check_win(player_name: str):
    """
    Check if the given player has won the game.

    - **player_name**: Name of the player to check for win conditions.
    """
    player = next((p for p in game_manager.players if p.name == player_name), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    if player.check_win():
        return {"message": f"{player_name} wins!"}
    return {"message": "Game continues"}


@app.post("/next-turn/", summary="Next Player's Turn", tags=["Gameplay"])
def next_turn():
    """
    Advance to the next player's turn.
    """
    game_manager.next_turn()
    return {
        "message": f"It's now {game_manager.players[game_manager.current_turn].name}'s turn"
    }
