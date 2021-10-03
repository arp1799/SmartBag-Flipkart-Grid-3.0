import React, { useContext,useState} from 'react'
import {Box,makeStyles, Typography,Button} from '@material-ui/core'
import BagItems from "./BagItems";
import { CartContext } from "./Cart";
import EmptyCart from './EmptyCart';



const useStyles=makeStyles({
  leftcomponet:{
    marginTop:40
  },
  header:{
    padding:'15px 24px',
    background:'#fff'
  },
  clearCart:{
    background:'green',
    color:'#fff',
    borderRadius:2,
    width:250,
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
})

const ContextBag = () => {
  const classes=useStyles();
  const [selected,setSelected]=useState([]);
  const {item,movetocart, bag} = useContext(CartContext);
  
  const getSelected=(e)=>{
    let products=selected;
    let newe=[]
    if(e.target.checked === true)
    {
      products.push(e.target.value);
      newe=products;
    }else{
      newe=products.filter(ele=>ele!==e.target.value);
    }
    setSelected(newe);
  }
  
  if(bag.length === 0){
    return (
      <>
        {item.length !==0 &&
          <EmptyCart name="Shopping Bag"/>
        }
      </>
    )
  }
  return(
      <>
      <Box className={classes.leftcomponet}>
        <Box className={classes.header}>
          <Typography style={{fontWeight:600,fontSize:18}}>Smart Bag ({bag.length})</Typography>
        </Box>
        
              {bag.map((curItem) => {
                return <BagItems key={curItem.id} {...curItem} getSelected={getSelected} />;
              })}
      </Box>        
      <Box className={classes.bottom}>
          <Button className={classes.clearCart}  onClick={()=>{movetocart(selected)}}>
            Move Selected
          </Button>
        </Box>
      

      </>
  )
}
export default ContextBag;
