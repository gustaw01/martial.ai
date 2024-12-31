import { Outlet } from "react-router-dom"
import DashHeader from "./DashHeader"
import DashFooter from "./DashFooter"
import HistoryList from "../features/History/HistoryList"

const DashLayout = () => {
    return (
        <div className="main-container">
            <div className="history-list">
                <HistoryList />
            </div>
            <div className="main-content">
                <DashHeader />
                <section className="dash-content">
                    <Outlet />
                </section>
                <DashFooter />
            </div>
        </div>
    )
}

export default DashLayout