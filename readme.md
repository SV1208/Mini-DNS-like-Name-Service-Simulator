# Mini DNS-like Name Service Simulator

## Group Details
|  |  |
| --- | --- |
| Group Number | 3 |
| Project Title | Mini DNS-like Name Service Simulator |

### Team Members
| Name | Roll Number |
| --- | --- |
| Shaurya Kumar | 231020446 |
| Shivanshu Vishwakarma | 231020447 |
| Shiwani Banjare | 231020448 |
| Shrey Omer | 231020449 |
| Shubhang Nande | 231020450 |

## Project Info
This simulator mirrors a small slice of DNS behavior: a **root name server** holds static domain→IP mappings, a **local resolver** caches responses with TTL enforcement, and a **client** issues human-readable domain queries. The flow lets you demonstrate cache hits/misses and see how real DNS reduces latency with caching.

### What does DNS do?
![Domain to IP mapping](diagram2.png)
*DNS maps human-friendly names (e.g., `google.com`) to numeric IP addresses so clients reach the correct servers.*


## Architecture Overview
![Architecture diagram](diagram.png)

1. `client.py` sends a domain query to the local resolver.
2. `resolver.py` inspects its cache (with per-record TTL metadata).
3. Cache hit → respond immediately. Cache miss → forward to `root_server.py`.
4. Root server returns the IP, resolver writes it into cache, and forwards the answer to the client.

## Request Flow
- **Client Query:** User runs `client.py` and enters a domain.
- **Resolver Cache Check:** Resolver returns cached entry if TTL is valid.
- **Cache Miss Path:** Resolver contacts root server over sockets.
- **Cache Refresh:** On root response, resolver stores `{domain, ip, ttl, timestamp}` and answers the client.
- **TTL Expiry:** Once TTL elapses, the resolver evicts the entry and the next lookup triggers another root query.

## Repository Layout
```
project-folder/
├── client.py          # CLI client issuing DNS-style queries
├── resolver.py        # Local resolver with cache + TTL logic
├── root_server.py     # Root name server with static mappings
├── diagram.png        # Architecture overview diagram
├── diagram2.png       # Simple domain-to-IP mapping illustration
└── README.md          # You are here
```

## Prerequisites
- Python 3.x (tested with the standard interpreter)
- No external packages; only built-in `socket`, `time`, `json`, and `threading` modules are used.

## Run the Demo
Open three terminals (or background processes) in the repository root and execute the components in order:

```bash
python root_server.py
python resolver.py
python client.py
```

> On systems where `python3` is required, replace the command accordingly.

## Expected Behavior
- **First lookup:** Cache miss → resolver contacts root server → client receives IP.
- **Second lookup (same domain, within TTL):** Cache hit → resolver responds immediately.
- **After TTL expiry:** Entry invalidated → resolver re-queries root server → cache repopulated.

## How It Works
- `client.py` mimics a browser querying DNS for an IP address.
- `resolver.py` manages an in-memory dictionary keyed by domain with TTL metadata to illustrate caching benefits.
- `root_server.py` behaves like a simplified authoritative/root DNS server exposing fixed domain records.
- The trio demonstrates how caching slashes lookup latency and reduces server load.

## Key Takeaways
- Practical understanding of DNS request/response choreography.
- Hands-on experience with socket programming and lightweight network services.
- Insight into cache invalidation via TTL and its effect on performance.
- Appreciation of how layered DNS components collaborate to resolve names efficiently.
