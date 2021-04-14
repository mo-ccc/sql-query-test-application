import { Switch, Route } from 'react-router-dom'
import LandingPage from './views/LandingPage.js'
import TestPage from './views/TestPage.js'


const App = () => {
  return (
    <div className="App">
      <Switch>
        <Route exact path="/">
          <LandingPage />
        </Route>
        <Route exact path="/test">
          <TestPage />
        </Route>
      </Switch>
    </div>
  )
}

export default App
