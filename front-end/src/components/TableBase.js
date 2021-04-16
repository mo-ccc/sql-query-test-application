const TableBase = ({data}) => {
  if (!data) {
    return null
  }
  return(
    <div className="mb-5" style={{"height": "200px", "overflowY": "auto"}}>
      <table className="table table-bordered table-sm table-hover table-striped">
        <thead className="thead-dark">
          <tr>
            {Object.keys(data?.[0]).map(field => (
              <th key={field} style={{"position": "sticky", "top": 0}} >{field}</th>
            )
            )}
          </tr>
        </thead>
        <tbody>
          {data?.map((row, rowid) => (
            <tr key={`row#${rowid}`}>
              {Object.values(row).map((col, colid) => (
                <td key={`${row}.col#${colid}`}>{col?.toString() ?? "null"}</td>
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