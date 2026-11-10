import http from "k6/http";
import { check } from "k6";

const BASE_URL = __ENV.BASE_URL || "http://localhost:5001";

export const options = {
  vus: 10,
  duration: "30s",
  thresholds: {
    http_req_duration: ["p(95)<300"],
  },
};

export default function () {
  const res = http.post(
    `${BASE_URL}/count`,
    JSON.stringify({ text: "hello world from k6 smoke test" }),
    { headers: { "Content-Type": "application/json" } }
  );

  check(res, {
    "status is 200": (r) => r.status === 200,
    "count is present": (r) => r.json("count") !== undefined,
  });
}
