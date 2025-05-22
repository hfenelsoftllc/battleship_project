import {FC, JSX} from 'react';

type GridProps = {
  gridData: { size: number; cells: string[][]; ships:{type:string; coordinates: [number, number][]} [] };
};

const Grid: FC<GridProps> = ({ gridData }) => {
  // Function to get the icon based on the cell value
   // Function to get the icon based on the cell value
  const getIcon = (rowIndex: number, colIndex: number): JSX.Element | null => {
    const cellShipdata = gridData.ships.find(ship => ship.coordinates.some(([x, y]) => x === rowIndex && y === colIndex));

    if (cellShipdata?.type === 'ship') {
      return <span className="text-yellow-500">🚢</span>; // Ship
    }else if(cellShipdata?.type === 'battleship'){
      return <span className="text-blue-500">🛡️</span>; // Battleship{
    }
    return null; // Empty cell
  };

  // const getIcon = (cell: string): JSX.Element | null => {
  //   switch (cell) {
  //     case 'H':
  //       return <span className="text-green-500">💥</span>; // Hit
  //     case 'M':
  //       return <span className="text-red-500">💧</span>; // Miss
  //     case 'S':
  //       return <span className="text-blue-500">🚢</span>; // Ship
  //     case 'X':
  //       return <span className="text-gray-500">🏴‍☠️</span>; // Sunk
  //     case 'B':
  //       return <span className="text-yellow-500">🛡️</span>; // Battleship
  //     default:
  //       return null; // Empty cell
  //   }
  // };
  return (
    <div className="grid gap-1 border p-4 rounded-md bg-gray-100" 
      style={{ gridTemplateColumns: `repeat(${gridData.size}, 40px)` }}>
      {gridData.cells.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <div
            key={`${rowIndex}-${colIndex}`}
            className={`flex items-center justify-center border bg-white rounded-md ${
              cell === 'H' ? 'bg-green-500' : cell === 'M' ? 'bg-red-500' : cell === 'X' ? 'bg-gray-500': cell === 'S' ? 'bg-blue-500': cell === 'B' ? 'bg-yellow-500' : 'bg-white'
            }`}
            style={{ width: 40, height: 40 }}
          >
            {getIcon(rowIndex, colIndex)}
            {/* {getIcon(cell)} */}
          </div>
        ))
      )}
    </div>
  );
};

export default Grid;
