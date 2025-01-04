import { useState } from "react";
import { useUploadHistoryPDFMutation } from "./historyApiSlice";
import { useUploadHistoryDOCXMutation } from "./historyApiSlice";

const AddHistoryByFile = () => {
    const [uploadHistoryPDF, { isLoadingDOCX }] = useUploadHistoryPDFMutation();
    const [uploadHistoryDOCX, { isLoadingPDF }] = useUploadHistoryDOCXMutation();
    const [formData, setFormData] = useState({
        title: "",
        author: "",
        file: null,
    });

    const handleChange = (e) => {
        const { name, value, files } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: files ? files[0] : value, // Jeśli pole jest plikiem, przypisz plik
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.file) {
            alert("Proszę wybrać plik do przesłania.");
            return;
        }

        if (formData.file.type !== "application/pdf" && formData.file.type !== "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
            alert("Nieobsługiwany format pliku. Proszę wybrać plik PDF lub DOCX.");
            return;
        }

        try {
            const form = new FormData();
            form.append("file", formData.file);
            form.append("title", formData.title);
            form.append("author", formData.author);

            // Wywołanie mutacji z danymi formularza
            if (formData.file.type === "application/pdf") {
                await uploadHistoryPDF({ id: "upload", file: form }).unwrap();
            } else {
                await uploadHistoryDOCX({ id: "upload", file: form }).unwrap();
            }

            setFormData({ title: "", author: "", file: null }); // Reset formularza
            alert("Historia z pliku została dodana pomyślnie!");
        } catch (err) {
            console.error("Błąd podczas dodawania historii:", err);
            alert("Nie udało się dodać historii z pliku. Spróbuj ponownie.");
        }
    };

    return (
        <div className="history-form">
            <h2 className="text-3xl font-bold mb-4">Zweryfikuj pracę z pliku</h2>

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
                    <label htmlFor="author" className="label">
                        <span className="label-text">Autor</span>
                    </label>
                    <input
                        type="text"
                        id="author"
                        name="author"
                        placeholder="Wpisz autora"
                        className="input input-bordered w-full max-w-xs"
                        value={formData.author}
                        onChange={handleChange}
                        required
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
                        className="file-input input-bordered w-full max-w-xs"
                        onChange={handleChange}
                        required
                    />
                </div>

                <div>
                    <button 
                        type="submit" 
                        className={`btn mt-4 ${isLoadingPDF || isLoadingDOCX ? "btn-disabled" : "btn-neutral"}`}
                        disabled={isLoadingPDF || isLoadingDOCX}
                    >
                        {isLoadingPDF || isLoadingDOCX ? "Wysyłanie..." : "Sprawdź wpis!"}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AddHistoryByFile;