import { useGetHistoriesQuery } from "./historyApiSlice";
import AlertError from "../../components/AlertError";
import { Link } from "react-router-dom";
import Loading from "../../components/Loading";

const getProgressBarColor = (rating) => {
    if (rating <= 0.25) return "progress progress-success w-full";
    if (rating <= 0.50) return "progress progress-info w-full";
    if (rating <= 0.75) return "progress progress-warning w-full";
    return "progress progress-error w-full";
}

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
        // content = <Loading />
    }

    if (isError) {
        content = <AlertError error={ error?.data?.message }/>
    }

    if (isSuccess) {
        const historyItems = Object.values(histories.entities).map(history => {
            const progressBarColor = getProgressBarColor(history.rating);
            return (
                <Link to={`/dash/history/${history.id}`} key={history.id}>
                    <button className="btn btn-ghost" style={{ width: "100%" }}>
                        {history.title}
                        <progress className={progressBarColor} value={1 - history.rating} max="1"></progress>
                    </button>
                </Link>
            );
        });

        content = (
            <div className="menu bg-base-200 text-base-content min-h-full w-80 p-4">
                { historyItems }
            </div>
        )
    }

    return content
}
export default BasicHistoryList