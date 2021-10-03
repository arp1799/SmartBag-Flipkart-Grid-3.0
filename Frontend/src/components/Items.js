import React, { useContext } from "react";
import clsx from 'clsx';
import {Box, Button, ButtonGroup, Card,makeStyles, Typography} from '@material-ui/core'
import SaverPack from './SaverPack'
import { CartContext } from "./Cart";
// import { findByLabelText } from "@testing-library/react";

const useStyles=makeStyles({
  component:{
    display:'flex',
    borderRadius:0,
    border:'1px solid #f0f0f0'
  },
  leftcomponent:{
    margin:20
  },
  rightcomponent:{
    marginTop:20
  },
  smallText:{
    fontSize:14
  },
  greycolor:{
    color:'#878787'
  },
  mainprice:{
    fontSize:18,
    fontWeight:600
  },
  productimage:{
    height:110,
    width:110
  },
  removeButton:{
    marginTop:5,
    fontSize:15,
    color:'rgb(17,17,17)',
    "&:hover":{
      color:'#878787'
    }
  },
  quantityComponent:{
    margin: '25px 50px auto auto'
  },
  quantityButton:{
    borderRadius:'40%'
  },
  spn:{
    marginLeft:'10px',
    fontWeight:700,
    color:'#2874f0',
  }
})
const Items = ({ id, description, title, img, price,mrp, quantity,sponsored }) => {
  const { removeItem, increment, decrement } = useContext(CartContext);
  const classes=useStyles();

  return (
    <>
    <Card className={classes.component}>
    
      <Box className={classes.leftcomponent}>
        <img className={classes.productimage} src={img} alt="product" />
      </Box>
      <Box className={classes.rightcomponent}>
        <Typography style={{fontWeight:'600'}}>{title}</Typography>
        <Typography className={clsx(classes.smallText,classes.greycolor)} style={{marginTop:10}}>{description} 
          {/* loop on saver pack products, here only done for one product and even hardcored */}
          {sponsored==="true" && <span ><SaverPack title={title} id={id} /></span>}
        </Typography>
        <Typography style={{margin:'20px 0'}}>
          {/* price */}
          <span className={classes.mainprice}>₹{price}</span>&nbsp;&nbsp;&nbsp;
          {/* mrp */}
          <span className={classes.greycolor}><strike>₹{mrp}</strike></span> &nbsp;&nbsp;&nbsp;
          {/* discount */}
          <span style={{color:'green'}}>{Math.floor(100-100*(price/mrp))}% off</span>
        </Typography>
       
        <Button className={clsx(classes.removeButton,classes.greycolor)} onClick={() => removeItem(id)}>REMOVE</Button>
      </Box>
      {/* <Box className={classes.incdec}>
          <i className="fas fa-minus minus" onClick={() => decrement(id)}></i>
          <input type="text" placeholder={quantity} disabled />
          <i className="fas fa-plus add" onClick={() => increment(id)}></i>
      </Box> */}
      <Box className={classes.quantityComponent}>
        <ButtonGroup className={classes.quantityComponent}>
          <Button className={classes.quantityButton} onClick={() => decrement(id)}>-</Button>
          <Button>{quantity}</Button>
          <Button className={classes.quantityButton} onClick={() => increment(id)}>+</Button>
        </ButtonGroup>
      </Box>
    </Card>
    </>
  );
};

export default Items;
