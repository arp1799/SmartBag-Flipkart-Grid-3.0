import React,{useState} from 'react'
import Navbar from "./NavBar";
import { TextField, Box, Button, makeStyles, Typography } from '@material-ui/core';
import Cart from "./Cart";
const useStyles=makeStyles(theme=>({
    
    component: {
      height: '70vh',
      width: '90vh',
      maxWidth: 'unset !important',
      marginTop:100,
      marginLeft:400,
      borderRadius: 2,
      boxShadow: '0 2px 4px 0 rgb(0 0 0 / 50%)',
      background: '#fdfdfd',
      
  },
  image: {
      backgroundImage: `url(${'https://static-assets-web.flixcart.com/www/linchpin/fk-cp-zion/img/login_img_c4a81e.png'})`,
      background: '#2874f0',
      backgroundPosition: 'center 85%',
      backgroundRepeat: 'no-repeat',
      height: '70vh',
      width: '40%',
      padding: '45px 35px',
      '& > *': {
          color: '#FFFFFF',
          fontWeight: 600
      }
  },
  login: {
      padding: '25px 35px',
      display: 'flex',
      flex: 1,
      flexDirection: 'column',
      '& > *': {
          marginTop: 20
      }
  },
  loginbtn: {
      textTransform: 'none',
      background: '#FB641B',
      color: '#fff',
      height: 48,
      borderRadius: 2
  },
  requestbtn: {
      textTransform: 'none',
      background: '#fff',
      color: '#2874f0',
      height: 48,
      borderRadius: 2,
      boxShadow: '0 2px 4px 0 rgb(0 0 0 / 20%)'
  },
  text: {
      color: '#878787',
      fontSize: 12
  },
  createText: {
      margin: 'auto 0 5px 0',
      textAlign: 'center',
      color: '#2874f0',
      fontWeight: 600,
      fontSize: 14,
      cursor: 'pointer'
  },
  error: {
      fontSize: 10,
      color: '#ff6161',
      lineHeight: 0,
      marginTop: 10,
      fontWeight: 600
  }
}));

const Landing = (props) => {
    const classes=useStyles();
    const [smartbag, setBag] = useState([])
    const [userid, setUserid] = useState(0)
    const [temp,changevalue] = useState(0)
    
    // on submit function
    const fetchPredictions =async e => {
      const data = {user_id: temp};
      var prediction=await fetch('/predict', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' },
      }).then(res =>res.json())
      console.log(prediction.predictions)
      setBag(prediction.predictions);
      setUserid(temp);
    }


    return (
      <div>
          {userid?<div></div>:<div>
          <Navbar item={[]}/>

          <div className={classes.component} >
                <Box style={{display: 'flex'}}>
                    <Box className={classes.image}>
                        <Typography variant="h5">Flipkart Grid 3.0</Typography>
                        <Typography style={{marginTop: 20}}>SmartBag - Enter into the world of smart shopping </Typography>
                    </Box>
                    
                        <Box className={classes.login}>
                            <TextField onChange={(e) => changevalue(e.target.value)} name='user_id' label='Enter User Id :' />
                            <Typography className={classes.text}>By continuing, you agree to Flipkart's Terms of Use and Privacy Policy.</Typography>
                            <Button className={classes.loginbtn} onClick={() => fetchPredictions()} >View SmartBag</Button>
                            
                        </Box> 

                    
                </Box>
            </div>
          </div>}
        { userid ? <Cart smartbag={smartbag}/>:<div></div>}
      </div>
    )
}

export default Landing;

