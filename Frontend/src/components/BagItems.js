import React, { useContext } from "react";
import clsx from 'clsx';
import {Box, Button, Card,makeStyles, Typography,Checkbox} from '@material-ui/core'
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import { CartContext } from "./Cart";

const useStyles=makeStyles({
  component:{
    display:'flex',
    borderRadius:0,
    border:'1px solid #f0f0f0'
  },
  leftcomponent:{
    margin:20,
    display:'flex',
    flexDirection:'column'
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
  moveButton:{
    marginTop:5,
    fontSize:15,
    color:'rgb(17,17,17)',
    "&:hover":{
      color:'#878787'
    }
  },
  incdec:{
    margin: '25px 50px auto auto'
  },
  spn:{
    margin: '10px 2px',
    height: '13px',
    color:'#878787',
    "&:hover":{
      color:'#2874f0'
    }
  },
  infoIcon:{
    display:'inline-block',
    verticalAlign:'top',
    margin: '1px 0px',
    width: '14px',
    height: '12px',
    "&:hover":{
      color:'#2874f0'
    }
  }
})


const BagItems = ({ id, description, title, img, price,mrp ,getSelected,sponsored}) => {
    const {  move} = useContext(CartContext);
    const classes=useStyles();
    return (
        <>
        <Card className={classes.component}>
      <Box className={classes.leftcomponent}>
        <img className={classes.productimage} src={img} alt="product" />
        {sponsored === "TRUE" &&<span className={classes.spn}>Sponsored <span className={classes.infoIcon}><InfoOutlinedIcon fontSize="medium"/></span></span>}
      </Box>
      <Box className={classes.rightcomponent}>
        <Typography style={{fontWeight:'600'}}>{title} </Typography>
        <Typography className={clsx(classes.smallText,classes.greycolor)} style={{marginTop:10}}>{description}</Typography>
        <Typography style={{margin:'20px 0'}}>
          {/* price */}
          <span className={classes.mainprice}>₹{price}</span>&nbsp;&nbsp;&nbsp;
          {/* mrp */}
          <span className={classes.greycolor}><strike>₹{mrp}</strike></span> &nbsp;&nbsp;&nbsp;
          {/* discount */}
          <span style={{color:'green'}}>{Math.floor(100-100*(price/mrp))}% off</span>
        </Typography>
        <Button className={clsx(classes.moveButton,classes.greycolor)} onClick={() => move(id)}>Move To Basket</Button>
      </Box>
      <Box className={classes.incdec}>
          
          <Checkbox color="primary" value={id} onChange={(e)=>getSelected(e)}/>
      </Box>
    </Card>
      
    </>
    )
}
export default BagItems;
