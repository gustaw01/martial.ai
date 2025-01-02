import { Link } from 'react-router-dom'
import DashDrawer from './DashDrawer'

const DashHeader = () => {
    return (
        <header className="header">
            <nav className='navbar bg-base-100'>
                <DashDrawer />
                <Link to="/dash" className="navigation-item btn-ghost btn">
                    Martial.AI
                </Link>
                <Link to="/dash/history" className="navigation-item btn btn-ghost">
                    Historia
                </Link>
                <Link to="/dash/history/new" className="navigation-item btn btn-ghost">
                    Zweryfikuj nową pracę
                </Link>
                <Link to="/dash/history/new-file" className="navigation-item btn btn-ghost">
                    Zweryfikuj nowy plik
                </Link>
                <Link to="/" className="navigation-item btn btn-ghost">Wyloguj się</Link>
            </nav>
        </header>
    )
}

export default DashHeader