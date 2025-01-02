import { useGetHistoriesQuery } from "./historyApiSlice";
import AlertError from "../../components/AlertError";
import { Link } from "react-router-dom";

const BasicHistoryList = () => {
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
        content = <h3>Ładowanie danych z API</h3>
    }

    if (isError) {
        content = <AlertError error={ error?.data?.message }/>
    }

    if (isSuccess) {
        const historyItems = Object.values(histories.entities).map(history => (
            <div key={history.id} className="indicator">
                <span className="indicator-item badge badge-secondary">{history.rating}</span>
                <Link to="/dash/history"><li className="btn btn-ghost" style={{width: "100%"}}>{history.title}</li></Link>
            </div>
        ));

        content = (
            <ul className="menu bg-base-200 text-base-content min-h-full w-80 p-4">
                { historyItems }
            </ul>
        )
    }

    return content
}
export default BasicHistoryList