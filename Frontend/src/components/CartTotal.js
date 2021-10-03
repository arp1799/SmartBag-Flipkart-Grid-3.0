import React,{useContext} from 'react';
import {Box,Button,makeStyles, Typography} from '@material-ui/core'
import { CartContext } from './Cart';

const useStyles=makeStyles({
    component:{
        marginLeft:15,
        background:'#fff',
        width:'27%',
        height:'50%'
    },
    header:{
        padding:'16px 24px',
        borderBottom:'1px solid #f0f0f0'
    },
    container:{
        padding:'15px 24px',
        '& > *': {
            marginBottom: 20,
            fontSize: 14
        }
    },
    price:{
        float:'right'
    },
    finalprice:{
        fontSize:18,
        fontWeight:600,
        borderTop:'1px dashed #e0e0e0',
        padding:'20px 0',
        borderBottom:'1px dashed #e0e0e0'
   },
   checkoutCart:{
    background:'#fb641b',
    color:'#fff',
    borderRadius:2,
    width:150,
    height:40,
    display:'flex',
    marginLeft:'auto'
  },
  bottom:{
    padding:'16px 22px',
    background:'#fff',
    borderTop:'1px solid #f0f0f0',
    boxShadow:'0 -2px 10px 0 rgb(0 0 0 /10%)'
  }
})


const CartTotal = () => {
    const {item,totalItem, totalAmount,totalDiscount,deliveryCharges}=useContext(CartContext)
    const classes=useStyles();
    if(item.length ===0 )
        return(<></>)
    const charges=deliveryCharges=== 0?"FREE":"₹"+deliveryCharges;

    
    return (
        <Box item className={classes.component}>
            <Box className={classes.header}>
                <Typography style={{color:'#878787'}}>Price Details</Typography>
            </Box>
            <Box className={classes.container}>
                <Typography>Price ({totalItem} items) <span className={classes.price}>₹{totalAmount}</span></Typography>
                <Typography>Discount <span className={classes.price}>-₹{totalDiscount}</span> </Typography>
                <Typography>Delivery Charges <span className={classes.price}>{charges}</span></Typography>
                <Typography className={classes.finalprice}>Total Amount <span className={classes.price}>₹{deliveryCharges+totalAmount-totalDiscount}</span></Typography>
                <Typography style={{color:'green'}}>You will save ₹{totalDiscount-deliveryCharges>0 && totalDiscount-deliveryCharges} {totalDiscount-deliveryCharges < 0 && totalDiscount} on this order</Typography>
            </Box>
            <Box className={classes.bottom}>
                <Button variant='contained' className={classes.checkoutCart}>
                    Checkout
                </Button>
            </Box>
        </Box>
    )
};

export default CartTotal;
