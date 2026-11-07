import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
os.environ["VV_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")
import app as vv  # noqa: E402


class Backend(unittest.TestCase):
    def setUp(self):
        self.c = vv.app.test_client()

    def test_health_and_roles(self):
        self.assertEqual(self.c.get("/api/health").json["status"], "ok")
        roles = self.c.get("/api/roles?lang=ta").json
        self.assertEqual(len(roles), 3)
        self.assertIn("டேட்டா", roles[0]["title"])

    def test_path_orders_biggest_gap_first(self):
        r = self.c.post("/api/path", json={"role": "data-analyst", "lang": "en",
                        "ratings": {"excel": 3, "sql": 0, "stats": 1, "viz": 2, "comm": 3}}).json
        self.assertEqual(r["steps"][0]["skill"], "sql")
        self.assertEqual(r["steps"][-1]["gap"], 0)
        self.assertTrue(0 <= r["readiness"] <= 100)

    def test_all_strong_is_100(self):
        r = self.c.post("/api/path", json={"role": "customer-support", "ratings": {k["id"]: 3 for k in vv.ROLES["customer-support"]["skills"]}}).json
        self.assertEqual(r["readiness"], 100)
        self.assertEqual(r["total_minutes"], 0)

    def test_scoring_good_vs_poor(self):
        q = vv.QUESTIONS["data-analyst"][0]
        good = vv.score_answer(q, "A join combines rows from two tables using a common key. For example an inner join keeps matching rows. Then a left join keeps all left rows.")
        poor = vv.score_answer(q, "um I think maybe like it is a thing")
        self.assertGreater(good["overall"], poor["overall"])
        self.assertGreaterEqual(good["overall"], 70)
        self.assertEqual(vv.score_answer(q, "")["overall"], 0)

    def test_score_endpoint_and_progress(self):
        self.c.post("/api/progress/reset", json={"student": "t1"})
        r = self.c.post("/api/interview/score", json={"student": "t1", "role": "data-analyst", "qid": "da2", "lang": "en",
                        "answer": "I use the median when there are outliers, because the average gets pulled up."})
        self.assertEqual(r.status_code, 200)
        p = self.c.get("/api/progress?student=t1").json
        self.assertEqual(p["attempts"], 1)
        self.assertEqual(self.c.post("/api/interview/score", json={"role": "x", "qid": "nope"}).status_code, 400)

    def test_tamil_answer_matches_tamil_keywords(self):
        q = vv.QUESTIONS["data-analyst"][1]
        self.assertGreater(vv.score_answer(q, "சராசரி மற்றும் median பற்றி நான் கற்றேன்", "ta")["relevance"], 0)

    def test_word_count_tamil_and_hindi(self):
        q = vv.QUESTIONS["hr"][1]
        self.assertEqual(vv.score_answer(q, "என் பலம் குழு வேலை", "ta")["words"], 4)
        self.assertEqual(vv.score_answer(q, "मेरी ताकत टीम वर्क है।", "hi")["words"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
