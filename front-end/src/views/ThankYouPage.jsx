import { useLocation} from 'react-router-dom'

const ThankYouPage = () => {
  let data = useLocation().data

  const msToHMS = (ms) => {
    // This only works if Hours are less than 24
    return new Date(ms).toISOString().slice(11,19)
  }

  const calcDiff = (date1, date2) => {
    const dateObj1 = new Date(date1)
    const dateObj2 = new Date(date2)
    return Math.abs(dateObj1 - dateObj2)
  }

  if (!data) {
    return (
      <h1>Something went wrong <a href="/">Redirect to home</a></h1>
    )
  }
  return (
    <div className="text-center">
      <div>
        <h1 className="mt-5">Thank you!</h1>
        <h3 className="mt-3">Result: {`${data?.result * 100}%`}</h3>
        <h3 className="mt-3">Time taken: {msToHMS(calcDiff(data?.time_submitted, data?.time_started))}</h3>
      </div>

    </div>
    
  )
}
export default ThankYouPage