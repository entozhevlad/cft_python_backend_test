up:
	docker compose -f docker-compose-local.yaml up -d
down:
	docker compose -f docker-compose-local.yaml down && docker networks prune --force
up:
	docker compose -f docker-compose-ci.yaml up -d
down:
	docker compose -f docker-compose-ci.yaml down && docker networks prune --force

