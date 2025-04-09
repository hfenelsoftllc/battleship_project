type GridProps = {
  gridData: { size: number; cells: string[][] };
};

const Grid: React.FC<GridProps> = ({ gridData }) => {
  return (
    <div className="grid gap-1" style={{ gridTemplateColumns: `repeat(${gridData.size}, 30px)` }}>
      {gridData.cells.map((row, i) =>
        row.map((cell, j) => (
          <div
            key={`${i}-${j}`}
            className={`border flex items-center justify-center ${
              cell === 'H' ? 'bg-red-500' : cell === 'M' ? 'bg-gray-500' : 'bg-white'
            }`}
            style={{ width: 30, height: 30 }}
          >
            {cell}
          </div>
        ))
      )}
    </div>
  );
};

export default Grid;
