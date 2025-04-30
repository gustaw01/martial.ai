import { useGetHistoriesQuery } from "./historyApiSlice";
import AlertError from "../../components/AlertError";
import { Link, useNavigate } from "react-router-dom";

const getProgressBarColor = (rating) => {
    if (rating <= 0.25) return "progress progress-success w-full";
    if (rating <= 0.50) return "progress progress-info w-full";
    if (rating <= 0.75) return "progress progress-warning w-full";
    return "progress progress-error w-full";
};

const BasicHistoryList = () => {
    const navigate = useNavigate();

    const {
        data: histories,
        isLoading,
        isSuccess,
        isError,
        error,
    } = useGetHistoriesQuery(undefined, {
        pollingInterval: 60000,
        refetchOnFocus: true,
        refetchOnMountOrArgChange: true,
    });

    const navigateToHistory = (assessmentId) => {
        navigate(`/dash/history/${assessmentId}`);
        window.location.reload(); // Dodanie odświeżania strony
    };

    let content;

    if (isLoading) {
        // content = <Loading />
    }

    if (isError) {
        content = <AlertError error={error?.data?.message} />;
    }

    if (isSuccess) {
        const historyItems = Object.values(histories.entities).map((history) => {
            const progressBarColor = getProgressBarColor(history.rating);
            return (
                <button
                    onClick={() => navigateToHistory(history.assessment_id)} // Strzałkowa funkcja zapobiega natychmiastowemu wywołaniu
                    key={history.assessment_id}
                    className="btn btn-ghost"
                    style={{ width: "100%" }}
                >
                    {history.title}
                    <progress className={progressBarColor} value={1 - history.rating} max="1"></progress>
                </button>
            );
        });

        content = (
            <div className="menu bg-base-200 text-base-content min-h-full w-80 p-4">
                {historyItems}
            </div>
        );
    }

    return content;
};

export default BasicHistoryList;