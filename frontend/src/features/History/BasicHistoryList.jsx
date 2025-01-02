import { useGetHistoriesQuery } from "./historyApiSlice";
import AlertError from "../../components/AlertError";
import History from "./History";

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
            <div key={history.id} className="overflow-x-auto">
                {history.title} <br />
                Ocena: {history.rating}
                <hr style={{ color: "white" }} />
            </div>
        ));

        content = (
            <div className="overflow-x-auto">
                { historyItems }
            </div>
        )
    }

    return content
}
export default BasicHistoryList