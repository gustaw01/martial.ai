import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAddNewPlagiarismAssessmentMutation } from "./plagiarismAssessmentSlice";

const AddPlagiarismAssessment = () => {
    const author = import.meta.env.VITE_USER || "Anonim";

    const navigate = useNavigate();
    const [addNewPlagiarismAssessment, { isLoading }] = useAddNewPlagiarismAssessmentMutation();

    const [formData, setFormData] = useState({
        file: null,
        text: "",
        author: author,
        title: "",
        language: "",
    })

    const [disableText, setDisableText] = useState(false);
    const [disableFile, setDisableFile] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    
        // Zmiana disableText i disableFile
        if (name === "text" && value.trim() !== "") {
            setDisableFile(true);
        } else if (name === "file" && e.target.files.length > 0) {
            setDisableText(true);
        } else {
            // Przywrócenie, jeśli użytkownik usuwa dane
            if (name === "text" && value.trim() === "") {
                setDisableFile(false);
            }
            if (name === "file" && e.target.files.length === 0) {
                setDisableText(false);
            }
        }
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file && file.size > 50 * 1024 * 1024) { // maksymalnie 50 MB
            alert("Plik jest zbyt duży!");
            return;
        }
        setFormData((prevData) => ({
            ...prevData,
            file: file,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const { file, text, author, title, language } = formData;
    
        // Walidacja: Musi być tekst lub plik, ale nie oba naraz
        if ((!file && !text) || (file && text)) {
            alert("Musisz przesłać **albo tekst**, **albo plik**, ale nie oba jednocześnie.");
            return;
        }
    
        try {
            let newPlagiarismAssessment;
    
            if (file) {
                // Gdy przesyłany jest plik
                const formData = new FormData();
                formData.append("file", file);
                formData.append("author", author);
                formData.append("title", title);
                formData.append("language", language);
    
                newPlagiarismAssessment = formData;
            } else {
                // Gdy przesyłany jest tekst
                newPlagiarismAssessment = {
                    text,
                    author,
                    title,
                    language,
                };
            }
    
            await addNewPlagiarismAssessment(newPlagiarismAssessment).unwrap();
            alert("Praca została dodana pomyślnie!");
            navigate("/dash/history");
        } catch (err) {
            if (err.status === 400) {
                alert("Serwer odrzucił żądanie. Upewnij się, że przesyłasz poprawne dane.");
            } else {
                alert("Wystąpił nieoczekiwany błąd.");
            }
            console.error("Błąd:", err);
        }
    };

    return (
        <div className="history-form">
            <h1 className="text-3xl font-bold mb-4">Dodaj nową pracę</h1>

            <form onSubmit={handleSubmit}>
                <div className="form-control w-full max-w-xs">
                    <label htmlFor="title" className="label">
                        <span className="label-text">Tytuł</span>
                    </label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        placeholder="Wpisz tytuł"
                        className="input input-bordered w-full max-w-xs"
                        value={formData.title}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-control w-full max-w-xs">
                    <label htmlFor="text" className="label">
                        <span className="label-text">Treść</span>
                    </label>
                    <textarea
                        id="text"
                        name="text"
                        className="textarea h-24"
                        value={formData.text}
                        onChange={handleChange}
                        disabled={disableText}
                    />
                </div>

                <div className="form-control w-full max-w-xs">
                    <label htmlFor="file" className="label">
                        <span className="label-text">Plik</span>
                    </label>
                    <input
                        type="file"
                        id="file"
                        name="file"
                        className="input input-bordered w-full max-w-xs"
                        onChange={handleFileChange}
                        disabled={disableFile}
                    />
                </div>

                <div className="form-control w-full max-w-xs">
                    <label htmlFor="author" className="label">
                        <span className="label-text">Język</span>
                    </label>
                    <select
                        id="language"
                        name="language"
                        className="select select-bordered w-full max-w-xs"
                        value={formData.language}
                        onChange={handleChange}
                        required
                    >
                        <option value="" disabled>
                            Wybierz język
                        </option>
                        <option value="pl">Polski</option>
                        <option value="en">Angielski</option>
                        <option value="fr">Francuski</option>
                    </select>
                </div>

                <button type="submit" className="btn">
                    {isLoading ? "Dodawanie..." : "Dodaj pracę"}
                </button>
            </form>
        </div>
    )
}

export default AddPlagiarismAssessment;