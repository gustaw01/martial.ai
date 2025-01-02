const AddHistoryByFile = () => {
    return (
        <div className="history-form">
            <h2 class="text-3xl font-bold">Zweryfikuj pracę z pliku</h2>

            <form>
                <div className="form-control w-full max-w-xs"> {/* Dodany div dla form-control */}
                    <label htmlFor="title" className="label">
                        <span className="label-text">Tytuł</span>
                    </label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        placeholder="Wpisz tytuł"
                        className="input input-bordered w-full max-w-xs"
                    />
                </div>

                <div className="form-control w-full max-w-xs"> {/* Dodany div dla form-control */}
                    <label htmlFor="author" className="label">
                        <span className="label-text">Autor</span>
                    </label>
                    <input
                        type="text"
                        id="author"
                        name="author"
                        placeholder="Wpisz autora"
                        className="input input-bordered w-full max-w-xs"
                    />
                </div>

                <div className="form-control w-full max-w-xs"> {/* Dodany div dla form-control */}
                    <label htmlFor="file" className="label">
                        <span className="label-text">Plik</span>
                    </label>
                    <input type="file" className="file-input input-bordered w-full max-w-xs" /> {/* Dodane style */}
                </div>

                <div>
                    <button type="submit" className="btn btn-neutral mt-4"> {/* Dodany margin top */}
                        Sprawdź wpis!
                    </button>
                </div>
            </form>
        </div>
    )
}

export default AddHistoryByFile