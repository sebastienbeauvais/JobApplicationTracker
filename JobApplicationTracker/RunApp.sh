#!/bin/bash

cd backend || exit
source venv/bin/activate                                                                                                             
uvicorn app.main:app --reload  > ../backend.log 2>&1 &

cd ../frontend || exit
npm run dev > ../frontend.log 2>&1 &

echo "Backend log: backend.log"
echo "Frontend log: frontend.log"

wait