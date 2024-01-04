import React, { useState, useEffect } from 'react';
import { getAllGroupProduct } from '../api/market.api';

const ProductFilter = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState('');
  const [filteredProducts, setFilteredProducts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getAllGroupProduct();
        setData(res.data.products);
      } catch (error) {
        console.error('Error fetching product data:', error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const filtered = data.filter(product =>
      product.nombre_producto.toLowerCase().includes(filter.toLowerCase())
    );
    setFilteredProducts(filtered);
  }, [filter, data]);

  return (
    <div className='pt-2'>
     
<form className='py-2'>   
    <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
    <div className="relative">
        <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
            <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
            </svg>
        </div>
        <input type="search" id="default-search" 
          placeholder='Filtrar por nombre...'
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" aria-placeholder ="Search Mockups, Logos..." required />
       
    </div>
</form>

    
      {filteredProducts.length > 0 ? (
        filteredProducts.map(product => (
          <Product key={product.Ean} product={product} />
        ))
      ) : (
        <p>No hay productos que coincidan con el filtro.</p>
      )}
    </div>
  );
};

const Product = ({ product }) => {
  const datosQuery = JSON.parse(product.datos_query);

  return (
    <div className='border stroke-orange-300 px-4 py-3 mb-3'>
      <h3>{product.nombre_producto}</h3>
      <p>Cantidad de mercados diferentes: {product.cantidad_mercados}</p>
      <p>Rango de precios: {product.rango_precio}</p>
      <div>
        <h4>Datos Query:</h4>
        <ul>
          {datosQuery.map((query, index) => (
            <li key={index}>
              Producto: {query.producto}, Mercado: {query.mercado}, Precio Normal: {query.precio_normal}, Precio Descuento: {query.precio_descuento}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ProductFilter;
