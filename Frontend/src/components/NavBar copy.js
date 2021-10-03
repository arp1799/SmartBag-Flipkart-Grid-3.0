import React,{useContext} from 'react';
import {Toolbar,makeStyles, AppBar, Typography,Box,Badge,Button} from '@material-ui/core'
import { CartContext } from "./Cart";

const useStyles= makeStyles({
  header:{
    backgroundColor:'#2874f0',
    height:55
  },
  logo:{
    width:75,
    fontSize:20,
    marginLeft:120
  },
  sublogo:{
    fontSize:14,
    width:10,
    marginLeft:2,
    fontStyle:'italic'
  },
  container:{
    marginLeft:12
  },
  cartIcon:{
    display: 'flex',
  textAlign: 'end',
  marginRight: '2rem',
  alignItems: 'center',
  position: 'relative',
  justifyContent: 'flex-end',
  float:'right'
  },
  cartImage:{
    width: '3rem',
  height: '3rem',
  color: '#2f80ed'
  },
  cartImageText:{
    position: 'absolute',
    width: '2.5rem',
    height: '2.5rem',
    right: '-1.2rem',
    top: '0.9rem',
    borderRadius: '50%',
    background: '#99cbf7',
    color: '#fff',
    boxSizing:'border-box',
    fontSize: '1.6rem',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    color: 'orange'
  }

})

const NavBar = () => {
     const {totalItem } = useContext(CartContext);
     const classes=useStyles();
    return (
        <AppBar className={classes.header}>
          <Toolbar>
            
              <Typography className={classes.logo}>Flipkart</Typography>
              <Typography className={classes.sublogo}>Grocery</Typography>
            

              <Box className={classes.cartIcon}>
                <img className={classes.cartImage} src="./images/cart.png" alt="cart" />
                <p className={classes.cartImageText}>{totalItem}</p>
              </Box>
              
           
          </Toolbar>

          
        </AppBar>


    )
}

export default NavBar
