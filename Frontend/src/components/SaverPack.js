import React, { useContext } from "react";
import Popover from '@material-ui/core/Popover';
import PopupState, { bindTrigger, bindPopover } from 'material-ui-popup-state';
import {Box,makeStyles, Typography} from '@material-ui/core'
import AddShoppingCartOutlinedIcon from '@material-ui/icons/AddShoppingCartOutlined';
import { CartContext } from "./Cart";

const useStyles=makeStyles({
  desc:{
    color:"#878787",
    fontWeight:600,
    marginLeft:'4px',
    fontSize:'14px'
  },
  price:{
    color:'green',
    fontSize:'14px'
  },
  icon:{
    display: 'flex',
    float:'right',
    marginTop:'4px'
  },
  head:{
    fontSize:'13px',
    fontWeight:600
  }
})

export default function PopoverPopupState({title,id}) {
  
  const { saver_pack_move } = useContext(CartContext);
  const classes=useStyles();

  
  return (
    <PopupState variant="popover" popupId="demo-popup-popover">
      {(popupState) => (
        <>
          <i style={{color:'green' ,marginTop:10,marginLeft:10,fontSize:'14px',fontWeight:600}} variant="contained" color="primary" {...bindTrigger(popupState)}>
            saver pack
          </i>
          <Popover
            {...bindPopover(popupState)}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'center',
            }}
            transformOrigin={{
              vertical: 'top',
              horizontal: 'left',
            }}
          >
            <Box p={2}>
              <Typography className={classes.head}>{title}</Typography>
              <Typography>
                <span className={classes.desc}>20Kg</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <span className={classes.price}>₹959</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                {/* instead of saver_pack_move use move to cart reducer */}
                <span className={classes.icon}> <AddShoppingCartOutlinedIcon color="action" fontSize="small"  onClick={() => saver_pack_move(3)}/> </span>
              </Typography>
            </Box>
          </Popover>
        </>
      )}
    </PopupState>
  );
}