import { Switch, Route } from 'react-router-dom'
import FormBase from './components/FormBase'

const App = () => {
  const onSubmit = (data) => {
    console.log(data)
  }

  const loginFields = [
    {name: "email", label: "Email:", placeholder: "login email", inputType: "email"},
  ]

  return (
    <div className="App">
      <Switch>
        <Route exact path="/">
          <div className="container">
            <div className="d-flex justify-content-center align-items-center mt-5">
              <div className="w-50">
                <FormBase fields={loginFields} onSubmit={onSubmit}/>
              </div>
            </div>
          </div>
        </Route>
      </Switch>
    </div>
  )
}

export default App
