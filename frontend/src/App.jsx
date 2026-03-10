import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './pages/Login'
import Register from './pages/Register'
import Rooms from './pages/Rooms'
import BookingList from './pages/BookingList'
import CreateBooking from './pages/CreateBooking'
import EditBooking from './pages/EditBooking'
import ProtectedRoute from './components/ProtectedRoute'
import Navigation from './components/Navigation'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    setIsAuthenticated(!!token)
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return <div className="loading-container"><div className="spinner"></div></div>
  }

  return (
    <BrowserRouter>
      {isAuthenticated && <Navigation />}
      <Routes>
        <Route
          path="/login"
          element={!isAuthenticated ? <Login setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/rooms" />}
        />
        <Route
          path="/register"
          element={!isAuthenticated ? <Register /> : <Navigate to="/rooms" />}
        />
        <Route
          path="/rooms"
          element={<ProtectedRoute><Rooms /></ProtectedRoute>}
        />
        <Route
          path="/bookings"
          element={<ProtectedRoute><BookingList /></ProtectedRoute>}
        />
        <Route
          path="/bookings/new"
          element={<ProtectedRoute><CreateBooking /></ProtectedRoute>}
        />
        <Route
          path="/bookings/:id/edit"
          element={<ProtectedRoute><EditBooking /></ProtectedRoute>}
        />
        <Route path="/" element={<Navigate to={isAuthenticated ? "/rooms" : "/login"} />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
