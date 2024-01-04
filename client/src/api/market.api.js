import axios from "axios";
// path('api/v1/products/group_products', group_products, name='group_products'),
// path('api/v1/products/last_active_price', product_list, name='product_list'),
const URL =
  process.env.NODE_ENV === "production"
    ? import.meta.env.VITE_BACKEND_URL
    : "http://localhost:8000";

console.log(URL);
const tasksApi = axios.create({
  baseURL: `${URL}/markets/api/v1/products`,
});

export const getAlProducts = () => tasksApi.get("/");
export const getAllLastPriceProduct = () => tasksApi.get("/last_active_price");
export const getAllGroupProduct = () => tasksApi.get("/group_products/");
