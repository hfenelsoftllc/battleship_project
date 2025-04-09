'use client';
import { useState } from 'react';
import Grid from '../app/components/Grid';
import ShipForm from '../app/components/FormShip';
import FireShotForm from '../app/components/FireshotForm';
import { initializeGrid, fireShot, checkWin, nextTurn } from '../app/utils/api';

export default function Home() {
  const [playerName] = useState('Player 1');
  const [grid] = useState({ size: 10, cells: Array(10).fill(Array(10).fill('-')) });
  const [message, setMessage] = useState('');

  const handleInitializeGrid = async (shipData: { name: string; coordinates: [number, number][] }) => {
    const config = { size: grid.size, ships: [shipData] };
    const response = await initializeGrid(playerName, config);
    setMessage(response.message);
  };

  const handleFireShot = async (coord: [number, number]) => {
    const response = await fireShot(playerName, coord);
    setMessage(response.result);
  };

  const handleCheckWin = async () => {
    const response = await checkWin(playerName);
    setMessage(response.message);
  };

 return (
    <div>
      <h1>Battleship Game</h1>
      <Grid gridData={grid} />
      <ShipForm onSubmit={handleInitializeGrid} />
      <FireShotForm onSubmit={handleFireShot} />
      <button onClick={handleCheckWin}>Check Win</button>
      <button onClick={nextTurn}>Next Turn</button>
      <p>{message}</p>
    </div>
  );
};

//export default Home;