import { Outlet } from "react-router-dom"
import DashHeader from "./DashHeader"
import DashFooter from "./DashFooter"
import BasicHistoryList from "../features/History/BasicHistoryList"

const DashLayout = () => {
    return (
        <div className="main-container">
            <div className="history-list">
                <BasicHistoryList />
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