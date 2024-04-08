curl -o elbow_curve.png http://localhost:8000/elbow-curve


curl -X POST "http://localhost:8000/run-rfm?k=2"


--for production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

-- for development
uvicorn main:app --reload

