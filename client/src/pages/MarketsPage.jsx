import React, { useState, useEffect } from "react";
import ProductList from "../components/ProductList";
import { Navigation } from "../components/Navigation";
import ProductFilter from "../components/ProductFilter";

export const MarketsPage = () => {
  const [selectedOption, setSelectedOption] = useState("lastPrice");

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const renderSelectedComponent = () => {
    if (selectedOption === "lastPrice") {
      return <ProductList />;
    } else if (selectedOption === "products") {
      return <ProductFilter />;
    }
    // Agrega más casos según sea necesario
    return null;
  };
  return (
    <>
      <Navigation 
      handleOptionChange={handleOptionChange}
      selectedOption={selectedOption}
      renderSelectedComponent={renderSelectedComponent} />
     {renderSelectedComponent()}
    </>
  );
};
