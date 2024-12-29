import { Outlet } from "react-router-dom"

const DashLayout = () => {
    return (
        <div className="dash-layout min-h-screen bg-base-200 text-center">
            <Outlet />
        </div>
    )
}

export default DashLayout