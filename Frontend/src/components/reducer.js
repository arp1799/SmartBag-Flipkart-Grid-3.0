export const reducer = (state, action) => {
  if (action.type === "REMOVE_ITEM") {
    return {
      ...state,
      item: state.item.filter((curElem) => {
        return curElem.id !== action.payload;
      }),
    };
  }

  if (action.type === "CLEAR_CART") {
    
    return { ...state, item: [] };
  }

  if (action.type === "INCREMENT") {
    const updatedCart = state.item.map((curElem) => {
      if (curElem.id === action.payload) {
        return { ...curElem, quantity: curElem.quantity + 1 };
      }
      return curElem;
    });

    return { ...state, item: updatedCart };
  }

  if (action.type === "DECREMENT") {
    const updatedCart = state.item
      .map((curElem) => {
        if (curElem.id === action.payload) {
          return { ...curElem, quantity: curElem.quantity - 1 };
        }
        return curElem;
      })
      .filter((curElem) => curElem.quantity !== 0);
    return { ...state, item: updatedCart };
  }

  if (action.type === "GET_TOTAL") {
    let {deliveryCharges,totalDiscount, totalItem, totalAmount } = state.item.reduce(
      (accum, curVal) => {
        let { mrp,price, quantity } = curVal;
        let updatedTotalAmount = mrp * quantity;
        accum.totalAmount += updatedTotalAmount;
        accum.totalDiscount+=mrp-price;
        accum.totalDiscount*=quantity;
        accum.totalItem += quantity;
        if(accum.totalAmount > 600)
          accum.deliveryCharges=0
        return accum;
      },
      {
        totalItem: 0,
        totalAmount: 0,
        totalDiscount:0,
        deliveryCharges:99,
      }
    );
    return { ...state,totalDiscount, totalItem, totalAmount,deliveryCharges };
  }

  if(action.type === "MOVE"){
    // console.log(state.bag)
    const moveitem=state.bag.filter((curElem)=>{return curElem.id === action.payload})
    const newCart=state.item.concat(moveitem)
    // console.log(newCart)
    const updatedBag= state.bag.filter((curElem) => {
      return curElem.id !== action.payload;
    });
    // console.log(updatedBag)
    return{...state,bag:updatedBag,item:newCart}
  }

  if(action.type === "MOVE_TO_CART"){
    let arr=[]
    // let newBag=[]
    state.bag.map((currEle)=>{
        if(action.payload.find(ele=>ele===currEle.id.toString()))
          arr.push(currEle)
      return currEle
    });
    let newBag=state.bag
    for (var i=0; i<arr.length; i++) {
      var index = undefined;
      while ((index = newBag.indexOf(arr[i])) !== -1) {
          newBag.splice(index, 1);
      }
    }
    const newCart=state.item.concat(arr)
    window.scrollTo(0, 0);
    return {...state,item:newCart,bag:newBag}    
  }

  if(action.type === "SAVE_MOVE"){
    const temp=state.item.filter((curElem)=>{return curElem.id === action.payload})
    let moveitem=[]
    moveitem.push(JSON.parse(JSON.stringify(temp[0])))
    moveitem[0].id=Math.floor(Math.random()*200)+20
    moveitem[0].price="959"
    moveitem[0].mrp="1100"
    moveitem[0].description="20 Kg"
    const newCart=state.item.concat(moveitem)
    window.scrollTo(0, 0);
    return{...state,item:newCart}
    // return {...state}
  }

  return state;
};
