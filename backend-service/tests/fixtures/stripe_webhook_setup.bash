stripe listen -f http://localhost:8000/stripe/webhook &

STRIPE_CLI_PID=$!

sleep 5

stripe trigger checkout.session.completed --add metadata.user_id=1

