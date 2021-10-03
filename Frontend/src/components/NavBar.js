import React from 'react';
import {Toolbar,makeStyles, AppBar, Typography,Box,Badge} from '@material-ui/core'
import { ShoppingCart } from '@material-ui/icons';

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
  container: {
    display: 'flex',
    float:'right'
    }
  
})

const NavBar = ({item}) => {
     const classes=useStyles();
    return (
        <AppBar className={classes.header}>
          <Toolbar>
            
              <Typography className={classes.logo}>Flipkart</Typography>
              <Typography className={classes.sublogo}>Grocery</Typography>
              <span style={{ margin: '0 5% 0 auto' }}>
              <Box className={classes.container}>
                <Badge badgeContent={item?.length} color="secondary">
                    <ShoppingCart />
                </Badge>
              </Box>
              </span>
           
          </Toolbar>

          
        </AppBar>


    )
}

export default NavBar
