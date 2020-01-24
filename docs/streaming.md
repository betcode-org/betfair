# Streaming

### Why streaming?

If your aim is to take a snapshot of horse markets 3 minutes before the off and at post time, polling (listMarketBook) is a good solution. You will only hit the Betfair API endpoint 2 times per market.
But if you want to gather, process and react to data more frequently (e.g. in-play horse racing), polling is inefficient and the reason lies in the way HTTP works. Every time you hit a Betfair API endpoint:

- Your machine establishes a new connection with the Betfair server.
- It sends an HTTP request and receives and HTTP response.
- HTTP requests/responses carry headers, so more data is sent/received.

Streaming is more efficient because:

- The connection gets established once.
- From that moment, data keeps flowing from Betfair to your machine.
- There are no data overheads as you would have with polling / HTTP.
- This results in faster data and less CPU from your machine (and Betfair's)

### Market


### Order


### Error Handling


### Listener


### Snap
