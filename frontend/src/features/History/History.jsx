import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectHistoryById } from "./historyApiSlice";

const History = ({id = null}) => {
    const history = useSelector(state => id ? selectHistoryById(state, id) : null)
    const navigate = useNavigate()

    const handleEdit = () => navigate(`/dash/history/${id}`)

    if (!history) {
        console.error("Nie znaleziono wpisu dla id:", id);
        return <div>Wpis nie istnieje</div>;
    }

    if (history) {
        return (
            <tr className="bg-base-200">
                <td>
                    {history.id}
                </td>
                <td>
                    {history.title}
                </td>
                <td>
                    {history.rating} %
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
                    <button onClick={handleEdit} className="btn btn-success">Przejdź</button>
                </td>
            </tr>
        )
    } else return null
}

export default History