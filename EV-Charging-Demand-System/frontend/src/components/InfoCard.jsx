export default function InfoCard({ data }) {
  const demandLevel = data.demand_level || data.level || "Unknown";
  const fastRatio =
    typeof data.fast_ratio === "number"
      ? `${Math.round(data.fast_ratio * 100)}%`
      : data.fast_ratio;

  return (
    <div className="info-card">
      <h3>{data.city}</h3>
      <p><b>Demand Level:</b> {demandLevel}</p>
      <p><b>Predicted Score:</b> {data.score ?? "N/A"}</p>
      <p><b>Charger Count:</b> {data.charger_count ?? "N/A"}</p>
      <p><b>Fast Charger %:</b> {fastRatio ?? "N/A"}</p>
    </div>
  );
}
