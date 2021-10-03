import { makeStyles, Typography, Box } from '@material-ui/core';

const useStyle = makeStyles({
    component: {
        width: '100%',
        height: '65vh',
        background: '#fff',
        margin: '80px 140px'
    },
    image: {
        width: '30%'
    },
    container: {
        textAlign: 'center',
        paddingTop: 70
    }
})


const EmptyCart = ({name}) => {
    const imgurl = 'https://rukminim1.flixcart.com/www/800/800/promos/16/05/2019/d438a32e-765a-4d8b-b4a6-520b560971e8.png?q=90';
    const classes = useStyle();

    return (
        
        <Box className={classes.component}>
            <Box className={classes.container}>
                <img src={imgurl} alt="empty" className={classes.image} />
                <Typography>Your {name} Is Empty!</Typography>
                {name==="Shopping Cart" && <span>Add items to it now.</span>}
            </Box>
        </Box>
    )
}

export default EmptyCart;