# Rez | Backend Engine

## System Overview
The Rez Backend serves as the primary infrastructure for the Rez ecosystem, managing data persistence, security protocols, and cross-platform communication. It acts as a centralized bridge between the Discord interface and external web services.

## Core Architecture
The system utilizes a dual-component architecture to ensure high availability and separation of concerns:

* **Service Layer (Discord Core):** An asynchronous event-driven engine built on `discord.py`/`disnake` for real-time interaction management.
* **API Gateway (Flask):** A RESTful API interface designed for low-latency data delivery to frontend consumers.

## Technical Stack
* **Runtime:** Python 3.10+
* **API Framework:** Flask
* **Interface Library:** Discord.py / Disnake
* **Database:** Supabase / MongoDB (Hybrid Persistence)
* **Process Management:** PM2 / Docker Containerization

## API Reference

### System Health & Metrics
| Endpoint | Method | Functional Description |
| :--- | :--- | :--- |
| `/api/v1/status` | `GET` | Returns system telemetry and latency metrics. |
| `/api/v1/stats` | `GET` | Retrieves aggregate server and user analytics. |
| `/api/v1/user/<id>`| `GET` | Fetches granular economy and security profiles. |

## Engineering Standards

### Concurrency
The engine leverages `asyncio` for non-blocking I/O operations, ensuring high throughput during peak load.

### Security Implementation
* **Cross-Origin Resource Sharing (CORS):** Strict policy configuration for authorized frontend domains.
* **Environment Abstraction:** Sensitive credentials and connection strings are managed via `.env` environments (excluded from VCS).

## Installation & Deployment

### Local Environment Setup
```bash
# Clone the repository
git clone [https://github.com/SnoW-099/Rez-Backend](https://github.com/SnoW-099/Rez-Backend)

# Navigate to project root
cd Rez-Backend

# Initialize virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
