python3 manage.py runserver &

sleep 5

SSH_COMMAND_SERVEO_1="ssh -R80:localhost:8000 serveo.net"


$SSH_COMMAND_SERVEO_1 &
