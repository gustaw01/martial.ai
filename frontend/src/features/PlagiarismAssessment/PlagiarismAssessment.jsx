import { useRef } from 'react';

const getProgressBarColor = (rating) => {
    if (rating <= 0.25) return "progress progress-success w-full";
    if (rating <= 0.50) return "progress progress-info w-full";
    if (rating <= 0.75) return "progress progress-warning w-full";
    return "progress progress-error w-full";
}

const PlagiarismModal = ({ plagiarism }) => {
    const dialogRef = useRef();
    const textColor = plagiarism.similarity < 0.7 ? "text-success" : "text-error";

    const showPlagiarismModal = () => {
        dialogRef.current.showModal();
    };

    const closePlagiarismModal = () => {
        dialogRef.current.close();
    };

    const progressBarColor = getProgressBarColor(plagiarism.similarity);

    return (
        <>
            <span onClick={showPlagiarismModal} className={`label label-primary cursor-pointer ${textColor}`}>
                {plagiarism.document_sentence}
            </span> 
            <dialog ref={dialogRef} className="modal">
                <div className="modal-box">
                    <h3 className="font-bold text-lg">Szczegóły</h3>
                    <form>
                        <div className="form-control">
                            <label className="label">
                                <span className="label-text">Zdanie z dokumentu</span>
                            </label>
                            <textarea
                                className="textarea h-24 textarea-bordered"
                                value={plagiarism.document_sentence}
                                readOnly
                            />
                        </div>
                        <div className="form-control">
                            <label className="label">
                                <span className="label-text">Zdanie podobne</span>
                            </label>
                            <textarea
                                className="textarea h-24 textarea-bordered"
                                value={plagiarism.matched_sentence || "Brak podobnego zdania w bazie danych"}
                                readOnly
                            />
                        </div>
                        <br />
                        <div className="form-control">
                            <progress className={progressBarColor} value={1 - plagiarism.similarity} max="1"></progress>
                        </div>
                    </form>
                    <br />
                    <button onClick={closePlagiarismModal} className="btn">
                        Zamknij
                    </button>
                </div>
            </dialog>
        </>
    );
};


const PlagiarismAssessment = ({ plagiarismAssessment = {} }) => {
    const { sent_at, rating, rating_other_lang, plagiarisms = [], plagiarisms_other_lang = [] } = plagiarismAssessment;

    return (
        <div>
            {sent_at ? (
                <>
                    <h3 className="font-bold text-lg">Treść po Polsku</h3>
                    <span className="label-text">Data: {sent_at}</span> <br />
                    <span className="label-text">Ocena: {rating}</span> <br /><br /><br />
                    <div className="left-0">
                        {plagiarisms.map((plagiarism, index) => (
                            <PlagiarismModal key={index} plagiarism={plagiarism} />
                        ))}
                    </div>
                    <br /><br />
                    <h3 className="font-bold text-lg">Treść w innych językach</h3>
                    <span className="label-text">Ocena: {rating_other_lang}</span> <br /><br /><br />
                    <div>
                        {plagiarisms_other_lang.map((plagiarism, index) => (
                            <PlagiarismModal key={index} plagiarism={plagiarism} />
                        ))}
                    </div>
                </>
            ) : (
                <div className="hero bg-base-200 min-h-screen">
                    <div className="hero-content flex-col lg:flex-row-reverse">
                        <div className="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
                            <p>Brak oceny dla dokumentu</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PlagiarismAssessment