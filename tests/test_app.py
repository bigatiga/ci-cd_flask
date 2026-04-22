import pytest
from app import create_app
from app import storage


@pytest.fixture(autouse=True)
def reset_storage():
    storage.reset()


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as c:
        yield c


# ── storage unit tests ────────────────────────────────────────────

class TestStorage:
    def test_create_task(self):
        task = storage.create("Buy milk")
        assert task["id"] == 1
        assert task["title"] == "Buy milk"
        assert task["done"] is False

    def test_create_empty_title_raises(self):
        with pytest.raises(ValueError):
            storage.create("")

    def test_create_whitespace_title_raises(self):
        with pytest.raises(ValueError):
            storage.create("   ")

    def test_get_all_empty(self):
        assert storage.get_all() == []

    def test_get_all(self):
        storage.create("A")
        storage.create("B")
        assert len(storage.get_all()) == 2

    def test_get_by_id(self):
        t = storage.create("X")
        assert storage.get_by_id(t["id"]) == t

    def test_get_by_id_missing(self):
        assert storage.get_by_id(999) is None

    def test_update_title(self):
        t = storage.create("Old")
        updated = storage.update(t["id"], {"title": "New"})
        assert updated["title"] == "New"

    def test_update_done(self):
        t = storage.create("Task")
        storage.update(t["id"], {"done": True})
        assert storage.get_by_id(t["id"])["done"] is True

    def test_update_missing_raises(self):
        with pytest.raises(KeyError):
            storage.update(999, {"title": "X"})

    def test_update_empty_title_raises(self):
        t = storage.create("Task")
        with pytest.raises(ValueError):
            storage.update(t["id"], {"title": ""})

    def test_delete(self):
        t = storage.create("Task")
        storage.delete(t["id"])
        assert storage.get_by_id(t["id"]) is None

    def test_delete_missing_raises(self):
        with pytest.raises(KeyError):
            storage.delete(999)


# ── API integration tests ─────────────────────────────────────────

class TestAPI:
    def test_health(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.get_json()["status"] == "ok"

    def test_list_empty(self, client):
        r = client.get("/api/tasks")
        assert r.status_code == 200
        assert r.get_json() == []

    def test_create(self, client):
        r = client.post("/api/tasks", json={"title": "Hello"})
        assert r.status_code == 201
        data = r.get_json()
        assert data["title"] == "Hello"
        assert data["done"] is False

    def test_create_no_title(self, client):
        r = client.post("/api/tasks", json={})
        assert r.status_code == 400

    def test_get_task(self, client):
        created = client.post("/api/tasks", json={"title": "T"}).get_json()
        r = client.get(f"/api/tasks/{created['id']}")
        assert r.status_code == 200

    def test_get_missing(self, client):
        r = client.get("/api/tasks/999")
        assert r.status_code == 404

    def test_update(self, client):
        created = client.post("/api/tasks", json={"title": "Old"}).get_json()
        r = client.patch(f"/api/tasks/{created['id']}", json={"done": True})
        assert r.status_code == 200
        assert r.get_json()["done"] is True

    def test_delete(self, client):
        created = client.post("/api/tasks", json={"title": "Del"}).get_json()
        r = client.delete(f"/api/tasks/{created['id']}")
        assert r.status_code == 204

    def test_delete_missing(self, client):
        r = client.delete("/api/tasks/999")
        assert r.status_code == 404
