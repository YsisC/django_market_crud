import React, { useState, useEffect } from 'react';
import { getAllGroupProduct, getAllLastPriceProduct } from '../api/market.api';

const ProductList = () => {
  const [data, setData] = useState([]);
 
  useEffect(() => {
    async function fetchData() {
      try {
        const res = await getAllLastPriceProduct();
     
        setData(res.data.products);
       
        // console.log(data)
      } catch (error) {
        console.error('Error fetching product data:', error);
      }
    }

    fetchData();
  }, []);

  return (
    <div className='pt-2'>
      {data.length > 0 ? (
        data.map(product => (
          <Product key={product.EAN} product={product} />
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
      <h3>{product.name}</h3>
      <p>El ultimo precio: - {product.last_active_price}</p>
      <p></p>
    </div>
  );
};

export default ProductList;
