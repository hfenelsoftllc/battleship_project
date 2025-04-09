from fastapi import FastAPI, HTTPException
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
        self.cells = [['-' for _ in range(size)] for _ in range(size)]
        self.ships = []

    def add_ship(self, ship):
        self.ships.append(ship)
        for coord in ship.coordinates:
            x, y = coord
            self.cells[x][y] = 'S'

    def track_shot(self, coord):
        x, y = coord
        if self.cells[x][y] == 'S':
            self.cells[x][y] = 'H'
            for ship in self.ships:
                ship.register_hit(coord)
                if ship.is_sunk():
                    return f"Hit and sunk {ship.name}!"
            return "Hit!"
        elif self.cells[x][y] == '-':
            self.cells[x][y] = 'M'
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
app = FastAPI()

# Create Game Manager and Players
player1 = Player("Player 1")
player2 = Player("Player 2")
game_manager = GameManager([player1, player2])

# API Endpoints
@app.post("/initialize-grid/{player_name}")
def initialize_grid(player_name: str, config: GridConfig):
    player = next((p for p in game_manager.players if p.name == player_name), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    player.grid = Grid(config.size)
    for ship_data in config.ships:
        ship = Ship(ship_data.name, ship_data.coordinates)
        player.grid.add_ship(ship)
    return {"message": f"Grid initialized for {player_name}"}

@app.post("/fire-shot/{player_name}")
def fire_shot(player_name: str, shot: FireShotModel):
    player = next((p for p in game_manager.players if p.name == player_name), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    result = player.fire_shot(shot.coord)
    if result == "Hit and sunk":
        game_manager.notify_sink(shot.coord)
    return {"result": result}

@app.get("/check-win/{player_name}")
def check_win(player_name: str):
    player = next((p for p in game_manager.players if p.name == player_name), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    if player.check_win():
        return {"message": f"{player_name} wins!"}
    return {"message": "Game continues"}

@app.post("/next-turn/")
def next_turn():
    game_manager.next_turn()
    return {"message": f"It's now {game_manager.players[game_manager.current_turn].name}'s turn"}
