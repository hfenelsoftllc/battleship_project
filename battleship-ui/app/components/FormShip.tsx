import { FC, useState } from 'react';

type ShipFormProps = {
  onSubmit: (shipData: { name: string; coordinates: [number, number][] }) => void;
};

const ShipForm: FC<ShipFormProps> = ({ onSubmit }) => {
  const [name, setName] = useState('');
  const [coordinates, setCoordinates] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const coordArray: [number, number][] = coordinates.split(';').map(coord => {
      const [x, y] = coord.split(',').map(Number);
      return [x, y];
    });
    onSubmit({ name, coordinates: coordArray });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input id="shipName"
        type="text"
        placeholder="Ship Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="border p-2 rounded w-full"
        required
      />
      <input id="coordinate"
        type="text"
        placeholder="Coordinates (e.g., 0,0;0,1)"
        value={coordinates}
        onChange={(e) => setCoordinates(e.target.value)}
        className="border p-2 rounded w-full"
        required
      />
      <button id="btnAddShip" type="submit" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
        Add Ship
      </button>
    </form>
  );
};

export default ShipForm;
