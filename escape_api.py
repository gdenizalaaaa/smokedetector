# filename: escape_api.py
from fastapi import FastAPI, HTTPException, Header
from collections import deque
from typing import List, Optional
import uvicorn

app = FastAPI()

# Sabit token (şimdilik)
API_TOKEN = "supersecret123"

# -----------------------------
# 1. GRAPH TANIMI (ODA + KAPI)
# -----------------------------
graph = {
    1: [(2, "k1")],
    2: [(1, "k1"), (3, "k17")],
    3: [(2, "k17"), (4, "k3"), (6, "k2")],
    4: [(3, "k3"), (5, "k21")],
    5: [(6, "k4"), (4, "k21")],
    6: [(3, "k2"), (5, "k4"), (7, "k5"), (9, "k6")],
    7: [(6, "k5")],
    8: [(9, "k7")],
    9: [(6, "k6"), (19, "k8"), (8, "k7")],
    10: [(11, "k15")],
    11: [(10, "k15"), (12, "k18")],
    12: [(11, "k18"), (13, "k16"), (15, "k14")],
    13: [(12, "k16")],
    14: [(15, "k13")],
    15: [(14, "k13"), (16, "k11"), (18, "k10"), (12, "k14")],
    16: [(15, "k11")],
    17: [(18, "k12")],
    18: [(19, "k9"), (15, "k10"), (17, "k12")],
    19: [(9, "k8"), (18, "k9"), (20, "k19")],
    20: [(19, "k19"), ("exit", "k20")],
    "exit": [(20, "k20")]
}

# -----------------------------
# 2. BFS EN KISA YOL FONKSİYONU (CLOSED ROOMS EKLENDİ)
# -----------------------------
def find_path(graph, start, target="exit", closed_rooms=None):
    if closed_rooms is None:
        closed_rooms = set()
    else:
        closed_rooms = set(closed_rooms)

    queue = deque()
    queue.append((start, [start], []))  # (oda, oda_yolu, kapı_yolu)
    visited = set()
    last_room = start  # Son ulaşılan oda

    while queue:
        current, room_path, door_path = queue.popleft()
        last_room = current  # her iterasyonda güncelle

        if current == target:
            return room_path, door_path

        if current in visited or current in closed_rooms:
            continue
        visited.add(current)

        for neighbor, door in graph.get(current, []):
            if neighbor not in visited and neighbor not in closed_rooms:
                queue.append((
                    neighbor,
                    room_path + [neighbor],
                    door_path + [door]
                ))

    # Exit'e ulaşılamadıysa son kalınan odayı döndür
    return [last_room], []

# -----------------------------
# 3. FASTAPI ENDPOINT
# -----------------------------
@app.post("/find_path")
def api_find_path(data: dict, x_api_token: Optional[str] = Header(None)):
    # token kontrolü
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Token")

    start_room = data.get("start_room")
    closed_rooms = data.get("closed_rooms", [])

    if start_room is None:
        raise HTTPException(status_code=400, detail="start_room is required")

    # path bul
    rooms, doors = find_path(graph, start_room, closed_rooms=closed_rooms)
   
    return {
        "start_room": start_room,
        "closed_rooms": closed_rooms,
        "rooms": rooms,
        "doors": doors
    }

# -----------------------------
# 4. SERVERI ÇALIŞTIR
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
