import React, { useEffect, useState } from "react";
import { getLog } from "./api.js";
export default function LogViewer() {
  const [log, setLog] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    const fetchLog = async () => {
      try {
        const data = await getLog();
        if (mounted) setLog(data.log || []);
      } finally {
        if (mounted) setLoading(false);
      }
    };
    fetchLog();
    const interval = setInterval(fetchLog, 5000);
    return () => { mounted = false; clearInterval(interval); };
  }, []);

  return (
    <div className="bg-gray-800 p-3 rounded-lg h-full overflow-y-auto font-mono text-sm">
      {loading && <div className="text-cyan-400">Đang tải log...</div>}
      {log.map((entry, i) =>
        <div key={i}>
          <span className={entry.level === "ERROR"
            ? "text-red-400"
            : entry.level === "WARN"
              ? "text-yellow-400"
              : "text-green-300"
          }>
            [{entry.time}] <b>{entry.level}</b>:
          </span> {entry.msg}
        </div>
      )}
    </div>
  );
}
