import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Provider } from 'react-redux'

import './index.css'
import App from './App.jsx'

import { store } from './app/store'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}>
      <BrowserRouter>
          <Routes>
              <Route path="/*" element={<App />} />
          </Routes>
      </BrowserRouter>
    </Provider>
  </StrictMode>,
)
