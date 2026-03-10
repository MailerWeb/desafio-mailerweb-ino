import { Link, useNavigate } from 'react-router-dom'
import { authService } from '../services/auth'
import './Navigation.css'

export default function Navigation() {
  const navigate = useNavigate()

  const handleLogout = () => {
    authService.logout()
    navigate('/login')
  }

  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          📅 Booking System
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/rooms" className="nav-link">
              Salas
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/bookings" className="nav-link">
              Reservas
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/bookings/new" className="nav-link nav-link-primary">
              + Nova Reserva
            </Link>
          </li>
          <li className="nav-item">
            <button className="nav-link nav-logout" onClick={handleLogout}>
              Sair
            </button>
          </li>
        </ul>
      </div>
    </nav>
  )
}
