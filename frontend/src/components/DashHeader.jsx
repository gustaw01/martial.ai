import { Link } from 'react-router-dom'

const DashHeader = () => {
    return (
        <header className="header">
            <nav>
                <Link to="/dash">Home</Link>
            </nav>
        </header>
    )
}

export default DashHeader