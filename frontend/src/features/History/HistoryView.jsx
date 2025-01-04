import { useParams } from 'react-router-dom';
import { useSelector } from "react-redux";
import { selectHistoryById } from "./historyApiSlice";

const getProgressBarColor = (rating) => {
    if (rating <= 25) return "radial-progress text-error";
    if (rating <= 50) return "radial-progress text-warning";
    if (rating <= 75) return "radial-progress text-info";
    return "radial-progress text-success";
};

const HistoryView = () => {
    const { historyId } = useParams();
    const history = useSelector(state => historyId ? selectHistoryById(state, historyId) : null);

    let content;

    if (!history) {
        content = (
            <div className="hero bg-base-200 min-h-screen">
                <div className="hero-content flex-col lg:flex-row-reverse">
                    <div className="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
                        <p>
                            Brak wpisu o podanym ID
                        </p>
                    </div>
                </div>
            </div>
        );
    } else {
        const progressBarColor = getProgressBarColor(history.rating);
        content = (
            <div className="grid grid-cols-1 xl:grid-cols-1 gap-9 px-4 py-3 bg-base-200 w-full">
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-9 px-4 py-3 mx-auto">
                    <div className="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
                        <form className="card-body">
                            <div className="form-control">
                                <label className="label">
                                    <span className="label-text">Tytuł</span>
                                </label>
                                <input type="text" placeholder="Tytuł" className="input input-bordered" value={history.title} readOnly />
                            </div>
                            <div className="form-control">
                                <label className="label">
                                    <span className="label-text">Autor</span>
                                </label>
                                <input type="text" placeholder="Autor" className="input input-bordered" value={history.author} readOnly />
                            </div>
                        </form>
                    </div>
                    <div className="text-center lg:text-right">
                        <div className={progressBarColor} style={{ "--value": history.rating, "--size": "12rem", "--thickness": "2rem" }} role="progressbar">{history.rating}%</div>
                    </div>
                </div>
                {/* Dodatkowa sekcja */}
                <div className=" grid-row grid-cols-1 mx-auto">
                    <div className="card bg-base-100 w-full max-w-3xl shadow-2xl">
                        <div className="card-body">
                            <h2 className="card-title">Treść</h2>
                            {history.message}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return content;
};

export default HistoryView;