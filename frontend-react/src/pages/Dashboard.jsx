import { useEffect, useState } from "react";
import api from "../api";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterTeam, setFilterTeam] = useState("");
  const [sortOrder, setSortOrder] = useState("desc");

  useEffect(() => {
    loadDashboard();
    loadTeams();
  }, []);

  const loadDashboard = async () => {
    try {
      const res = await api.get("/dashboard/matches");
      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadTeams = async () => {
    try {
      const res = await api.get("/teams/processed");
      setTeams(res.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  // Score Badge Color
  const getScoreBadge = (score) => {
    const percent = score * 100;
    if (percent >= 70)
      return "bg-green-500 text-white px-3 py-1 rounded-full text-sm font-bold";
    if (percent >= 40)
      return "bg-yellow-400 text-black px-3 py-1 rounded-full text-sm font-bold";
    return "bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold";
  };

  // Optional team logo selection
  const getTeamLogo = (teamName) => {
    const logos = {
      "vector": "🌀",
      "matrix": "🔷",
      "tools": "🛠",
      "embedded": "⚡",
      "qa": "🔍",
    };

    for (let key of Object.keys(logos)) {
      if (teamName?.toLowerCase().includes(key)) return logos[key];
    }
    return "👥"; // default
  };

  // Filtering
  const filteredData = data.filter((x) =>
    filterTeam ? x.team_id === filterTeam : true
  );

  // Sorting
  const sortedData = [...filteredData].sort((a, b) =>
    sortOrder === "asc" ? a.score - b.score : b.score - a.score
  );

  if (loading)
    return (
      <div className="p-6 text-xl font-semibold text-gray-600">Loading dashboard...</div>
    );

  return (
    <div className="p-10 bg-gray-100 min-h-screen">
      <h1 className="text-4xl font-bold mb-10 text-gray-800 tracking-wide">
        Query → Team Match Dashboard
      </h1>

      {/* Filters */}
      <div className="flex gap-4 mb-8">
        {/* Team Filter */}
        <select
          className="border px-4 py-2 rounded-lg bg-white shadow"
          value={filterTeam}
          onChange={(e) => setFilterTeam(e.target.value)}
        >
          <option value="">All Teams</option>
          {teams.map((t) => (
            <option key={t.id} value={t.id}>
              {t.team_name}
            </option>
          ))}
        </select>

        {/* Sort */}
        <select
          className="border px-4 py-2 rounded-lg bg-white shadow"
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
        >
          <option value="desc">Sort: Score High → Low</option>
          <option value="asc">Sort: Score Low → High</option>
        </select>
      </div>

      {/* Results */}
      {sortedData.length === 0 && (
        <div className="text-gray-500 text-lg">No matched queries found.</div>
      )}

      <div className="grid gap-6">
        {sortedData.map((item) => (
          <div
            key={item.query_id}
            className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-2xl transition duration-300"
          >
            {/* Top Row */}
            <div className="flex justify-between items-center">
              <div className="text-2xl font-semibold text-gray-800 flex items-center gap-3">
                <span className="text-4xl">{getTeamLogo(item.team_name)}</span>
                {item.query_title}
              </div>

              <span className={getScoreBadge(item.score)}>
                {(item.score * 100).toFixed(1)}%
              </span>
            </div>

            {/* Team Section */}
            <div className="mt-4 text-gray-700 text-lg">
              <span className="font-medium">Assigned Team:</span>{" "}
              <span className="text-blue-600 font-bold">
                {item.team_name}
              </span>
            </div>

            {/* Divider */}
            <div className="my-4 border-b border-gray-300"></div>

            {/* Metadata */}
            <div className="grid grid-cols-2 gap-2 text-sm text-gray-600">
              <div>
                <strong className="text-gray-800">Query ID:</strong>{" "}
                {item.query_id}
              </div>
              <div>
                <strong className="text-gray-800">Team ID:</strong>{" "}
                {item.team_id}
              </div>
            </div>

            {/* Full Ranking Link */}
            <div className="mt-5">
              <Link
                to={`/ranking/${item.query_id}`}
                className="text-blue-600 font-semibold hover:underline"
              >
                View full ranking →
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
