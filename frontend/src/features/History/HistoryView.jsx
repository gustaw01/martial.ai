import { useParams } from 'react-router-dom';
import { useSelector } from "react-redux";
import { selectHistoryById } from "./historyApiSlice";

const getProgressBarColor = (rating) => {
    if (rating <= 25) return "radial-progress text-error";
    if (rating <= 50) return "radial-progress text-warning";
    if (rating <= 75) return "radial-progress text-info";
    return "radial-progress text-success";
}

const HistoryView = () => {
    const { historyId } = useParams()
    const history = useSelector(state => historyId ? selectHistoryById(state, historyId) : null)

    let content

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
        )
    } else {
        const progressBarColor = getProgressBarColor(history.rating);
        content = (
            <div className="hero bg-base-200">
                <div className="hero-content flex-col lg:flex-row-reverse">
                    <div className="text-center lg:text-left">
                        <div className={progressBarColor} style={{ "--value": history ? history.rating : 0, "--size": "12rem", "--thickness": "2rem" }} role="progressbar">{history ? history.rating : 0}%</div>
                    </div>
                    <div className="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
                        <form className="card-body">
                            <div className="form-control">
                                <label className="label">
                                    <span className="label-text">Tytuł</span>
                                </label>
                                <input type="text" placeholder="Tytuł" className="input input-bordered" value={history ? history.title : null} />
                                </div>
                                <div className="form-control">
                                <label className="label">
                                    <span className="label-text">Treść</span>
                                </label>
                                <input type="text" placeholder="message" className="input input-bordered" value={history ? history.author : null} />
                            </div>
                        </form>
                    </div>
                </div>
                {/* <div className='hero-content flex-col lg:flex-row-reverse'>
                    <div className="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
                        <div className="card-body">
                            <p>
                                {history ? history.message : null}
                            </p>
                        </div>
                    </div>
                </div> */}
            </div>
        )
    }

    return content
}

export default HistoryView