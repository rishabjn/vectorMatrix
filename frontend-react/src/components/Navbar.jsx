import { Link } from 'react-router-dom';
export default function Navbar(){
  return (
    <nav className="nav">
      <div className="logo">Vector<span>Matrix</span></div>
      <div>
       <Link to="/" className="add-link">Add a new team</Link>{' | '} <Link className="add-link" to="/teams">All Teams</Link>
      </div>
    </nav>
  )
}
