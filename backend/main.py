import uvicorn
from fastapi import FastAPI
from context.user.routes.user import route as user_route
from context.room.routes.room import route as room_route
from context.booking.routes.booking import route as booking_route
from context.outbox.routes.outbox import route as outbox_route
from libs.database import load_tables

app = FastAPI(title="Booking System API")

load_tables()

app.include_router(user_route)
app.include_router(room_route)
app.include_router(booking_route)
app.include_router(outbox_route)

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
