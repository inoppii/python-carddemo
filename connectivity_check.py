import os
import psycopg2
import sys

def test_connection():
    db_url = os.getenv("DATABASE_URL")
    print(f"Testing connection to: {db_url}")
    try:
        conn = psycopg2.connect(db_url, connect_timeout=10)
        print("Successfully connected to Cloud SQL!")
        conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        # Keep alive for Cloud Run health check if needed, or just exit
        # For a simple job or short-lived service
        print("Connectivity test passed.")
        # Cloud Run expects a server to listen on PORT, 
        # but for a quick check we can just print and let it fail start after sensing success in logs.
        # Alternatively, start a dummy server.
        import http.server
        import socketserver
        PORT = int(os.getenv("PORT", 8080))
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("Serving for health check at port", PORT)
            httpd.serve_forever()
    else:
        sys.exit(1)
