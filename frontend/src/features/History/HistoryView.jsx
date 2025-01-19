import { useParams } from 'react-router-dom';
import { useGetHistoryByAssessmentIdQuery } from "./historyApiSlice";
import PlagiarismAssessment from '../PlagiarismAssessment/PlagiarismAssessment';
import Loading from '../../components/Loading';

const getProgressBarColor = (rating) => {
    if (rating <= 0.25) return "radial-progress text-success";
    if (rating <= 0.50) return "radial-progress text-info";
    if (rating <= 0.75) return "radial-progress text-warning";
    return "radial-progress text-error";
};

const HistoryView = () => {
    const { historyId: assessmentId } = useParams();
    const { data: history, isLoading, isError } = useGetHistoryByAssessmentIdQuery(assessmentId);

    let content;

    if (isLoading) {
        content = (
            <div className="hero bg-base-200 min-h-screen">
                <div className="hero-content flex-col lg:flex-row-reverse">
                    <div className=" w-full max-w-sm shrink-0 shadow-2xl">
                        <Loading />
                    </div>
                </div>
            </div>
        );
    } else if (isError || !history) {
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
        const progressBarColor = getProgressBarColor(history.entities[assessmentId].rating);
        content = (
            <div className="grid grid-cols-1 xl:grid-cols-1 gap-9 px-4 py-3 bg-base-200 w-full">
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-9 px-4 py-3 mx-auto">
                    <div className="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
                        <form className="card-body">
                            <div className="form-control">
                                <label className="label">
                                    <span className="label-text">Tytuł</span>
                                </label>
                                <input type="text" placeholder="Tytuł" className="input input-bordered" value={history.entities[assessmentId].title} readOnly />
                            </div>
                            <div className="form-control">
                                <label className="label">
                                    <span className="label-text">Autor</span>
                                </label>
                                <input type="text" placeholder="Autor" className="input input-bordered" value={history.entities[assessmentId].author} readOnly />
                            </div>
                        </form>
                    </div>
                    <div className="text-center lg:text-right">
                        <div className={progressBarColor} style={{ "--value": 100 - history.entities[assessmentId].rating * 100, "--size": "12rem", "--thickness": "2rem" }} role="progressbar">
                            {history.entities[assessmentId].rating.toFixed(5) * 100}% <br />plagiatu
                        </div>
                    </div>
                </div>
                {/* Dodatkowa sekcja */}
                <div className=" grid-row grid-cols-1 mx-auto">
                    <div className="card bg-base-100 w-full shadow-2xl">
                        <div className="card-body">
                            <h2 className="card-title">Treść</h2>
                            <PlagiarismAssessment plagiarismAssessment={history.entities[assessmentId]} />
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return content;
};

export default HistoryView;
