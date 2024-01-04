import React from "react";
import { Link } from "react-router-dom";

export function Navigation({ handleOptionChange, selectedOption }) {
  return (
    <div className="flex justify-between py-3 items-center">
      <Link to="/markets">
        <h1 className="font-bold text-black text-3xl mb-4">Market App</h1>
      </Link>
      <div>
        <select
          id="countries"
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          onChange={handleOptionChange}
          value={selectedOption}
        >
          <option value="lastPrice">Ultimo precio agregado</option>
          <option value="products">Productos</option>
        </select>
      </div>
    </div>
  );
}
