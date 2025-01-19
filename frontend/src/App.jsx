import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './components/Home'
import Login from './features/auth/Login'
import DashHome from './components/DashHome'
import DashLayout from './components/DashLayout'
import HistoryList from './features/History/HistoryList'
import AddHistoryByFile from './features/History/AddHistoryByFile'
import HistoryView from './features/History/HistoryView'

import './App.css'
import './input.css'
import AddHistory from './features/History/AddHistory'
import AddPlagiarismAssessment from './features/PlagiarismAssessment/AddPlagiarismAssessment'

function App() {

  return (
    <Routes>
      <Route path="/" element={ <Layout /> }>
        <Route index element={ <Home /> } />
        <Route path="login" element={<Login />} />

        <Route path="dash" element={ <DashLayout /> }>
          <Route index element={ <DashHome /> } />

          <Route path="history/new" element={ <AddHistory />} />
          <Route path="history/new-file" element={ <AddHistoryByFile /> } />
          <Route path="history" element={ <HistoryList/> } />
          <Route path="history/:historyId" element={ <HistoryView />} />

          <Route path="plagiarism/new" element={ <AddPlagiarismAssessment /> } />
        </Route>
      </Route>
    </Routes>
  )
}

export default App
