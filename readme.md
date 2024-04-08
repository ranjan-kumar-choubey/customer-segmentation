
tets api : 
Health check : curl https://customer-segmentation-3iy1.onrender.com/
elbow curve  : curl https://customer-segmentation-3iy1.onrender.com/elbow-curve

run-model :    curl -X POST "https://customer-segmentation-3iy1.onrender.com/run-rfm?k=3"


--for production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

-- for development
uvicorn main:app --reload

