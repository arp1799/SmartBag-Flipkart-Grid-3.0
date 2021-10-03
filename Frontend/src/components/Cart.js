import React, { createContext, useReducer, useEffect } from "react";

import { products } from "./products";
import { reducer } from "./reducer";
// import { smartbag } from "./smartbag";
import CartPage from "./CartPage";


export const CartContext = createContext();



const Cart = ({smartbag}) => {
  const initialState = {
    item: products,
    bag:smartbag,
    totalAmount: 0,
    totalItem: 0,
    totalDiscount: 0,
    deliveryCharges:99,
  };
  // const [item, setItem] = useState(products);
  const [state, dispatch] = useReducer(reducer, initialState);

  // to delete the indv. elements from an Item Cart
  const removeItem = (id) => {
    return dispatch({
      type: "REMOVE_ITEM",
      payload: id,
    });
  };

  // clear the cart
  const clearCart = () => {
    return dispatch({ type: "CLEAR_CART" });
  };

  // increment the item
  const increment = (id) => {
    return dispatch({
      type: "INCREMENT",
      payload: id,
    });
  };

  // decrement the item
  const decrement = (id) => {
    return dispatch({
      type: "DECREMENT",
      payload: id,
    });
  };

  const move=(id)=>{
    return dispatch({
      type:"MOVE",
      payload:id,
    });
  };
  const movetocart=(data)=>{
    return dispatch({
      type:"MOVE_TO_CART",
      payload:data,
    });
  };
  const saver_pack_move=(id)=>{
    return dispatch({
      type:"SAVE_MOVE",
      payload:id
    });
  };
  // we will use the useEffect to update the data
  useEffect(() => {
    dispatch({ type: "GET_TOTAL" });
    // console.log("Awesome");
  }, [state.item]);

  return (
    <CartContext.Provider
      value={{ ...state, removeItem, clearCart, increment, decrement,move ,movetocart,saver_pack_move}}>
     <CartPage />
    </CartContext.Provider>
  );
};

export default Cart;
