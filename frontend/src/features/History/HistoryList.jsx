import { useGetHistoriesQuery } from "./historyApiSlice";
import AlertError from "../../components/AlertError";
import History from "./History";

const HistoryList = () => {
    const {
        data: histories,
        isLoading,
        isSuccess,
        isError,
        error,
    } = useGetHistoriesQuery(undefined, {
        pollingInterval: 60000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true
    })

    let content

    if (isLoading) {
        content = <h3>Ładowanie z API</h3>
    }

    if (isError) {
        content = <AlertError error={ error?.data?.message }/>
    }

    if (isSuccess) {
        // console.log(histories.ids.length)
        const tableContent = histories.ids.length > 0
            ? histories.ids.map(historyId => <History key={historyId} id={historyId} />)
            : null

        content = (
            <div className="overflow-x-auto">
                <table className="table">
                    <thead>
                    <tr>
                        <th>ID</th>
                        <th>Tytuł</th>
                        <th>Ocena</th>
                        <th>Treść</th>
                        <th>Autor</th>
                        <th>Przesłano</th>
                        <th>Edit</th>
                    </tr>
                    </thead>
                    <tbody>
                    { tableContent }
                    </tbody>
                </table>
            </div>
        )
    }

    return content
}
export default HistoryList