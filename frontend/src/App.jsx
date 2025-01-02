import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './components/Home'
import Login from './features/auth/Login'
import DashHome from './components/DashHome'
import DashLayout from './components/DashLayout'
import HistoryList from './features/History/HistoryList'

import './App.css'

function App() {

  return (
    <Routes>
      <Route path="/" element={ <Layout /> }>
        <Route index element={ <Home /> } />
        <Route path="login" element={<Login />} />

        <Route path="dash" element={ <DashLayout /> }>
          <Route index element={ <DashHome /> } />
          <Route path="history" element={ <HistoryList/> } />
        </Route>
      </Route>
    </Routes>
  )
}

export default App
