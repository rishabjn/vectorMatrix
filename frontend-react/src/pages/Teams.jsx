import {useEffect,useState} from 'react'
import api from '../api'
import { Link } from 'react-router-dom'

export default function Teams(){
  const [teams,setTeams]=useState([])
  useEffect(()=>{api.get('/teams').then(r=>setTeams(r.data)).catch(()=>{})},[])
  return (
    <div className="card">
      <h1>Teams</h1>
      {teams.length===0 && <p className="muted">No teams yet.</p>}
      {teams.map(t=>(
        <div className="item" key={t.id}>
          <div>
            <div><strong>{t.team_name}</strong></div>
            <div style={{color:'#9aa4b2'}}>{t.full_name} • {t.manager_name}</div>
          </div>
          <div>
            <Link to={`/team/${t.id}`}>View</Link>
          </div>
        </div>
      ))}
    </div>
  )
}
