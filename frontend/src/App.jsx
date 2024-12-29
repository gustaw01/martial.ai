import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './components/Home'
import Login from './features/auth/Login'
import './App.css'
import DashLayout from './components/DashLayout'

function App() {

  return (
    <Routes>
      <Route path="/" element={ <Layout /> }>
        <Route index element={ <Home /> } />
        <Route path="/login" element={<Login />} />
        <Route path="/dash">
          <Route index element={ <DashLayout /> } />
        </Route>
      </Route>
    </Routes>
  )
}

export default App
