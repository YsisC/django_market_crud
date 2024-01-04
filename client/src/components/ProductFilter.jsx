import React, { useState, useEffect } from 'react';
import { getAllGroupProduct, getAllLastPriceProduct } from '../api/market.api';

const ProductFilter = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState('');
  const [filteredProducts, setFilteredProducts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res_all = await getAllGroupProduct();
        const products = res_all.data.products;
        setFilteredProducts(products);
      } catch (error) {
        console.error('Error fetching group product data:', error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      if (filteredProducts.length > 0) {
        const updatedProducts = [...filteredProducts];
        updatedProducts.pop();
        setFilteredProducts(updatedProducts);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [filteredProducts]);

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const filtered = filteredProducts.filter(product =>
    product.nombre_producto.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className='pt-2'>
      <input
        type="text"
        placeholder="Filtrar por nombre"
        value={filter}
        onChange={handleFilterChange}
      />
      {filtered.length > 0 ? (
        filtered.map(product => (
          <Product key={product.Ean} product={product} />
        ))
      ) : (
        <p>No hay productos que coincidan con el filtro.</p>
      )}
    </div>
  );
};

const Product = ({ product }) => {
  return (
    <div className='border stroke-orange-300 px-4 py-3'>
      <h3>{product.nombre_producto}</h3>
      <p>El ultimo precio: - {product.last_active_price}</p>
      {/* Agrega más detalles o información según sea necesario */}
    </div>
  );
};

export default ProductFilter;
