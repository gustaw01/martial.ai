import { useRef } from 'react';

const PlagiarismModal = ({ plagiarism }) => {
    const dialogRef = useRef();
    const textColor = plagiarism.similarity < 0.7 ? "text-success" : "text-error";

    const showPlagiarismModal = () => {
        dialogRef.current.showModal();
    };

    const closePlagiarismModal = () => {
        dialogRef.current.close();
    };

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
                                className="textarea h-24"
                                value={plagiarism.document_sentence}
                                readOnly
                            />
                        </div>
                        <div className="form-control">
                            <label className="label">
                                <span className="label-text">Zdanie podobne</span>
                            </label>
                            <textarea
                                className="textarea h-24"
                                value={plagiarism.matched_sentence}
                                readOnly
                            />
                        </div>
                        <div className="form-control">
                            <label className="label">
                                <span className="label-text">Podobieństwo</span>
                            </label>
                            <input
                                type="text"
                                className="input input-bordered"
                                value={plagiarism.similarity}
                                readOnly
                            />
                        </div>
                    </form>
                    <button onClick={closePlagiarismModal} className="btn">
                        Zamknij
                    </button>
                </div>
            </dialog>
        </>
    );
};


const PlagiarismAssessment = ({ documentId }) => {
    //const plagiarismAssessment = useSelector(state => documentId ? selectPlagiarismAssessmentById(state, documentId) : null);

    const plagiarismAssessment = {
        "plagiarism":
      [
        {
          "matched_sentence":"Równocześnie młodzieniec kuszony jest przez zło (uosabiane przez mroczną postać Dartha Sidiousa), które odwołuje się do jego ambicji i podsyca je, aby ostatecznie zawrzeć „szatański pakt” – poddanie się mu za cenę zaspokojenia własnych pragnień i posiadania wszechmocy, która okazuje się złudna.",
          "document_sentence":"Równocześnie młodzieniec kuszony jest przez zło (uosabiane przez mroczną postać Dartha Sidiousa), które odwołuje się do jego ambicji i podsyca je, aby ostatecznie zawrzeć „szatański pakt” – poddanie się mu za cenę zaspokojenia własnych pragnień i posiadania wszechmocy, która okazuje się złudna.",
          "similarity":0.9999870312376893,
          "index_in_text":0
        },
        {
          "matched_sentence":"Dobro i Zło są w ''Gwiezdnych wojnach'' przedstawione jednoznacznie, jednak nie oznacza to, że opisywany świat jest czarno-biały: nawet Jedi (w tym Mistrz Yoda) mają swoje słabości.",
          "document_sentence":"Dobro i Zło są w Gwiezdnych wojnach przedstawione jednoznacznie, jednak nie oznacza to, że opisywany świat jest czarno-biały: nawet Jedi (w tym Mistrz Yoda) mają swoje słabości.",
          "similarity":0.9972227202184902,
          "index_in_text":1
        },
        {
          "matched_sentence":"Nawet Vader nie jest w istocie zły, jest zwyczajnym człowiekiem, który uległ powabom zła.",
          "document_sentence":"Nawet Vader nie jest w istocie zły, jest zwyczajnym człowiekiem, który uległ powabom zła.",
          "similarity":0.9999986149925808,
          "index_in_text":2
        },
        {
          "matched_sentence":"''Gwiezdne wojny'' to opowieść o sile tkwiącej w miłości: to, czego nie mogli dokonać najwięksi i najpotężniejsi Rycerze Jedi – pokonanie Sithów – dokonuje się dzięki miłości syna do ojca oraz ojca do syna.",
          "document_sentence":"Gwiezdne wojny to opowieść o sile tkwiącej w miłości: to, czego nie mogli dokonać najwięksi i najpotężniejsi Rycerze Jedi – pokonanie Sithów – dokonuje się dzięki miłości syna do ojca oraz ojca do syna.",
          "similarity":0.9926155276805315,
          "index_in_text":3
        }
      ],
      "plagiarisms_other_lang":
      [
        {
          "matched_sentence":"",
          "document_sentence":"Równocześnie młodzieniec kuszony jest przez zło (uosabiane przez mroczną postać Dartha Sidiousa), które odwołuje się do jego ambicji i podsyca je, aby ostatecznie zawrzeć „szatański pakt” – poddanie się mu za cenę zaspokojenia własnych pragnień i posiadania wszechmocy, która okazuje się złudna.",
          "similarity":0.0,
          "index_in_text":0
        },
        {
          "matched_sentence":"",
          "document_sentence":"Dobro i Zło są w Gwiezdnych wojnach przedstawione jednoznacznie, jednak nie oznacza to, że opisywany świat jest czarno-biały: nawet Jedi (w tym Mistrz Yoda) mają swoje słabości.",
          "similarity":0.0,
          "index_in_text":1
        },
        {
          "matched_sentence":"",
          "document_sentence":"Nawet Vader nie jest w istocie zły, jest zwyczajnym człowiekiem, który uległ powabom zła.",
          "similarity":0.0,
          "index_in_text":2
        },
        {
          "matched_sentence":"",
          "document_sentence":"Gwiezdne wojny to opowieść o sile tkwiącej w miłości: to, czego nie mogli dokonać najwięksi i najpotężniejsi Rycerze Jedi – pokonanie Sithów – dokonuje się dzięki miłości syna do ojca oraz ojca do syna.",
          "similarity":0.0,
          "index_in_text":3
        }
      ],
      "rating":0.997455973532323,
      "rating_other_lang":0.0,
      "assessment_id":5,
      "sent_at":"2025-01-14T22:02:06.035240",
      "id": 1
      } 

      return (
        plagiarismAssessment ? (
            <div>
                <h3 className="font-bold text-lg">
                    Treść po Polsku
                </h3>
                <span className="label-text">Data: {plagiarismAssessment.sent_at}</span> <br />
                <span className="label-text">Ocena: {plagiarismAssessment.rating}</span> <br /><br /><br />
                <div>
                    {plagiarismAssessment.plagiarism.map((plagiarism, index) => (
                        <PlagiarismModal key={index} plagiarism={plagiarism} />
                    ))}
                </div>
                <br /><br />
                <h3 className="font-bold text-lg">
                    Treść w innych językach
                </h3>
                <span className="label-text">Ocena: {plagiarismAssessment.rating_other_lang}</span> <br /><br /><br />
                <div>
                    {plagiarismAssessment.plagiarisms_other_lang.map((plagiarism, index) => (
                        <PlagiarismModal key={index} plagiarism={plagiarism} />
                    ))}
                </div>
            </div>
        ) : (
            <div className="hero bg-base-200 min-h-screen">
                <div className="hero-content flex-col lg:flex-row-reverse">
                    <div className="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
                        <p>
                            Brak oceny dla dokumentu
                        </p>
                    </div>
                </div>
            </div>
        )
    );
}

export default PlagiarismAssessment