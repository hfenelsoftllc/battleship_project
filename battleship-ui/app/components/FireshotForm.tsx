import { FC, useState } from 'react';

type FireShotFormProps = {
  onSubmit: (coord: [number, number]) => void;
};

const FireShotForm: FC<FireShotFormProps> = ({ onSubmit }) => {
  const [coord, setCoord] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const coordArray: [number, number] = coord.split(',').map(Number) as [number, number];
    onSubmit(coordArray);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input  id="coordinate"
        type="text"
        placeholder="Coordinate (e.g., 1,1)"
        value={coord}
        onChange={(e) => setCoord(e.target.value)}
        className="border p-2 rounded w-full"
        required
      />
      <button id="btnSubmit" type="submit" className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600">
        Fire Shot
      </button>
    </form>
  );
};

export default FireShotForm;
