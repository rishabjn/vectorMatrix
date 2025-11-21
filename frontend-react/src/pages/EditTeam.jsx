import {useEffect,useState} from 'react'
import {useParams, useNavigate} from 'react-router-dom'
import api from '../api'

export default function EditTeam(){
  const {id}=useParams()
  const [form,setForm]=useState(null)
  const nav = useNavigate()
  useEffect(()=>{api.get('/team/'+id).then(r=>setForm({...r.data,documents:r.data.documents.join(', ')})).catch(()=>{})},[id])
  if(!form) return <div className="card">Loading...</div>
  const submit=async(e)=>{ e.preventDefault(); await api.put('/team/'+id,{...form,documents: form.documents ? form.documents.split(',').map(s=>s.trim()) : []}); alert('Updated'); nav('/team/'+id) }
  return (
    <div className="card">
      <h1>Edit Team</h1>
      <form className="grid" onSubmit={submit}>
        <input value={form.full_name} onChange={e=>setForm({...form,full_name:e.target.value})} />
        <input value={form.email} onChange={e=>setForm({...form,email:e.target.value})} />
        <input value={form.team_name} onChange={e=>setForm({...form,team_name:e.target.value})} />
        <input value={form.manager_name} onChange={e=>setForm({...form,manager_name:e.target.value})} />
        <textarea value={form.documents} onChange={e=>setForm({...form,documents:e.target.value})} />
        <div style={{gridColumn:'1/-1',display:'flex',gap:12}}>
          <button className="btn" type="submit">Save</button>
        </div>
      </form>
    </div>
  )
}
