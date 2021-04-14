import Col from "react-bootstrap/esm/Col"


const TableBase = ({data}) => {
  if (!data) {
    return null
  }
  return(
    <div className="mb-5" style={{"height": "300px", "overflow-y": "auto"}}>
      <table className="table table-bordered table-sm table-hover table-striped">
        <thead className="thead-dark">
          <tr>
            {Object.keys(data?.[0]).map(field => (
              <th style={{"position": "sticky", "top": 0}} key={field}>{field}</th>
            )
            )}
          </tr>
        </thead>
        <tbody>
          {data?.map(row => (
            <tr>
              {Object.values(row).map(col => (
                <td>{col?.toString() ?? "null"}</td>
              ))
              }
            </tr>
          ))
          }
        </tbody>
      </table>
    </div>
  )
}

export default TableBase