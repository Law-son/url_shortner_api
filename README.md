# URL Shortener with Analytics

A backend-only application that shortens long URLs and tracks analytics such as visits, user agents, and IP addresses. Built with Flask, this project demonstrates RESTful API development and backend-centric design.

## Features

- **User Authentication**: Secure access to the API using JWT-based authentication.
- **URL Shortening**: Convert long URLs into short, easily shareable links.
- **Redirection**: Redirect users to the original URL using the shortened link.
- **Analytics Tracking**: Monitor:
  - Total number of visits.
  - Timestamp of visits.
  - User agent and IP address of visitors.
- **RESTful API**: Built using Flask, this API is fully RESTful and follows standard best practices.

---

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL (default database; can be replaced with other SQL databases)
- Pipenv or virtualenv (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Law-son/url-shortener-api.git
   cd url-shortener-api
