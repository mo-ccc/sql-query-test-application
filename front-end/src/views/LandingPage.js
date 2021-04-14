import FormBase from '../components/FormBase'
import axios from 'axios'
import { useHistory } from 'react-router-dom'

const LandingPage = () => {
  let history = useHistory()

  const onSubmit = (data) => {
    axios.post(`${process.env.REACT_APP_HOST}/user`, data)
    .then(response => {
      history.push({pathname: '/test', state: {testId: response.data.tests[0].id}})
    })
    .catch(error => console.log(error))
  }

  const loginFields = [
    {name: "email", label: "Email:", placeholder: "login email", inputType: "email"},
  ]

  return (
  <div className="container">
    <div className="d-flex justify-content-center align-items-center mt-5">
      <div className="w-50">
        <FormBase fields={loginFields} onSubmit={onSubmit}/>
      </div>
    </div>
  </div>
  )
}
export default LandingPage