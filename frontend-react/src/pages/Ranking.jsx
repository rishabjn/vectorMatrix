import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";

export default function Ranking() {
  const { qid } = useParams();
  const [ranking, setRanking] = useState([]);
  const [loading, setLoading] = useState(true);
  const [queryTitle, setQueryTitle] = useState("");

  useEffect(() => {
    loadRanking();
    loadQueryTitle();
  }, []);

  const loadRanking = async () => {
    try {
      const res = await api.get(`/dashboard/rankings/${qid}`);
      setRanking(res.data || []);
    } catch (err) {
      console.error("Ranking API error", err);
    } finally {
      setLoading(false);
    }
  };

  const loadQueryTitle = async () => {
    try {
      const res = await api.get("/queries/raw");
      const q = res.data.find((x) => x.id === qid);
      if (q) setQueryTitle(q.title);
    } catch (err) {
      console.error("Query title load error", err);
    }
  };

  const getScoreColor = (score) => {
    const p = score * 100;
    if (p >= 70) return "text-green-600 font-semibold";
    if (p >= 40) return "text-yellow-600 font-semibold";
    return "text-red-600 font-semibold";
  };

  const getTeamLogo = (name) => {
    const logos = {
      "vector": "🌀",
      "matrix": "🔷",
      "tools": "🛠",
      "embedded": "⚡",
      "qa": "🔍",
    };

    for (let key of Object.keys(logos)) {
      if (name.toLowerCase().includes(key)) return logos[key];
    }
    return "👥";
  };

  if (loading) {
    return <div className="p-10 text-xl">Loading ranking...</div>;
  }

  return (
    <div className="p-10 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        Full Ranking for Query
      </h1>

      <div className="bg-white shadow-md rounded-xl p-6 mb-8">
        <div className="text-lg font-semibold text-gray-700">{queryTitle}</div>
        <div className="text-sm text-gray-500 mt-1">Query ID: {qid}</div>
      </div>

      <div className="grid gap-4">
        {ranking.map((t, index) => (
          <div
            key={t.team_id}
            className="bg-white p-5 rounded-xl shadow-md border border-gray-200"
          >
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{getTeamLogo(t.team_name)}</span>
                <div>
                  <div className="text-xl font-semibold text-gray-800">
                    {index + 1}. {t.team_name}
                  </div>
                  <div className="text-sm text-gray-500">Team ID: {t.team_id}</div>
                </div>
              </div>

              <div className={getScoreColor(t.score)}>
                {(t.score * 100).toFixed(1)}%
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
