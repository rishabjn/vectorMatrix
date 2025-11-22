import { HashRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Teams from "./pages/Teams";
import ViewTeam from "./pages/ViewTeam";
import EditTeam from "./pages/EditTeam";
import Dashboard from "./pages/Dashboard";
import Ranking from "./pages/Ranking"

export default function App() {
  return (
    <HashRouter>
      <Navbar />
      <main className="app">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/team/:id" element={<ViewTeam />} />
          <Route path="/team/:id/edit" element={<EditTeam />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/ranking/:qid" element={<Ranking />} />

        </Routes>
      </main>
    </HashRouter>
  )
}
