import { useState } from "react";
import { useAddNewHistoryMutation } from "./historyApiSlice";
import { useNavigate } from "react-router-dom";


// TODO LANGAGE: Przejazywanie języka jako select w formularzu jako: pl, en, fr
const AddHistory = () => {
    const navigate = useNavigate();
    const [addNewHistory, { isLoading }] = useAddNewHistoryMutation();
    const [formData, setFormData] = useState({
        title: "",
        message: "",
        author: "",
        // TODO: Usunąć rating z formularza w finalnej wersji
        sent_at: new Date().toISOString(),
        rating: 0,
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Wywołanie mutacji z danymi formularza
            await addNewHistory(formData).unwrap();
            setFormData({ title: "", message: "", author: "" }); // Reset formularza
            alert("Wpis został dodany pomyślnie!");
            navigate("/dash/history");
        } catch (err) {
            console.error("Błąd podczas dodawania historii:", err);
            alert("Nie udało się dodać wpisu. Spróbuj ponownie.");
        }
    };

    return (
        <div className="history-form">
            <h1 className="text-3xl font-bold mb-4">Zweryfikuj nową pracę</h1>

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
                    <label htmlFor="message" className="label">
                        <span className="label-text">Treść</span>
                    </label>
                    <textarea
                        id="message"
                        name="message"
                        placeholder="Wpisz treść"
                        className="textarea textarea-bordered"
                        value={formData.message}
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

                <div>
                    <button 
                        type="submit" 
                        className={`btn mt-4 ${isLoading ? "btn-disabled" : "btn-neutral"}`}
                        disabled={isLoading}
                    >
                        {isLoading ? "Wysyłanie..." : "Sprawdź wpis!"}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AddHistory;