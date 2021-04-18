import { Switch, Route, Redirect } from 'react-router-dom'
import LandingPage from './views/LandingPage.js'
import TestPage from './views/TestPage.js'
import ThankYouPage from './views/ThankYouPage.js'


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
        <Route exact path="/finish">
          <ThankYouPage />
        </Route>
        <Route exact path="/404">
          <h1>404</h1>
        </Route>
        <Route>
          <Redirect to="/404" />
        </Route>
      </Switch>
    </div>
  )
}

export default App
