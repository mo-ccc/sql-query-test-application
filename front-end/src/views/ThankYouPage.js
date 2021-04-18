import { useLocation} from 'react-router-dom'

const ThankYouPage = () => {
  let data = useLocation().data

  console.log(data)
  if (!data) {
    return (
      <h1>Something went wrong <a href="/">Redirect to home</a></h1>
    )
  }
  return (
    <pre>
      {JSON.stringify(data, undefined, 2)}
    </pre>
  )
}
export default ThankYouPage