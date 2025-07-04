import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const groupResults = (results) => {
  const groups = [];
  let current = results[0];
  let count = 1;

  for (let i = 1; i < results.length; i++) {
    if (results[i] === current) {
      count++;
    } else {
      groups.push(current.repeat(count));
      current = results[i];
      count = 1;
    }
  }
  groups.push(current.repeat(count));
  return groups;
};

const analyzeBaccarat = (sequence) => {
  if (sequence.length < 20) return { error: "Nhập tối thiểu 20 ký tự kết quả." };
  const base = sequence.slice(0, 10);
  const main = sequence.slice(10);
  const groups = groupResults(sequence);

  // Simple Pattern Detection
  let last = main[main.length - 1];
  let prev = main[main.length - 2];
  let prediction = "⚠️";
  let pattern = "Unknown";
  let confidence = 0;
  let risk = "Normal";

  if (last === prev) {
    pattern = "Momentum";
    prediction = last;
    confidence = 70;
  } else if ((prev === "P" && last === "B") || (prev === "B" && last === "P")) {
    pattern = "Pingpong";
    prediction = last === "P" ? "B" : "P";
    confidence = 65;
  } else {
    pattern = "Trap Zone";
    risk = "Trap";
    confidence = 50;
  }

  let recommendation = "Avoid";
  if (confidence >= 60) {
    recommendation = "Play";
  }

  return {
    developerView: groups,
    prediction,
    confidence,
    pattern,
    risk,
    recommendation,
  };
};

export default function BaccaratPredictor() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);

  const handleAnalyze = () => {
    const res = analyzeBaccarat(input.trim().toUpperCase());
    setResult(res);
  };

  return (
    <div className="p-4 max-w-xl mx-auto space-y-4">
      <h1 className="text-xl font-bold">🎲 SYNAPSE VISION Baccarat</h1>
      <Input
        placeholder="Nhập kết quả (ví dụ: BBPBPPPPPBBPBBBBPPP)"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <Button onClick={handleAnalyze}>Phân Tích</Button>
      {result && (
        <Card>
          <CardContent className="p-4 space-y-2">
            {result.error ? (
              <p className="text-red-500">{result.error}</p>
            ) : (
              <>
                <p>🧬 <strong>Developer View:</strong> [{result.developerView.join(", ")}]</p>
                <p>🔮 <strong>Prediction:</strong> {result.prediction}</p>
                <p>🎯 <strong>Accuracy:</strong> {result.confidence}%</p>
                <p>📍 <strong>Risk:</strong> {result.risk}</p>
                <p>🧾 <strong>Recommendation:</strong> {result.recommendation}</p>
              </>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
