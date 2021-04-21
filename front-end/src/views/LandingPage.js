import FormBase from '../components/FormBase'
import axios from 'axios'
import { useHistory } from 'react-router-dom'
import * as yup from 'yup'
import { yupResolver } from '@hookform/resolvers/yup'

const LandingPage = () => {
  let history = useHistory()

  const validation_schema = yup.object().shape({
    email: yup.string().email().required()
  })

  const onSubmit = (data) => {
    axios.post(`${process.env.REACT_APP_HOST}/user`, data)
    .then(response => {
      history.push({pathname: '/test', state: {testId: response.data.tests[0].id}})
    })
    .catch(error => console.log(error.response))
  }

  const loginFields = [
    {name: "email", label: "Email:", placeholder: "login email", inputType: "text"},
  ]

  return (
  <div className="container">
    <div className="d-flex justify-content-center align-items-center mt-5">
      <div style={{maxWidth: 1000}}>
        <FormBase fields={loginFields} onSubmit={onSubmit} submitLabel="start test" formMeta={{resolver: yupResolver(validation_schema), mode: 'onChange'}}/>
      </div>
    </div>
  </div>
  )
}
export default LandingPage