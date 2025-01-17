# get_events_subscriber takes an EventFilter as input.
# prints Prefect events as they occur
# creates an infinite loop 
# so you'll need to add your own logic to exit it 
# once you've seen the events you're looking for

from prefect.events import get_events_subscriber
from prefect import flow
import asyncio


@flow(log_prints=True)
async def subs():
    seen_events = set()
    async with get_events_subscriber() as subscriber:
        async for event in subscriber:
            print(f"📬 Received event {event.event!r}")
            seen_events.add(event.event)
            if len(seen_events) > 5:
                break


if __name__ == "__main__":
    asyncio.run(subs())