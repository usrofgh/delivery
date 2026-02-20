local-up:
	docker compose --env-file envs/.env.local -f docker/docker-compose-base.yml -f docker/docker-compose-local.yml up
