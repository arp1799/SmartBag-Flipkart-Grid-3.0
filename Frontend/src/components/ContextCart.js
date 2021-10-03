import React, { useContext } from "react";
import {Box,Button,makeStyles, Typography} from '@material-ui/core'
import Items from "./Items";
import { CartContext } from "./Cart";
import EmptyCart from "./EmptyCart";


const useStyles=makeStyles(theme=>({
  leftcomponet:{
    width:'100%',
    
  },
  header:{
    padding:'15px 24px',
    background:'#fff'
  },
  clearCart:{
    background:'red',
    color:'#fff',
    borderRadius:2,
    width:140,
    height:35,
    display:'flex',
    marginLeft:'auto'
  },
  bottom:{
    padding:'16px 22px',
    background:'#fff',
    borderTop:'1px solid #f0f0f0',
    boxShadow:'0 -2px 10px 0 rgb(0 0 0 /10%)'
  }
}));
const ContextCart = () => {
  const { item, clearCart, totalItem} = useContext(CartContext);
  const classes=useStyles();

  // if cart is empty
  if (item.length === 0) {
    return (
      <>
        <EmptyCart name="Shopping Cart"/>
      </>
    );
  }
// if there are items in cart
  return (
    <>
      <Box  className={classes.leftcomponet}>
        <Box className={classes.header}>
          <Typography style={{fontWeight:600,fontSize:18}}>My Basket ({totalItem})</Typography>
        </Box>
        
              {item.map((curItem) => {
                return <Items key={curItem.id} {...curItem} />;
              })}
        <Box className={classes.bottom}>
          <Button variant='contained' className={classes.clearCart} onClick={clearCart}>
              Clear Cart
          </Button>
        </Box>
      </Box>      

      
    </>
  );
};

export default ContextCart;
