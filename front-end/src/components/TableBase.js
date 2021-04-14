import Col from "react-bootstrap/esm/Col"


const TableBase = (data) => {
  return(
    <table className="table table-bordered table-sm table-hover">
      <thead className="thead-dark">
        <tr>
          {Object.keys(data?[0]).map(field => (
            <th key={field}>{field}</th>
          )
          )}
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr>
            {Object.values(row).map(col => (
              <td>{Col.toString()}</td>
            ))
            }
          </tr>
        ))
        }
      </tbody>
    </table>
  )
}