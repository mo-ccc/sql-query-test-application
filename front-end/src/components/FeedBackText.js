const FeedBackText = ({data}) => {
  if (!data) {
    return null
  }
  return(
    <div>
    {data?.matches ? 
      <pre style={{color: "green"}}>
        correct
      </pre>
        : 
      <pre style={{color: "red"}}>
        {data?.issues && Object.keys(data?.issues).length ?
          `expected: ${JSON.stringify(data?.issues, undefined, 1).replace(/(["{},])+/g, " ")}`
            :
          "query incorrect"
        }
      </pre>
    }
    </div>
  )
}
export default FeedBackText