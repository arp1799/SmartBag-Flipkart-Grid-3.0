import React,{useContext} from 'react';
import { CartContext } from "./Cart";
import {Box,makeStyles} from '@material-ui/core'
import ContextBag  from "./ContextBag";
import CartTotal from "./CartTotal";
import ContextCart from "./ContextCart";
import Navbar from "./NavBar";
import "./cartPage.css"

const useStyles=makeStyles(theme=>({
    maincomponent:{
        display:'flex',
        marginTop:55,
      padding:'30px 135px',
     
    },
    componet:{
      width:'67%',
      
    },
    body:{
        backgroundColor:'#f0f0f0'
    }
}));
const CartPage = () => {
    const classes=useStyles();
    const {item} = useContext(CartContext);
    return (
        <Box className={classes.body}>
       <Navbar item={item}/>
       <Box className={classes.maincomponent}>
        <Box  className={classes.componet}>  
                    <ContextCart />
                    <ContextBag />

        </Box>
        <CartTotal />
       </Box>
        
            
        
        </Box>
    )
}

export default CartPage;


