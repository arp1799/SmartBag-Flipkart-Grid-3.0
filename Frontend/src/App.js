import React from "react";
import Landing from "./components/main";
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
const App = () => {
  return (
    <Router>
           <div className="App">
            <Switch>
              <Route  path='/:id?' component={Landing}></Route>
            </Switch>
          </div>
       </Router>
  );
};


export default App;
