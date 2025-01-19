import { Link } from "react-router-dom"

const DashHome = () => {
    return (
        <div className="hero bg-base-200">
            <div className="hero-content text-center">
                <div className="max-w-md">
                    <h1 className="text-5xl font-bold">Witaj w Martial.AI</h1>
                    <p className="py-6">
                        W systemie do weryfikacji prac pod kątem plagiatu. 
                    </p>
                    <Link to="/dash/plagiarism/new" className="btn btn-primary">Zweryfikuj pracę</Link>
                </div>
            </div>
        </div>
    )
}

export default DashHome