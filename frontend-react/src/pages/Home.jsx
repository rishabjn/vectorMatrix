import { useState } from 'react'
import api from '../api'

export default function Home(){
  const [form,setForm]=useState({full_name:"",email:"",team_name:"",manager_name:"",documents:""})

  const submit=async(e)=>{
    e.preventDefault()
    try{
      await api.post('/teams',{...form,documents: form.documents ? form.documents.split(',').map(s=>s.trim()) : []})
      alert('Saved')
      setForm({full_name:"",email:"",team_name:"",manager_name:"",documents:""})
    }catch(err){
      alert('Error saving')
      console.error(err)
    }
  }

  return (
    <div className="card">
      <h1>Add Team</h1>
      <form className="grid" onSubmit={submit}>
        <input placeholder="Full name" value={form.full_name} onChange={e=>setForm({...form,full_name:e.target.value})} required />
        <input placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} required />
        <input placeholder="Team name" value={form.team_name} onChange={e=>setForm({...form,team_name:e.target.value})} required />
        <input placeholder="Manager name" value={form.manager_name} onChange={e=>setForm({...form,manager_name:e.target.value})} required />
        <textarea placeholder="Document links, comma separated" value={form.documents} onChange={e=>setForm({...form,documents:e.target.value})} />
        <div style={{gridColumn:'1/-1',display:'flex',gap:12}}>
          <button className="btn" type="submit">Save</button>
        </div>
      </form>
    </div>
  )
}
