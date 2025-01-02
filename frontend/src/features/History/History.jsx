import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectHistoryById } from "./historyApiSlice";

const History = ({id = null}) => {
    const history = useSelector(state => id ? selectHistoryById(state, id) : null)
    const navigate = useNavigate()

    if (!history) {
        console.error("Nie znaleziono wpisu dla id:", id);
        return <div>Wpis nie istnieje</div>;
    }

    if (history) {
        const handleEdit = () => navigate(`/dash`) //navigate(`/dash/history/${id}`)
        // console.log(history)

        return (
            <tr className="bg-base-200">
                <td>
                    {history.id}
                </td>
                <td>
                    {history.title}
                </td>
                <td>
                    {history.rating}
                </td>
                <td>
                    {history.message}
                </td>
                <td>
                    {history.author}
                </td>
                <td>
                    {history.sent_at}
                </td>
                <td>
                    <button onClick={handleEdit} className="btn btn-primary">Edit</button>
                </td>
            </tr>
        )
    } else return null
}

export default History