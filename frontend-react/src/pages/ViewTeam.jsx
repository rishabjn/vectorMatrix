import {useEffect,useState} from 'react'
import {useParams, Link, useNavigate} from 'react-router-dom'
import api from '../api'

export default function ViewTeam(){
  const {id}=useParams()
  const [team,setTeam]=useState(null)
  const nav = useNavigate()
  useEffect(()=>{api.get('/team/'+id).then(r=>setTeam(r.data)).catch(()=>{})},[id])
  if(!team) return <div className="card">Loading...</div>
  const del = async ()=>{ if(!confirm('Delete?')) return; await api.delete('/team/'+id); nav('/teams') }
  return (
    <div className="card">
      <h1>{team.team_name}</h1>
      <p><strong>Owner:</strong> {team.full_name}</p>
      <p><strong>Email:</strong> {team.email}</p>
      <p><strong>Manager:</strong> {team.manager_name}</p>
      <h3>Documents</h3>
      {team.documents && team.documents.length>0 ? (
        <ul>
          {team.documents.map((d,i)=>(<li key={i}><a href={d} target="_blank" rel="noreferrer">{d}</a></li>))}
        </ul>
      ):<p className="muted">No documents.</p>}
      <div style={{display:'flex',gap:12,marginTop:12}}>
        <Link className="btn" to={`/team/${team.id}/edit`}>Edit</Link>
        <button className="btn" style={{background:'#ff6b6b'}} onClick={del}>Delete</button>
        <Link to="/teams" style={{alignSelf:'center'}}>Back</Link>
      </div>
    </div>
  )
}
