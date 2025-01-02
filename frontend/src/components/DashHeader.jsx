import { Link } from 'react-router-dom'

const DashHeader = () => {
    return (
        <header className="header">
            <nav>
                <Link to="/dash" className="navigation-item">Home</Link>
                <Link to="/dash/history" className="navigation-item">Historia</Link>
            </nav>
        </header>
    )
}

export default DashHeader